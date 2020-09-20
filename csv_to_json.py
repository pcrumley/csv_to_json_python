#! /usr/bin/env python

if __name__ == '__main__':
    import argparse
    from csv_to_json.app import run
    parser = argparse.ArgumentParser(
        description='Program to ETL csv -> JSON.')
    parser.add_argument(
        'csv_file', metavar='csv_file', type=str,
        help='Path to csvfile you want to parse')
    parser.add_argument(
        '-O', default='',
        help='The file the program writes to. Defaults to csvfile.json')

    # Throws an error if a csv file is not given.
    cmd_args = parser.parse_args()

    # Handle where where we are writing our json to.
    outfile = cmd_args.O
    if len(outfile) == 0:
        outfile = cmd_args.csv_file
        split_outfile = outfile.split('.')

        if len(split_outfile) > 1:
            outfile = "".join(split_outfile[0:-1])
        outfile = f"{outfile}.json"

    run(cmd_args.csv_file, outfile)
