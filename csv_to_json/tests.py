import unittest
from app import csv_to_user_list, parse_name, extract_transform
import os


class TestCSVtoDictWithSchema(unittest.TestCase):
    def test_name_parser(self):
        """ This tests the parse_name function. it takes in a user_dict
        and modifies in place.
        """
        user_dict = {
            "list_id": 1,
            "first name": "",
            "last name": "",
            "email": "THE_Smiths_Fan02@aol.com"
        }
        full_name = "John Smith"
        config = {
            "delim": ',',
            "show_warnings": True
        }

        parse_name(full_name, user_dict, **config)

        correct_user_dict = {
            "list_id": 1,
            "first name": "John",
            "last name": "Smith",
            "email": "THE_Smiths_Fan02@aol.com"
        }
        # make sure the two dictionarys have the same # of keys
        self.assertEqual(len(correct_user_dict.keys()), len(user_dict.keys()))

        # make sure the two dictionarys have the same keys and values
        for key in correct_user_dict.keys():
            self.assertEqual(user_dict[key], correct_user_dict[key])

    def test_csv_reader(self):
        """Tests the csv_to_user_list. It should take a csv_file, and return
        a list of dictionaries. The csv_file looks like:
        --------
        full_name,email
        John Smith,THE_Smiths_Fan02@aol.com
        Rip van Winkle,sleepyhead+20yrs@gmail.com
        ---------

        and it should return
        ---------
        [
            {
                "full_name": "John Smith",
                "email": "THE_Smiths_Fan02@aol.com"
            },
            {
                "full_name": "Rip van Winkle",
                "email": "sleepyhead+20yrs@gmail.com"
            }
        ]
        """
        testfile_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_test_csv = os.path.join(
            testfile_dir,
            'example_data',
            'test.csv')

        config = {
            "delim": ',',
            "show_warnings": True
        }
        user_list = csv_to_user_list(path_to_test_csv, **config)

    def test_csv_to_python_obj(self):
        """This is close to an integration test, testing everything
        but the writing to a file.

        The csv_file looks like:
        --------
        full_name,email
        John Smith,THE_Smiths_Fan02@aol.com
        Rip van Winkle,sleepyhead+20yrs@gmail.com
        ---------

        and it should return
        ---------
        {
            "user_list_size": 2,
            "user_list": [
                {
                    "list_id": 1,
                    "first name": "John",
                    "last name": "Smith",
                    "email": "THE_Smiths_Fan02@aol.com"
                },
                {
                    "list_id": 2,
                    "first name": "Rip",
                    "last name": "van Winkle",
                    "email": "sleepyhead+20yrs@gmail.com"
                }]
        }
        """
        testfile_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_test_csv = os.path.join(
            testfile_dir,
            'example_data',
            'test.csv')
        config = {
            "delim": ',',
            "show_warnings": True
        }
        users_dict = extract_transform(path_to_test_csv, **config)
        correct_users_dict = {
            "user_list_size": 2,
            "user_list": [
                {
                    "list_id": 1,
                    "first name": "John",
                    "last name": "Smith",
                    "email": "THE_Smiths_Fan02@aol.com"
                },
                {
                    "list_id": 2,
                    "first name": "Rip",
                    "last name": "van Winkle",
                    "email": "sleepyhead+20yrs@gmail.com"
                }]
            }

        # check that the two have the same len key
        self.assertEqual(len(users_dict.keys()), 2)
        # see that the user lists are the same length
        self.assertEqual(users_dict["user_list_size"], 2)
        # iterate over both user lists and compare the values of the user.
        for user, correct_user in zip(users_dict["user_list"],
                                      correct_users_dict["user_list"]):
            self.assertEqual(len(user.keys()), 4)
            for key, val in correct_user.items():
                self.assertEqual(val, user[key])

if __name__ == '__main__':
    unittest.main()
