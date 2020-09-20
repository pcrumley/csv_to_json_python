#! /usr/bin/env python

if __name__ == '__main__':
    import argparse
    from csv_to_json.app import run
    parser = argparse.ArgumentParser(
        description='Program to ETL csv -> JSON.')
    parser.add_argument('csvfile', metavar='csvfile', type=str,
                    help='Path to csvfile you want to parse')
    cmd_args = parser.parse_args()

    run(cmd_args.csvfile)
