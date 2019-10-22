"""Statistics on the vehicle data."""
from typing import List

import numpy as np
import scipy.stats as stats

from config import Config
from vehicles.sample import noise_col_names, noise_per_column


def vehicle_density_stats(c: Config):
    """Human readable statistics on vehicle density."""
    data = c.vehicle_data
    num_bins = len(c.vehicle_density)
    groups = length_groups(c, c.vehicle_density_col)
    lengths_dict = {i: 0 for i in range(num_bins)}
    for i, group in groups:
        lengths_dict[i] = len(group)
    lengths_list = list(lengths_dict.values())
    return (
        "Vehicle density info:"
        + "\n" + "\n".join([
            f"Vehicles < than {length} in {c.vehicle_density_col}:"
            + f" {lengths_dict[i]}"
            for i, length
            in enumerate(map(lambda x: x[0], c.vehicle_density))])
        + f"\nmean vehicles per group: {int(np.mean(lengths_list))}"
        + f"\nmin vehicles per group: {np.min(lengths_list)}"
        + f"\nmax vehicles per group: {np.max(lengths_list)}"
        + f"\nstd vehicles per group: {np.std(lengths_list):.2f}")


def vehicle_data_noise_stats(
        c: Config, noise_col_names: List[str]=noise_col_names):
    """Human readable statistics on noise for vehicle data columns."""
    noise_data = noise_per_column(c, noise_col_names)
    data_len = len(c.vehicle_data[noise_col_names[0]])
    return (
        "Noise info:"
        + "\n" + "\n".join([
            f"\"{col_name}\":"
            + f"\n\tremoved {noise_data[i][0]}"
            + f" or {noise_data[i][0] / data_len:.4f}% outliers"
            + f"\n\tstd. dev. of remaining is {noise_data[i][1]:.4f}"
            for i, col_name in enumerate(noise_col_names)]))
