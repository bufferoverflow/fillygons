import sys
import os
from argparse import ArgumentParser


def main(files):
    existing_files = list(filter(os.path.exists, files))

    for i in existing_files:
        print('File contains differences: {}'.format(i))

    if existing_files:
        print('Found {} test cases with differences.'.format(len(existing_files)))
        sys.exit(1)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('files', nargs='...')

    return parser.parse_args()


def script_main():
    main(**vars(parse_args()))
