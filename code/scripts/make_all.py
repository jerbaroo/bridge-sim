"""Make all generated things."""
import scripts.make_plots as make_plots
import scripts.make_text as make_text
from model.bridge_705 import bridge_705_config


if __name__ == "__main__":
    c = bridge_705_config()
    clean = False

    make_plots.make_all(c, clean)
    make_text.make_all(c, clean)