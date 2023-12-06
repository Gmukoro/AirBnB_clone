#!/usr/bin/python3

"""Defines the FileStorage class."""

import json
from models.base_model import BaseModel

class FileStorage:

     """Represent an abstracted storage engine.

    Attributes:

        __file_path (str): The name of the file to save objects to.

        __objects (dict): A dictionary of instantiated objects.

    """

    dat = '%Y-%m-%dT%H:%M:%S.%f'

    __file_path = "file.json"
    __objects = {}

    def all(self):
        return FileStorage.__objects

    def new(self, obj):
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        serialized_objects = {}
        for key, obj in FileStorage.__objects.items():
            serialized_objects[key] = obj.to_dict()

        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            json.dump(serialized_objects, file, default=str)

    def reload(self):
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for key, ob in data.items():
                    class_name, obj_id = key.split('.')
                    ob['created_at'] = datetime.strptime(ob['created_at'], dat)
                    ob['updated_at'] = datetime.strptime(ob['updated_at'], dat)
                    obj = globals()[class_name](**ob)
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass

