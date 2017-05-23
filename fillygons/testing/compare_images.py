import os
from argparse import ArgumentParser

import pkg_resources
from PIL import Image


def get_overlay(name):
    stream = pkg_resources.resource_stream(
        __name__,
        'resources/overlay_{}.png'.format(name))

    return Image.open(stream).convert()


def paste_with_transparency(image, overlay):
    image.paste(overlay, None, overlay)


def main(expected_path, actual_path, output_path):
    expected = Image.open(expected_path).convert('L')
    actual = Image.open(actual_path).convert('L')

    paste_with_transparency(expected, get_overlay('expected'))
    paste_with_transparency(actual, get_overlay('actual'))

    output = Image.merge('RGB', [expected, actual, expected])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output.save(output_path, 'PNG')


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('expected_path')
    parser.add_argument('actual_path')
    parser.add_argument('output_path')

    return parser.parse_args()


def script_main():
    main(**vars(parse_args()))
