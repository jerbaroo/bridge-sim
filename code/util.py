"""Useful functions that don't belong anywhere else."""
from __future__ import annotations

import os

import scipy.stats as stats
from colorama import init
from termcolor import colored


init()


DEBUG = False


def print_d(s):
    """Print some debug text."""
    if DEBUG:
        print(colored(f"DEBUG: {s}", "yellow"))


def print_i(s):
    """Print some info text."""
    print(colored(f"INFO: {s}", "green"))


def print_w(s):
    """Print some warning text."""
    print(colored(f"WARN: {s}", "red"))


def clean_generated(c: Config):
    """Remove generated files but keep folders."""
    print_i(f"Removing all files in: {c.generated_dir}")

    def clean_dir(dir_path):
        for root, dir_names, file_names in os.walk(dir_path):
            for file_name in file_names:
                print_i(f"Removing {file_name}")
                os.remove(os.path.join(root, file_name))
            for dir_name in dir_names:
                clean_dir(os.path.join(root, dir_name))

    clean_dir(c.generated_dir)


def kde_sampler(data, print_=False):
    """A generator which returns samples from a KD estimate of the data."""
    kde = stats.gaussian_kde(data)
    i = 1
    while True:
        if print_ and i % 100 == 0:
            print(i, end=", ", flush=True)
        i += 1
        yield kde.resample(1)[0][0]


def pstr(s):
    """A string with some characters removed, for use in filepaths."""
    return s.replace(".", "").replace(" ", "")
