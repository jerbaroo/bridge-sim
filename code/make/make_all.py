"""Make all generated things."""
import sys

import make.make_plots as make_plots
import make.make_text as make_text
from config import Config
from make.make_plots import make_contour_plots
from model.bridge.bridge_705 import bridge_705_2d, bridge_705_3d, bridge_705_test_config
from util import clean_generated, print_i


def make_all(c: Config, d3: bool):
    if d3:
        make_plots.make_all_3d(c)
    else:
        make_plots.make_all_2d(c)
    make_text.make_all(c)


def main():
    d3 = "--3d" in sys.argv
    if d3:
        print_i("Using 3D model")
        c = bridge_705_test_config(bridge_705_3d)
    else:
        print_i("Using 2D model")
        c = bridge_705_test_config(bridge_705_2d)
    if "--clean" in sys.argv:
        clean_generated(c)
        print_i("Finished cleaning")
    make_all(c=c, d3=d3)


if __name__ == "__main__":
    main()
