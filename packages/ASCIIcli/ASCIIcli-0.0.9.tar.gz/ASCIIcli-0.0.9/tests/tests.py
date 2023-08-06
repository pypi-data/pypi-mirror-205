"""
This file is the test area for the ASCIIcli module.
This module provides a command line tool for converting images to ASCII art.
"""

import unittest
import argparse
from unittest.mock import MagicMock
from src.functions import randomize, get_char_set, char_a, char_b, char_c, char_d, char_e


class Testing(unittest.TestCase):
    """
    The group of tests for ASCIIcli.
    """

    def test_randomize(self):
        """
        Tests the randomize function to see if it randomizes the sets when the argument is True.
        """

        args = MagicMock(random=True, set="1")
        randomize(args)
        if args.set == "1":
            self.assertNotEqual(args.set, char_a)
        elif args.set == "2":
            self.assertNotEqual(args.set, char_b)
        elif args.set == "3":
            self.assertNotEqual(args.set, char_c)
        elif args.set == "4":
            self.assertNotEqual(args.set, char_d)
        elif args.set == "5":
            self.assertNotEqual(args.set, char_e)

    # see if character sets are operational
    def test_valid_set_1(self):
        """
        Tests whether or not set one is valid.
        """
        args = argparse.Namespace(set="1")
        char_set = get_char_set(args.set)
        self.assertEqual(char_set, char_a)

    def test_valid_set_2(self):
        """
        Tests whether or not set two is valid.
        """
        args = argparse.Namespace(set="2")
        char_set = get_char_set(args.set)
        self.assertEqual(char_set, char_b)

    def test_valid_set_3(self):
        """
        Tests whether or not set five is valid.
        """
        args = argparse.Namespace(set="3")
        char_set = get_char_set(args.set)
        self.assertEqual(char_set, char_c)

    def test_valid_set_4(self):
        """
        Tests whether or not set four is valid.
        """
        args = argparse.Namespace(set="4")
        char_set = get_char_set(args.set)
        self.assertEqual(char_set, char_d)

    def test_valid_set_5(self):
        """
        Tests whether or not set five is valid.
        """
        args = argparse.Namespace(set="5")
        char_set = get_char_set(args.set)
        self.assertEqual(char_set, char_e)

    def test_invalid_set(self):
        """
        Tests whether or not an invalid set will be shown as valid.
        """
        args = argparse.Namespace(set="10")
        char_set = get_char_set(args.set)
        char_invalid = 0
        self.assertEqual(char_set, char_invalid)


if __name__ == '__main__':
    unittest.main()
