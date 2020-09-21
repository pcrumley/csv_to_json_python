# csv_to_json_python
A script that gives a cli to convert python to json. Only uses standard library modules for python 3.7.

## Overview
This python script takes in a list of csv files
```bash
python csv_to_json.py my_users1.csv my_users2.csv
```

and outputs them to my_users1.json ... You can specify an output with
```bash
python csv_to_json.py my_users1.csv my_users2.csv -O users1.json users2.json
```

It assumes that the csv is in the format
```
full_name,email
John Smith,THE_Smiths_Fan02@aol.com
Rip van Winkle,sleepyhead+20yrs@gmail.com
```
and converts it to a json that looks like
```
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
    }
  ]
}
```

There are also some additional flags, if you run it with the `--warn` flag it will be very strict about
logging any errors in the csv schema to stderr. You can also specify the delimiter in all of the csv files
with the `--delim` option

```
python csv_to_json.py -h
```
has more information.

# Project Structure & Testing
The main file that handles the command line arg parsing is `./csv_to_json.py`

All of the business logic beyond cli parsing is in the `./csv_to_json/main.py`
file, which is relatively self-explanatory.

You can test the code by running `python csv_to_json/tests.py`
