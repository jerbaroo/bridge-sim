"""Make all textual information for the thesis."""
from config import Config
from data.normal.a16 import vehicle_data_noise_stats, vehicle_density_stats
from model.bridge_705 import bridge_705_config
from util import *


def make_all(c: Config, clean=True):
    """Make all textual information for the thesis."""
    print_i("\n" + vehicle_density_stats(c))
    print_i("\n" + vehicle_data_noise_stats(c))


if __name__ == "__main__":
    make_all(bridge_705_config(), clean=False)
