#!/usr/bin/python3

"""Defines the HBnB console."""

import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse_command_arguments(command):
    curly_braces = re.search(r"\{(.*?)\}", command)
    brackets = re.search(r"\[(.*?)\]", command)

    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(command)]
        else:
            lexer = split(command[:brackets.span()[0]])
            parsed_args = [i.strip(",") for i in lexer]
            parsed_args.append(brackets.group())
            return parsed_args
    else:
        lexer = split(command[:curly_braces.span()[0]])
        parsed_args = [i.strip(",") for i in lexer]
        parsed_args.append(curly_braces.group())
        return parsed_args


class HBNBConsole(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __valid_classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, command):
        """Default behavior for cmd module when input is invalid"""
        command_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }

        dot_match = re.search(r"\.", command)

        if dot_match is not None:
            command_list =
            [command[:dot_match.span()[0]], command[dot_match.span()[1]:]]
            dot_match = re.search(r"\((.*?)\)", command_list[1])

            if dot_match is not None:
                sub_command =
                [command_list[1][:dot_match.span()[0]],
                 dot_match.group()[1:-1]]

                if sub_command[0] in command_dict.keys():
                    full_command =
                    "{} {}".format(command_list[0], sub_command[1])
                    return command_dict[sub_command[0]](full_command)

        print("*** Unknown syntax: {}".format(command))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")

        return True

    def do_create(self, command):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        args_list = parse_command_arguments(command)

        if len(args_list) == 0:
            print("** class name missing **")
        elif args_list[0] not in HBNBConsole.__valid_classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(args_list[0])()
            print(new_instance.id)
            storage.save()

    def do_show(self, command):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        args_list = parse_command_arguments(command)
        objects_dict = storage.all()

        if len(args_list) == 0:
            print("** class name missing **")
        elif args_list[0] not in HBNBConsole.__valid_classes:
            print("** class doesn't exist **")
        elif len(args_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args_list[0], args_list[1]) not in objects_dict:
            print("** no instance found **")
        else:
            print(objects_dict["{}.{}".format(args_list[0], args_list[1])])

    def do_destroy(self, command):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id.
        """
        args_list = parse_command_arguments(command)
        objects_dict = storage.all()

        if len(args_list) == 0:
            print("** class name missing **")
        elif args_list[0] not in HBNBConsole.__valid_classes:
            print("** class doesn't exist **")
        elif len(args_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(
                args_list[0], args_list[1]) not in objects_dict.keys():
            print("** no instance found **")

        else:
            del objects_dict["{}.{}".format(args_list[0], args_list[1])]
            storage.save()

    def do_all(self, command):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        """
        args_list = parse_command_arguments(command)
        classes = HBNBConsole.__valid_classes
        if len(args_list) > 0 and args_list[0] not in classes:
            print("** class doesn't exist **")
        else:
            objects_list = []
            for obj in storage.all().values():
                class_name = obj.__class__.__name__
                if len(args_list) > 0 and args_list[0] == class_name:
                    objects_list.append(obj.__str__())
                elif len(args_list) == 0:
                    objects_list.append(obj.__str__())
            print(objects_list)

    def do_count(self, command):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class.
        """
        args_list = parse_command_arguments(command)
        count = 0

        for obj in storage.all().values():
            if args_list[0] == obj.__class__.__name__:
                count += 1

        print(count)

    def do_update(self, command):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.
        """
        args_list = parse_command_arguments(command)
        objects_dict = storage.all()

        if len(args_list) == 0:
            print("** class name missing **")
            return False
        if args_list[0] not in HBNBConsole.__valid_classes:
            print("** class doesn't exist **")
            return False
        if len(args_list) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(
                args_list[0], args_list[1]) not in objects_dict.keys():
            print("** no instance found **")
            return False
        if len(args_list) == 2:
            print("** attribute name missing **")
            return False
        if len(args_list) == 3:
            try:
                type(eval(args_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(args_list) == 4:
            obj = objects_dict["{}.{}".format(args_list[0], args_list[1])]

            if args_list[2] in obj.__class__.__dict__.keys():
                val_type = type(obj.__class__.__dict__[args_list[2]])
                obj.__dict__[args_list[2]] = val_type(args_list[3])
            else:
                obj.__dict__[args_list[2]] = args_list[3]
        elif type(eval(args_list[2])) == dict:
            obj = objects_dict["{}.{}".format(args_list[0], args_list[1])]

            for key, value in eval(args_list[2]).items():
                data_types = {str, int, float}
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in data_types):
                    val_type = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = val_type(value)
                else:
                    obj.__dict__[key] = value

        storage.save()


if __name__ == "__main__":
    HBNBConsole().cmdloop()
