"""
This file is the command line parser for the ASCIIcli module.
This module provides a command line tool for converting images to ASCII art.
"""

import argparse
from src.functions import convert_to_ascii
from src.functions import print_cmd


def main():
    """
    Parses the command line arguments for the ASCII art converter program.
    """

    # cmd arguments
    # define the command line arguments
    parser = argparse.ArgumentParser(
        description="Converts an image to ASCII art.")
    parser.add_argument("path", metavar="path", type=str,
                        help="The path to the image")
    parser.add_argument("--set", type=str, default="1",
                        help="Character set to use for the ASCII art (1 -> 5)",)
    parser.add_argument("--random", type=bool, default=False,
                        help="Character set is scrambled")
    parser.add_argument("--invert", type=bool, default=False,
                        help="Output is inverted")
    parser.add_argument("--darkness", type=int, default=100,
                        help="Darkness of line-art")
    parser.add_argument("--percent", type=int,
                        help="The height of the output")
    args = parser.parse_args()

    # print out the chosen options
    print_cmd(args)
    # call the conversion function from ascii.py
    convert_to_ascii(args)


if __name__ == '__main__':
    main()
