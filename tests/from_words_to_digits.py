#!/usr/bin/env python3

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

"""
Test number to digit conversion.
"""

# TIP: to run tests on file change (on Linux).
# bash -c 'while true; do inotifywait -e close_write nerd-dictation tests/from_words_to_digits.py ; tests/from_words_to_digits.py ; done'

import os
import sys

# -----------------------------------------------------------------------------
# General Utilities
#
def execfile_as_module(mod_name, filepath):
    """
    Execute a file path as a Python script.

    :arg mod_name: The name to use for the module.
    :type mod_name: string
    :arg filepath: Path of the script to execute.
    :type filepath: string
    :return: The module which can be passed back in as ``mod``.
    :rtype: ModuleType
    """
    import importlib.util
    import importlib.machinery

    loader = importlib.machinery.SourceFileLoader(mod_name, filepath)
    mod = loader.load_module()

    # While the module name is not added to `sys.modules`, it's important to temporarily
    # include this so statements such as `sys.modules[cls.__module__].__dict__` behave as expected.
    # See: https://bugs.python.org/issue9499 for details.
    modules = sys.modules

    mod_orig = modules.get(mod_name, None)
    modules[mod_name] = mod

    # No error suppression, just ensure `sys.modules[mod_name]` is properly restored in the case of an error.
    try:
        loader.exec_module(mod)
    finally:
        if mod_orig is None:
            modules.pop(mod_name, None)
        else:
            modules[mod_name] = mod_orig

    return mod


def name_of_caller(frame=1):
    """
    Return "class_name.function_name" of the caller or just "function_name".
    """
    frame = sys._getframe(frame)
    fn_name = frame.f_code.co_name
    var_names = frame.f_code.co_varnames
    if var_names:
        if var_names[0] == "self":
            self_obj = frame.f_locals.get("self")
            if self_obj is not None:
                return type(self_obj).__name__ + "." + fn_name
        if var_names[0] == "cls":
            cls_obj = frame.f_locals.get("cls")
            if cls_obj is not None:
                return cls_obj.__name__ + "." + fn_name
    return fn_name


# -----------------------------------------------------------------------------
# Tests

VERBOSE = True

import unittest


class NumberMixIn:
    def assertNumberFromTextEqual(self, words_input, expected_output):
        words = words_input.split()
        nerd_dictation.from_words_to_digits.parse_numbers_in_word_list(
            words,
            numbers_use_separator=True,
        )
        actual_output = tuple(words)
        expected_output = tuple(expected_output.split())
        if VERBOSE:
            print("{:>38}: {!r} -> {!r}".format(name_of_caller(frame=2), words_input, " ".join(actual_output)))
        self.assertEqual(actual_output, expected_output)


class TestNumberNoop(unittest.TestCase, NumberMixIn):
    def test_noop(self):
        self.assertNumberFromTextEqual("", "")

    def test_no_number(self):
        self.assertNumberFromTextEqual("hello world", "hello world")


class TestNumberSeries(unittest.TestCase, NumberMixIn):
    def test_single(self):
        self.assertNumberFromTextEqual("one two", "1 2")
        self.assertNumberFromTextEqual("one two three", "1 2 3")

    def test_teens(self):
        self.assertNumberFromTextEqual("thirteen", "13")
        self.assertNumberFromTextEqual("thirteen fourteen", "13 14")
        self.assertNumberFromTextEqual("nineteen one two three", "19 1 2 3")

    def test_mixed(self):
        self.assertNumberFromTextEqual("one nineteen two fourteen three zero", "1 19 2 14 3 0")
        self.assertNumberFromTextEqual("zero twenty", "0 20")


class TestNumberWhole(unittest.TestCase, NumberMixIn):
    def test_one(self):
        self.assertNumberFromTextEqual("one", "1")

    def test_large_number(self):
        self.assertNumberFromTextEqual(
            "fifty four million two hundred and twelve thousand five hundred and forty seven",
            "54,212,547",
        )

    def test_very_large_number(self):
        self.assertNumberFromTextEqual(
            "fifty four septillion thirteen trillion twelve thousand five hundred and fifty eight million and two",
            "54,000,000,000,013,000,558,012,002",
        )
        self.assertNumberFromTextEqual("two trillion", "2,000,000,000,000")
        self.assertNumberFromTextEqual("two trillion and seven", "2,000,000,000,007")


class TestNumberWholeAutoDelimit(unittest.TestCase, NumberMixIn):
    """
    Detect when a new number has begun, instead of accumulating.
    """

    def test_zero(self):
        self.assertNumberFromTextEqual("two hundred and zero", "200 and 0")
        self.assertNumberFromTextEqual("two hundred and zero and one", "200 and 0 and 1")

    def test_hundreds(self):
        self.assertNumberFromTextEqual("one hundred two hundred", "100 200")
        self.assertNumberFromTextEqual("one hundred two hundred three hundred", "100 200 300")

    def test_hundreds_and_units(self):
        self.assertNumberFromTextEqual("one hundred two hundred and one", "100 201")
        self.assertNumberFromTextEqual("one hundred two hundred three hundred and one", "100 200 301")

    def test_hundreds_complex_1(self):
        self.assertNumberFromTextEqual("one hundred two hundred thousand and one", "100 200,001")

    def test_hundreds_complex_2(self):
        self.assertNumberFromTextEqual(
            "one hundred and three two hundred and thirteen thirteen thousand three hundred and two",
            "103 213 13,302",
        )

    def test_hundreds_complex_3(self):
        self.assertNumberFromTextEqual(
            "sixty hundred fifty thousand",
            "6,000 50,000",
        )

    def test_hundreds_complex_3(self):
        self.assertNumberFromTextEqual(
            ("ninety two "
             "three hundred and three "
             "two hundred and thirteen "
             "thirteen thousand three hundred "
             "four hundred"
             ),
            (
                "92 "
                "303 "
                "213 "
                "13,300 "
                "400"
             ),
        )


if __name__ == "__main__":
    nerd_dictation = execfile_as_module(
        "nerd_dictation",
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "nerd-dictation"),
    )

    unittest.main(verbosity=not VERBOSE)
