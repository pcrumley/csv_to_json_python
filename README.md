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
...
```
and converts it to a json that looks like
```
{
  "user_list_size": len(user_list),
  "user_list": [
    {
      "user_id": 1
      "first name": "John",
      "last name": "Smith"
      "email": "THE_Smiths_Fan02@aol.com",
    }
    ...
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

