import os
import sys

from colorama import init
from termcolor import colored

from config import Config

init()


def print_i(s):
    """Print some info text."""
    print(colored(s, "green"))


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


def exit():
    """I don't want to import sys when I need sys.exit."""
    sys.exit()
