#!/usr/bin/env python3
"""
A test script for BaseModel and FileStorage integration
"""

import unittest
import os
from models import storage
from models.base_model import BaseModel


class TestBaseModelFileStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test environment"""

        cls.model_file = "file.json"
        cls.storage = storage
        cls.base_model = BaseModel()

    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment"""

        try:
            os.remove(cls.model_file)
        except FileNotFoundError:
            pass

    def test_base_model_creation(self):
        """Test if BaseModel is created and stored in FileStorage"""

        obj_id = "{}.{}".format(self.base_model.__class__.__name__, self.base_model.id)
        self.assertIn(obj_id, self.storage.all())
        self.assertIs(self.storage.all()[obj_id], self.base_model)

    def test_save_reload_integration(self):
        """Test if saving and reloading works correctly"""

        obj_id = "{}.{}".format(self.base_model.__class__.__name__, self.base_model.id)

        self.storage.save()

        new_model = BaseModel()
        new_model.save()
        new_obj_id = "{}.{}".format(new_model.__class__.__name__, new_model.id)

        self.storage.reload()

        self.assertIn(new_obj_id, self.storage.all())
        self.assertIs(self.storage.all()[new_obj_id], new_model)

        self.assertIn(obj_id, self.storage.all())
        self.assertIs(self.storage.all()[obj_id], self.base_model)

    def test_file_storage_save_reload(self):
        """Test if FileStorage saves and reloads correctly"""

        new_model = BaseModel()
        new_model.save()
        new_obj_id = "{}.{}".format(new_model.__class__.__name__, new_model.id)

        self.storage.save()

        self.storage.all().clear()

        self.storage.reload()

        self.assertIn(new_obj_id, self.storage.all())
        self.assertIs(self.storage.all()[new_obj_id], new_model)

    def test_file_storage_save_reload_existing_file(self):
        """Test if FileStorage saves and reloads correctly from an existing file"""

        new_model = BaseModel()
        new_model.save()
        new_obj_id = "{}.{}".format(new_model.__class__.__name__, new_model.id)

        self.storage.save()

        new_storage = storage

        new_storage.reload()

        self.assertIn(new_obj_id, new_storage.all())
        self.assertIs(new_storage.all()[new_obj_id], new_model)


if __name__ == "__main__":
    unittest.main()

