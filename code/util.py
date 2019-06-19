from colorama import init
from termcolor import colored

init()


def print_i(s):
    """Print some info text."""
    print(colored(s, "green"))


def param_path(c , startswith, path_attr, ignore=[]):
    """A path based on parameters from a Config."""
    attrs = list(filter(lambda x: x.startswith(startswith), dir(c)))
    path = getattr(c, path_attr)
    for attr in filter(
            lambda x: x != path_attr and x not in ignore, attrs):
        print(attr)
