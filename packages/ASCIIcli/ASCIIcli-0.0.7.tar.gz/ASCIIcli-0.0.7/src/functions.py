"""
This file is the functions for the ASCIIcli module.
This module provides a command line tool for converting images to ASCII art.
"""

import random
import os
import sys
import string
from PIL import Image

# define characters used
char_a = list(string.ascii_uppercase)
char_b = list(string.digits)
char_c = ["0", "O", "o", "8", "9", "6", "@", "&", ":", '"', "."]
char_d = ["▀", "▄", "▌", "▐", "■", "◽", "◆", "►", "●", "░", "▒", "▓", "█"]
char_e = ['-', '=', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+']


def get_char_set(set_choice):
    """
    Uses choice for character set by number and then returns the chosen set to.
    """

    listed_sets = {"1": char_a, "2": char_b, "3": char_c, "4": char_d, "5": char_e}

    if set_choice in listed_sets:
        return listed_sets[set_choice]

    print("Error: Invalid character set. Please choose 1, 2, 3, 4, or 5.")
    sys.exit()


def randomize(args):
    """
    If random is true randomize the character set.
    """

    char_set = get_char_set(args.set)
    if args.random:
        random.shuffle(char_set)


def get_gray_value(pixel):
    """
    Calculates the gray value of a pixel.
    """

    return int(sum(pixel) / 2)


def convert_to_ascii(args):
    """
    Converts the input image into an ASCII string.
    """

    # input is set
    brush = int(args.darkness)
    invert = bool(args.invert)
    char_set = get_char_set(args.set)
    full_path = os.path.abspath(args.path)

    # set the current working directory to the one of the input image
    os.chdir(os.path.dirname(args.path))

    # run other functions
    randomize(args)

    # resize image
    with Image.open(full_path) as image:
        image = image.resize((args.width, args.height))

    # *convert the image to ASCII art
    ascii_art = ""
    for y_val in range(args.height):
        for x_val in range(args.width):
            pixel = image.getpixel((x_val, y_val))
            gray_value = get_gray_value(pixel)
            if invert:
                gray_value = 255 - gray_value
            if gray_value >= brush:
                ascii_char = " "
            else:
                index = int(gray_value / 10)
                ascii_char = char_set[index % len(char_set)]
            ascii_art += ascii_char
        ascii_art += "\n"

    # generate output file into text
    # add -ascii.txt to imagename
    file_name = args.path.split(".")[0] + "-ascii.txt"
    output_file = os.path.join(full_path, file_name)
    with open(output_file, "w", encoding="utf-8") as enc:
        enc.write(ascii_art)

    # print to output file
    print(f"ASCII art written to {os.path.abspath(output_file)}")


def print_cmd(args):
    """
    Prints all of the variables and the character set. (Used for development.)
    """

    char_set = get_char_set(args.set)
    invert = bool(args.invert)

    # print chosen options
    print(f"Set {args.set} chosen.")
    print(
        " ".join([f"{i+1}. {char_set[i]}, " for i in range(len(char_set))])[:-2])
    print(f"{'Randomization is on.' if args.random else 'Randomization is off.'}")
    print(f"{'Invert is on.' if invert else 'Invert is off.'}")
