from colorama import init
from termcolor import colored

init()


def print_i(s):
    """Print some info text."""
    print(colored(s, "green"))
