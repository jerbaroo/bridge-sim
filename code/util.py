"""Useful functions that don't belong anywhere else."""
from __future__ import annotations
from typing import Union

import os
import math
import numpy as np

import scipy.stats as stats
from colorama import init
from termcolor import colored

init()

# If set to False, then debug statements are disabled globally.
DEBUG = True


# The letters that come after a number e.g. in 1st, 2nd, 3rd.
st = lambda n: "%s" % ("tsnrhtdd"[(np.floor(n/10)%10!=1)*(n%10<4)*n%10::4])


def round_m(x):
    """Round meters to an accuracy that avoids machine error."""
    return np.round(x, decimals=6)


# TODO: Debug argument only needs to be of type bool, we can get the calling
#     module's name automatically.
# https://stackoverflow.com/questions/1095543/get-name-of-calling-functions-module-in-python
def print_d(debug: Union[bool, str], s: str, *args, **kwargs):
    """Print some debug text."""
    if DEBUG and debug:
        path_str = ""
        if isinstance(debug, str):
            path_str = debug
        print(colored(f"DEBUG: {path_str}: {s}", "yellow"), *args, **kwargs)


def print_i(s: str, *args, **kwargs):
    """Print some info text."""
    print(colored(f"INFO: {s}", "green"), *args, **kwargs)


def print_s(s: str):
    """Print some special info text."""
    print(colored(f"INFO: {s}", "cyan"))


def print_w(s: str):
    """Print some warning text."""
    print(colored(f"WARN: {s}", "red"))


def nearest_index(array, value):
    """Return the index of the nearest value in a sorted array."""
    i = np.searchsorted(array, value, side="left")
    if i > 0 and (
            i == len(array) or
            math.fabs(value - array[i - 1]) < math.fabs(value - array[i])):
        return i - 1
    else:
        return i


def clean_generated(c: "Config"):
    """Remove generated files but keep folders."""
    print_w(f"Removing all files in: {c.generated_data_dir}")

    def clean_dir(dir_path):
        for root, dir_names, file_names in os.walk(dir_path):
            for file_name in file_names:
                print_i(f"Removing {file_name}")
                os.remove(os.path.join(root, file_name))
            for dir_name in dir_names:
                clean_dir(os.path.join(root, dir_name))

    clean_dir(c.generated_data_dir)


def kde_sampler(data, print_: bool = False):
    """A generator which returns samples from a KD estimate of the data."""
    kde = stats.gaussian_kde(data)
    i = 1
    while True:
        if print_ and i % 100 == 0:
            print(i, end=", ", flush=True)
        i += 1
        yield kde.resample(1)[0][0]


def safe_str(s: str) -> str:
    """A lowercase string with some special characters replaced."""
    for char in "[]()":
        s = s.replace(char, "")
    s = s.replace(" ", "-")
    s = s.replace(".", ",")
    return s.lower()
