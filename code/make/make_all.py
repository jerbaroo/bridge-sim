"""Make all generated things."""
import make.make_plots as make_plots
import make.make_text as make_text
from config import Config
from model.bridge.bridge_705 import bridge_705_config


def make_all(c: Config, clean: bool):
    make_plots.make_all(c, clean)
    make_text.make_all(c, clean)


if __name__ == "__main__":
    c = bridge_705_config()
    clean = False
    make_all(c=c, clean=clean)
