"""Command line interface to make all generated things."""
import sys

import make.make_plots as make_plots
import make.make_text as make_text
import util
from config import Config
from model.bridge.bridge_705 import (
    bridge_705_2d,
    bridge_705_3d,
    bridge_705_config,
    bridge_705_debug_config,
    bridge_705_test_config,
    bridge_705_single_sections,
)
from util import clean_generated, print_i


def make_all(c: Config, d3: bool):
    if d3:
        make_plots.make_all_3d(c)
    else:
        make_plots.make_all_2d(c)
    if "--text" in sys.argv:
        make_text.make_all(c)


def main():
    # util.DEBUG = False

    if "--test" in sys.argv:
        print_i("Main: using test Config")
        c_func = bridge_705_test_config
    elif "--debug" in sys.argv:
        print_i("Main: using debug Config")
        c_func = bridge_705_debug_config
    else:
        print_i("Main: using normal Config")
        c_func = bridge_705_config

    d3 = "--3d" in sys.argv
    single_sections = "--single-sections" in sys.argv

    if d3:
        print_i("Main: using 3D model")

        def bridge_705_3d_overload(*args, **kwargs):
            return bridge_705_3d(
                *args,
                **kwargs,
                single_sections=(
                    bridge_705_single_sections if single_sections else None
                ),
            )

        c = c_func(bridge_705_3d_overload)
    else:
        print_i("Main: using 2D model")
        c = c_func(bridge_705_2d)
    if "--clean" in sys.argv:
        clean_generated(c)
        print_i("Main: finished cleaning")

    make_all(c=c, d3=d3)


if __name__ == "__main__":
    main()
