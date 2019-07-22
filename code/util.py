"""Useful functions that don't belong anywhere else."""
import os
import sys

import scipy.stats as stats
from colorama import init
from termcolor import colored

from config import Config

init()


def print_d(s):
    """Print some debug text."""
    print(colored(s, "yellow"))


def print_i(s):
    """Print some info text."""
    print(colored(s, "green"))


def print_w(s):
    """Print some warning text."""
    print(colored(s, "orange"))


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


def exit():
    """I don't want to import sys when I need sys.exit."""
    sys.exit()
