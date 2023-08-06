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

FAKE_HEIGHT = 26
FAKE_WIDTH = 62

def get_char_set(set_choice):
    """
    Uses choice for character set by number and then returns the chosen set to.
    If 1 is chosen, character set A will be chosen and so on.
    """

    listed_sets = {"1": char_a, "2": char_b,
                   "3": char_c, "4": char_d, "5": char_e}

    if set_choice in listed_sets:
        return listed_sets[set_choice]

    print("Error: Invalid character set. Please choose 1, 2, 3, 4, or 5.")
    sys.exit()

def randomize(args):
    """
    Checks if the random variable is true, if so: randomize the character set.
    """

    char_set = get_char_set(args.set)
    if args.random:
        random.shuffle(char_set)

def find_dir(path):
    """
    Finds the directory file name and complete directory and turns them into a complete path
    """
    file_name = os.path.basename(path)
    directory = os.path.dirname(path)
    complete_path = f"{directory}/{file_name}"
    print("File found:", complete_path)
    return complete_path

def get_gray_value(pixel):
    """
    Calculates the gray value of a pixel in the image.
    """

    return int(sum(pixel) / 2)

def resize_height(image, percent):
    """
    Resizes the image to the given height while maintaining the aspect ratio.
    """

    # calculate the aspect ratio of the original image
    original_width, original_height = image.size

    # calculate the new width and height based on the desired percentage and aspect ratio
    new_height = int(original_height * percent / 200)
    print("Height was resized.", original_height, original_width)

    return new_height

def resize_width(image, percent):
    """
    Resizes the image to the given height while maintaining the aspect ratio.
    """

    # calculate the aspect ratio of the original image
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height

    # calculate the new width and height based on the desired percentage and aspect ratio
    new_height = int(original_height * percent / 100)
    new_width = int(new_height * aspect_ratio)
    print("Width was resized.", original_height, original_width)

    return new_width

def gen_output(argument, complete_dir, finished_art):
    """
    Generates the output .txt file with the ending -ascii.txt.
    """

    # set path
    complete_path = find_dir(complete_dir)

    # generate output file into text
    file_name = argument.split(".")[0] + "-ascii.txt"
    output_file = os.path.join(complete_path, file_name)
    with open(output_file, "w", encoding="utf-8") as enc:
        enc.write(finished_art)

    # print to output file
    print(f"ASCII art written to {os.path.abspath(output_file)}")

def convert_to_ascii(args):
    """
    Converts the input image into an ASCII string.
    """

    # input is set
    char_set = get_char_set(args.set)

    # set the current working directory to the one of the input image
    os.chdir(os.path.dirname(args.path))

    # run other functions
    randomize(args)

    # set path
    complete_path = find_dir(args.path)

    # open and then resize image
    try:
        with Image.open(complete_path) as image:
            # envoke resize function
            used_height = resize_height(image, args.percent)
            used_width = resize_width(image, args.percent)
            print("Used Lines = ", used_height)
            print("Used Chars-Per-Str = ", used_width)
            image = image.resize((used_width, used_height))
    except FileNotFoundError:
        print(f"Error: Could not find file {args.path}")
        sys.exit()

    # convert the image to ASCII art
    ascii_art = ""
    for y_val in range(used_height):
        for x_val in range(used_width):
            pixel = image.getpixel((x_val, y_val))
            gray_value = get_gray_value(pixel)
            if bool(args.invert):
                gray_value = 255 - gray_value
            if gray_value >= int(args.darkness):
                ascii_char = " "
            else:
                index = int(gray_value / 10)
                ascii_char = char_set[index % len(char_set)]
            ascii_art += ascii_char
        ascii_art += "\n"

    gen_output(args.path, complete_path, ascii_art)

def print_cmd(args):
    """
    Prints all of the variables and the character set. (Used for development.)
    """

    char_set = get_char_set(args.set)

    # print chosen options
    print(f"Set {args.set} chosen.")
    print(
        " ".join([f"{i+1}. {char_set[i]}, " for i in range(len(char_set))])[:-2])
    print(f"{'Randomization is on.' if args.random else 'Randomization is off.'}")
    print(f"{'Invert is on.' if bool(args.invert) else 'Invert is off.'}")
