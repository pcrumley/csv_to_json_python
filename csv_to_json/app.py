import csv
import json
import sys


def run(csv_list, json_list, **kwargs):
    """ The main loop of the program, goes over each csvfile in the csvlist
    and writes the json file @ json_list.
    """
    for infile, outfile in zip(csv_list, json_list):
        try:
            extract_transform_write(infile, outfile, **kwargs)

        except CSVSchemaError:
            print(
               f"Warning: was not able to convert csv {infile}",
               file=sys.stderr)


def extract_transform_write(csv_in: str, json_out: str, **kwargs):
    """
    The main logical part of the code. Is passed a csv, and
    a location to write a Json File. Will raise an CSVSchemaError
    if csv_schema is unexpected.
    """
    # first convert the csv into a list of dictionaries
    # in: csv that looks like
    # full_name,email
    # John Smith,THE_Smiths_Fan02@aol.com
    # ...
    #
    # out: list of dictionaries that looks like
    # [
    #    {
    #       "list_id": 1
    #       "first name": "John",
    #       "last name": "Smith"
    #       "email": "THE_Smiths_Fan02@aol.com",
    #    }
    # ]
    user_list = csv_to_user_list(csv_in, **kwargs)

    # now we need to add the metadata
    # {
    #   "user_list_size": "integer, length of the user_list",
    #   "user_list": "The list described above."
    # }

    json_obj = {
        "user_list_size": len(user_list),
        "user_list": user_list,
    }

    # write it to a file
    with open(json_out, 'w') as jsonfile:
        # pretty print for easier debug
        json.dump(json_obj, jsonfile, indent="  ")


def csv_to_user_list(csv_in: str, **kwargs) -> list:
    """
    Extracts the data from the csv
    full_name,email
    John Smith,THE_Smiths_Fan02@aol.com
    ...
    and returns a list structured like
    [
        {
            "list_id": 1,
            "first name": "John",
            "last name": "Smith",
            "email": "THE_Smiths_Fan02@aol.com"
        }
        ...
    ]


    """


    user_list = []
    with open(csv_in, newline='') as csv_file:
        csv_rdr = csv.DictReader(csv_file, delimiter=kwargs['delim'])
        user_list = [row_dict for row_dict in csv_rdr]

    # we want to convert each row to user_list schema requested by the
    # plan in the problem
    #  {
    #     "list_id": "integer, sequence number for this user in the file
    #                starting at 1",
    #     "first name": "John",
    #     "last name": "Smith",
    #     "email": "THE_Smiths_Fan02@aol.com"
    #  }

    # handle the error when the function is called on a csv that does not
    # contain a header with full_name or email.
    if len(user_list) > 0:
        for key in ['full_name', 'email']:
            if key not in user_list[0].keys():
                raise CSVSchemaError(f"Expected a csv with a {key} header")

    result = []

    for i, user in enumerate(user_list):
        """ This method would filter out bad user, I think I should try:
            to keep them instead

        except Exception as e:
            raise
        is_bad = False
        for key in ['full_name', 'email']:
            if key not in user.keys():
                is_bad = True
        if is_bad:
            # We can't process this user, write to stderr and keep goin
            print("I cannot parse user with row:",
                ''.join(val for key, val in user.items()), file=sys.stderr)

        else:
        """

        new_user_dict = {
            "list_id": i+1,
            "first name": "",
            "last name": "",
            "email": ""
        }

        try:
            new_user_dict["email"] = user["email"]

        except KeyError:
            # user doesn't have an email. If we are showing warnings,
            # let's print.
            if kwargs.show_warnings:
                print(
                   "Warning: user {i+1} doesn't have an email in the csv.",
                   file=sys.stderr)

        if "full_name" not in user.keys():
            if kwargs.show_warnings:
                print(
                   "Warning: user {i+1} doesn't have an full_name in the csv.",
                   file=sys.stderr)
        else:
            parsed_name = parse_name(
                user["full_name"],
                new_user_dict,
                **kwargs)

        result.append(new_user_dict)
    return result


def parse_name(full_name: str, user_dict: dict, **kwargs):
    """ A function that takes in a full name and a dictionary of the form

    user_dict = {
        "list_id": i+1,
        "first name": "",
        "last name": "",
        "email": ""
    }

    and it will set the first and last name values.

    We assume the names are split on whitespace and that the first word
    corresponds to the first name and the rest of the words are the last name.

    If there is only one word, we assume it is the last name.

    Neither of these assumtions may be true, so this function could be updated
    in future, so we will print a warning
    """

    split_name = full_name.split(' ')
    if len(split_name) == 0 and kwargs.show_warnings:
        print(
            "Warning: user {user_dict[list_id]} has no name, {split_name[0]}",
            file=sys.stderr)

    elif len(split_name) == 1:
        if kwargs.show_warnings:
            print(
                "Warning: user {user_dict[list_id]} has only 1 name, {split_name[0]}",
                file=sys.stderr)
        user_dict["last name"] = split_name[0]

    else:
        # name is good
        user_dict["first name"] = split_name[0]
        user_dict["last name"] = " ".join(split_name[1:])


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class CSVSchemaError(Error):
    """Exception raised when CSV doesn't have the headers we expect.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
