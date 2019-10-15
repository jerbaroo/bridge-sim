"""Make all textual information for the thesis."""
from config import Config
from vehicles.stats import vehicle_data_noise_stats, vehicle_density_stats
from util import print_i


def make_all(c: Config):
    """Make all textual information for the thesis."""
    print_i("\n\n" + vehicle_density_stats(c) + "\n")
    print_i("\n\n" + vehicle_data_noise_stats(c) + "\n")
