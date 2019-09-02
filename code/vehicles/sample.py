"""Sample vehicles from the vehicle data."""
from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import scipy.stats as stats

from config import Config
from model.load import Vehicle
from vehicles import axle_array_and_count
from util import print_d, print_w

# Print debug information for this file.
D: bool = False

# Column names of the vehicle data to add noise.
noise_col_names = ["speed", "length", "total_weight"]


def length_groups(
        c: Config, col: Optional[str] = None, lengths: List[int] = None):
    """Return vehicle data grouped by a maximum value per group."""
    if col is None:
        col = c.vehicle_density_col
    if lengths is None:
        lengths = list(map(lambda x: x[0], c.vehicle_density))
    print_d(D, f"Vehicle density col is \"{col}\"")
    print_d(D, lengths)
    assert sorted(lengths) == lengths
    # TODO Better vehicle data format, should be meters.
    if col == "length":
        lengths = [l * 100 for l in lengths]

    def length_group(x):
        length = c.vehicle_data.loc[x, col]
        for i, l in enumerate(lengths):
            if length < l:
                return i

    return c.vehicle_data.groupby(by=length_group)


def noise_per_column(c: Config, col_names: List[str]):
    """Return (#outliers removed, stddev of remaining) for each column."""
    data = c.vehicle_data
    result = []
    for col_name in col_names:
        col = data[col_name]
        amount_before_removal = len(col)
        col = col[np.abs(stats.zscore(col)) < 3]
        amount_removed = amount_before_removal - len(col)
        result.append((amount_removed, np.std(col)))
    return result


def sample_vehicle(
        c: Config, group_index: int = None,
        noise_col_names: List[str] = noise_col_names, pd_row: bool = False
    ) -> Union[Vehicle, Tuple[Vehicle, pd.DataFrame]]:
    """Sample a vehicle from a c.vehicle_density group.

    Args:
        c: Config, config from which to load vehicle data and density info.
        init_group_index: int, sample from a given group index or all (None).
        noise_col_names: List[str], a list of columns to apply noise to.
        pd_row: bool, if true return a tuple of Vehicle and the corresponding
            row from the Pandas DataFrame, else return just a Vehicle.

    """
    # Select a group based on density, if none given.
    if group_index is None:
        rand = np.random.uniform()
        min, max = 0, c.vehicle_density[-1][0]
        print_d(D, f"rand = {rand}")
        print_d(D, f"min = {min}, max = {max}")
        running_fraction = 0
        print_d(D, f"vehicle density = {c.vehicle_density}")
        for i, (_, group_fraction) in enumerate(c.vehicle_density):
            running_fraction += group_fraction
            print(f"i = {i}, running_fraction = {running_fraction}")
            if rand < running_fraction:
                group_index = i
                break
    else: group_index = init_group_index
    print_d(D, f"group_index = {group_index}")

    # Sample a vehicle uniformly randomly from the group.
    groups_dict = {i: None for _ in range(len(c.vehicle_density))}
    print_d(D, groups_dict.items())
    for i, group in length_groups(c):
        print_d(D, f"i = {i}")
        groups_dict[i] = group
    group = groups_dict[group_index]
    print(f"group = {type(group)}")
    if group is None:
        print_w(f"Sampled group is None, resampling...")
        return sample_vehicle(c, init_group_index)
    sample = c.vehicle_data.loc[group.sample().index]

    # Add noise to the sample if requested.
    if c.perturb_stddev:
        for col_name, (_, stddev) in zip(
                noise_col_names, noise_per_column(c, noise_col_names)):
            print_d(D,
                f"col_name = {col_name}, stddev = {stddev:.2f},"
                + f"{c.perturb_stddev} x stddev = {c.perturb_stddev * stddev:.2f}")
            noise = np.random.normal(loc=0, scale=c.perturb_stddev * stddev)
            print_d(D, f"before =\n{sample[col_name]},\nnoise = {noise}")
            sample[col_name] = sample[col_name] + noise
            print_d(D, f"after =\n{sample[col_name]}")

    # Convert sample to Vehicle and return it.
    row = sample.iloc[0]
    kmph = row["speed"]
    axle_distances = axle_array_and_count(row["axle_distance"])
    num_axles = len(axle_distances) + 1
    total_kn = row["total_weight"]
    vehicle = Vehicle(
        kmph=kmph,
        kn_per_axle=total_kn / num_axles,
        # TODO: Fix units in database.
        axle_distances=np.array(axle_distances) / 100)
    return (vehicle, sample) if pd_row else vehicle
