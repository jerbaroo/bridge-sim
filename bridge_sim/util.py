"""A collection of potentially useful functions."""

from __future__ import annotations

import os
import math
import pathlib
from typing import Union, List

import findup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import portalocker
from colorama import init
from scipy.interpolate import interp1d
from termcolor import colored

init()


kg_to_kn = 0.00980665
"""Multiply by this to convert kg to kN."""
kn_to_kg = 1 / kg_to_kn
"""Multiply by this to convert kN to kg."""


def convert_times(f: str, t: str, times: List[float]):
    """Convert time series from one unit to another."""
    second, day = "second", "day"
    if f == day and t == second:
        return np.array(times) * 86400
    if f == second and t == day:
        return np.array(times) / 86400
    raise ValueError(f"Unrecognized: {f}, {t}")


def apply(effect: List[float], signal: List[float]):
    """Given effect interpolated to length of given signal.

    Args:
        effect: effect to interpolate to signal length.
        signal: length of which effect is interpolated to.

    """
    max_len = max(len(effect), len(signal))
    # Signal indices to effect indices.
    i = interp1d(
        np.linspace(0, len(signal) - 1, max_len),
        np.linspace(0, len(effect) - 1, max_len),
    )(np.arange(len(signal)))
    # print(
    #     f"i[0:10] = {i[0:10]}, np.arange(len(effect))[0:10] = {np.arange(len(effect))[0:10]}, effect[0:10] = {effect[0:10]}"
    # )
    # Effect indices to effect.
    return interp1d(np.arange(len(effect)), effect)(i)


def project_dir():
    """Root directory of the project."""
    return pathlib.Path(__file__).parents[1].absolute()


def log(c: "Config", s):
    """Write a string to a log file."""
    with open(c.get_data_path("log", "log.txt"), "a") as f:
        f.write("\n" + s)


def assert_sorted(l):
    """Assert a list is sorted."""
    assert all(l[i] <= l[i + 1] for i in range(len(l) - 1))


# The letters that come after a number e.g. in 1st, 2nd, 3rd.
st = lambda n: "%s" % (
    "tsnrhtdd"[(np.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10 :: 4]
)


def flatten(container, t: type):
    """Flatten into a list of elements of type t."""

    def _flatten(container, t):
        for i in container:
            if isinstance(i, t):
                yield i
            else:
                for j in _flatten(i, t):
                    yield j

    return list(_flatten(container, t))


def round_m(x):
    """Round meters to an accuracy that avoids machine error."""
    return np.around(x, decimals=6)


def print_d(debug: Union[bool, str], s: str, *args, **kwargs):
    """Print some debug text."""
    if debug:
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


def shorten_path(c: Config, filepath: str, bypass_config: bool = False) -> str:
    """Shorten path by mapping to a shorter filepath via a metadata file."""
    # If file already exists at unshortened path, return unshortened path.
    if os.path.exists(filepath):
        return filepath

    if not bypass_config and not c.shorten_paths:
        return filepath
    df_path = c.get_data_path("metadata", "filepath-shortening-map.txt")
    lock_path = df_path + ".lock"

    # Acquire an exclusive file lock.
    with portalocker.Lock(lock_path, flags=portalocker.LOCK_EX) as f:

        def flush():
            """Ensure all results are written back before exiting 'with'."""
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
            raise ValueError(f"Duplicate rows in metadata file: row = {filepath}")
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


def remove_except_npy(c: "Config", keep: str):
    """Remove files except keep .npy files with a given word in the filename."""
    exts = [".npy", ".txt", ".lock"]
    keep = keep.split()
    print_w(f"Removing all files in: {c.generated_data_dir()}")
    print_w(f"Except files containing one of: {keep}")
    print_w(f"Except files with extension: {exts}")
    print_w(f"Except files starting with: 'short'")

    def clean_dir(dir_path):
        for root, dir_names, file_names in os.walk(dir_path):
            for file_name in file_names:
                if (
                    any(file_name.endswith(ext) for ext in exts)
                    or file_name.startswith("short")
                    or any(k in file_name for k in keep)
                ):
                    print_w(f"Keeping {file_name}")
                else:
                    print_i(f"Removing {file_name}")
                    os.remove(os.path.join(root, file_name))
            for dir_name in dir_names:
                clean_dir(os.path.join(root, dir_name))

    clean_dir(c.generated_data_dir())


def scalar(input):
    """Accepts scalars and lists of length one, returns a scalar."""
    try:
        if len(input) == 1:
            return input[0]
        raise ValueError(f"Not a scalar: {input}")
    except:
        return input


def safe_str(s: str) -> str:
    """A lowercase string with some special characters replaced."""
    for char in "[]()'":
        s = s.replace(char, "")
    s = s.replace(" ", "-")
    s = s.replace(".", ",")
    return s.lower()


def flip(l, ref):
    assert len(l) == len(ref)
    ref_zeros = len(l) - np.count_nonzero(ref)
    zeros = ref_zeros - np.count_nonzero(l[:ref_zeros])
    print(f"ref_zeros, zeros = {ref_zeros}, {zeros}")
    if zeros / ref_zeros >= 0.5:
        return l

    def flip_(l_):
        if l_ == 0:
            return 1
        if l_ == 1:
            return 0
        return l_

    return list(map(flip_, l))


def get_dir(directory: str):
    """The given directory path but creating the directories if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def plot_hours(df):
    """Plot a black vertical line at every 00:00."""
    label_set = False
    for dt in df["datetime"]:
        if np.isclose(float(dt.hour + dt.minute), 0):
            label = None
            if not label_set:
                label = "Time at vertical line = 00:00"
                label_set = True
            plt.axvline(x=dt, linewidth=1, color="black", label=label)
