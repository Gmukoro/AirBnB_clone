#!/usr/bin/env python3

"""module for Review"""


from models.base_model import BaseModel


class Review(BaseModel):
    """
    class Review that inherits from BaseModel
    place_id: string - empty string: it will be the Place.id
    user_id: string - empty string: it will be the User.id
    text: "" - string - empty string
    """

    place_id = ""
    user_id = ""
    text = ""
