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

    __file_path = "data.json"
    __objects = {}

    def all(self):
        """Returns the dictionary of stored objects."""
        return self.__objects

    def new(self, obj):
        """Adds instance to objects_dict with key <instance_class_name>.id."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serializes objects_dict to the JSON file file_path."""
        key_val = self.__objects.items()
        serialized_objects = {key: val.to_dict() for key, val in key_val}
        with open(self.__file_path, "w") as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Deserializes the JSON file in file_path to objects, if it exists."""
        try:
            with open(self.__file_path) as file:
                serialized_objects = json.load(file)
                for obj_data in serialized_objects.values():
                    class_name = obj_data["__class__"]
                    del obj_data["__class__"]
                    self.new(eval(class_name)(**obj_data))
        except FileNotFoundError:
            return
