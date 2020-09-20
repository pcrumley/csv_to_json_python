#! /usr/bin/env python

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

if __name__ == '__main__':
    import argparse
    from csv_to_json.app import run

    parser = argparse.ArgumentParser(
        description='Program to ETL csv -> JSON.')

    parser.add_argument(
        'csv_files', nargs='+', metavar='csv_files', type=str,
        help='Path to csvfile you want to parse')

    parser.add_argument(
        '-O', nargs='+', default=[],
        help='The file the program writes to. Defaults to csvfile.json')

    parser.add_argument(
        '--delim', default=',',
        help='specify the deliminator of the csv_file')

    parser.add_argument(
        '--warn', action="store_true",
        help='the application will print formatting warning to stderr'
    )

    # Throws an error if a csv file is not given.
    cmd_args = parser.parse_args()

    # Handle where where we are writing our json to.
    outfiles = cmd_args.O
    if len(outfiles) == 0:
        for csv_in in cmd_args.csv_files:
            outfile = csv_in
            split_outfile = outfile.split('.')

            if len(split_outfile) > 1:
                outfile = ".".join(split_outfile[0:-1])
            outfiles.append(f"{outfile}.json")

    elif len(outfiles) != len(cmd_args.csv_files):
        raise InputError(
            "If you are specifying the output files, the number of outputs must equal the number of inputs"
        )

    config = {
        "delim": cmd_args.delim,
        "show_warnings": cmd_args.warn
    }

    run(cmd_args.csv_files, outfiles, **config)
