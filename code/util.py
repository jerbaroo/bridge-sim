"""Useful functions that don't belong anywhere else."""
from __future__ import annotations

import os
import math
from typing import Union

import numpy as np
import pandas as pd
import portalocker
import scipy.stats as stats
from colorama import init
from termcolor import colored

init()

# If set to False, then debug statements are disabled globally.
DEBUG = True


def assert_sorted(l):
    assert all(l[i] <= l[i + 1] for i in range(len(l) - 1))


# The letters that come after a number e.g. in 1st, 2nd, 3rd.
st = lambda n: "%s" % (
    "tsnrhtdd"[(np.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10 :: 4]
)


def flatten(container, t):
    def _flatten(container, t):
        for i in container:
            if not isinstance(i, t):
                for j in _flatten(i, t):
                    yield j
            else:
                yield i

    return list(_flatten(container, t))


def round_m(x):
    """Round meters to an accuracy that avoids machine error."""
    return np.around(x, decimals=6)


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
        i == len(array) or math.fabs(value - array[i - 1]) < math.fabs(value - array[i])
    ):
        return i - 1
    else:
        return i


def shorten_path(c: Config, filepath: str) -> str:
    """Shorten path by mapping to shorter filepath saved on disk."""
    if not c.shorten_paths:
        return filepath
    df_path = c.get_data_path("metadata", "filepath-shortening-map.txt")
    lock_path = df_path + ".lock"
    # with FileLock(df_path + ".lock"):
    with portalocker.Lock(lock_path, flags=portalocker.LOCK_EX) as f:

        def flush():
            f.flush()
            os.fsync(f.fileno())

        if os.path.exists(df_path):
            df = pd.read_csv(df_path, index_col=0)
        else:
            df = pd.DataFrame(columns=["original", "short"])
        existing_row = df[df["original"] == filepath]
        if len(existing_row) == 1:
            return str(existing_row["short"].iloc[0])
        elif len(existing_row) > 1:
            raise ValueError("Oops")
        short = len(df.index) + 1
        short = os.path.join(
            os.path.dirname(filepath),
            "short" + str(short) + os.path.splitext(filepath)[1],
        )
        if not os.path.exists(os.path.dirname(short)):
            os.makedirs(os.path.dirname(short))
        df = df.append({"original": filepath, "short": short}, ignore_index=True)
        df.to_csv(df_path)
        flush()
    print_i(f"Shortened path to: {short}")
    return short


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

    clean_dir(c.generated_data_dir())


def scalar(input):
    try:
        if len(input) == 1:
            return input[0]
        raise ValueError(f"Not a scalar: {input}")
    except:
        return input


def kde_sampler(data, print_: bool = False):
    """A generator which returns samples from a KD estimate of the data."""
    kde = stats.gaussian_kde(data)
    i = 1
    while True:
        if print_ and i % 100 == 0:
            print(i, end=", ", flush=True)
        i += 1
        yield kde.resample(1)[0][0]


def read_csv(path: str, min_spaces: int = 0, ignore: int = 1):
    """Read CSV data from a file.

    'ignore' first lines are ignored as are lines with '<= min_spaces' spaces.

    """
    with open(path) as f:
        return list(
            map(
                lambda line: list(map(float, line.split(","))),
                filter(
                    lambda line: len(line.split()) > min_spaces, f.readlines()[ignore],
                ),
            )
        )


def safe_str(s: str) -> str:
    """A lowercase string with some special characters replaced."""
    for char in "[]()":
        s = s.replace(char, "")
    s = s.replace(" ", "-")
    s = s.replace(".", ",")
    return s.lower()


kg_to_kn = 0.00980665
kn_to_kg = 1 / kg_to_kn
