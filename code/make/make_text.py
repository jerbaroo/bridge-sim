"""Make all textual information for the thesis."""
from config import Config
from model.bridge.bridge_705 import bridge_705_config
from vehicles.stats import vehicle_data_noise_stats, vehicle_density_stats


def make_all(c: Config, clean=True):
    """Make all textual information for the thesis."""
    print_i("\n\n" + vehicle_density_stats(c) + "\n")
    print_i("\n\n" + vehicle_data_noise_stats(c) + "\n")


if __name__ == "__main__":
    make_all(bridge_705_config(), clean=False)
