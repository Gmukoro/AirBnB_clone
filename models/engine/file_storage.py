#!/usr/bin/python3

"""Defines the FileStorage class."""

import json

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """This class represents an abstracted storage engine.

    Attributes:
        file_path (str): The name of the file used to save objects.
        objects_dict (dict): A dictionary storing instantiated objects.
    """

    file_path = "file.json"
    objects_dict = {}

    def all_instances(self):
        """Returns the dictionary of stored objects."""
        return FileStorage.objects_dict

    def add_instance(self, instance):
        """Adds instance to objects_dict with key <instance_class_name>.id."""
        class_name = instance.__class__.__name__
        FileStorage.objects_dict["{}.{}".format(class_name, instance.id)] = instance

    def save_instances(self):
        """Serializes objects_dict to the JSON file file_path."""
        serialized_objects = {key: FileStorage.objects_dict[key].to_dict() for key in FileStorage.objects_dict.keys()}
        with open(FileStorage.file_path, "w") as file:
            json.dump(serialized_objects, file)

    def reload_instances(self):
        """Deserializes the JSON file file_path to objects_dict, if it exists."""
        try:
            with open(FileStorage.file_path) as file:
                serialized_objects = json.load(file)
                for obj_data in serialized_objects.values():
                    class_name = obj_data["__class__"]
                    del obj_data["__class__"]
                    self.add_instance(eval(class_name)(**obj_data))
        except FileNotFoundError:
            return

