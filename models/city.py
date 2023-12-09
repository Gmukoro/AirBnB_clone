#!/usr/bin/python3

"""module for City"""

from models.base_model import BaseModel


class City(BaseModel):
    """
    class City that inherits from BaseModel
    name: string - empty string
    state_id: string
    """

    name = ""
    state_id = ""
