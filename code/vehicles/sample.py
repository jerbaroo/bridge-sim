"""Sample vehicles from the vehicle data."""
from typing import List, Optional

from config import Config
from model import *
from util import *
from vehicles import axle_array_and_count


# Column names of the vehicle data to add noise.
noise_col_names = ["speed", "length", "total_weight"]


def length_groups(c: Config, col: Optional[str]=None, lengths: List[int]=None):
    """Return vehicle data grouped by a maximum value per group."""
    if col is None:
        col = c.vehicle_density_col
    if lengths is None:
        lengths = list(map(lambda x: x[0], c.vehicle_density))
    print_d(f"Vehicle density col is \"{col}\"")
    print_d(lengths)
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
        c: Config, noise_stddevs: float=0.1, init_group_index: int=None,
        noise_col_names: List[str]=noise_col_names, pd_row: bool=False
    ) -> Vehicle:
    """Return a sample vehicle from a c.vehicle_density group.

    Args:
        c: Config, config from which to load vehicle data and density info.
        noise_std: float, standard deviation of noise added per column.
        init_group_index: int, sample from a given group index or all (None).
        noise_col_names: List[str], a list of columns to apply noise to.

    """
    # Select a group based on density, if none given.
    if init_group_index is None:
        rand = np.random.uniform()
        min, max = 0, c.vehicle_density[-1][0]
        print_d(f"rand = {rand}")
        print_d(f"min = {min}, max = {max}")
        running_fraction = 0
        print_d(f"vehicle density = {c.vehicle_density}")
        for i, (_, group_fraction) in enumerate(c.vehicle_density):
            running_fraction += group_fraction
            print(f"i = {i}, running_fraction = {running_fraction}")
            if rand < running_fraction:
                group_index = i
                break
    else: group_index = init_group_index
    print_d(f"group_index = {group_index}")

    # Sample a vehicle uniformly randomly from the group.
    groups_dict = {i: None for _ in range(len(c.vehicle_density))}
    print_d(groups_dict.items())
    for i, group in length_groups(c):
        print_d(f"i = {i}")
        groups_dict[i] = group
    group = groups_dict[group_index]
    print(f"group = {type(group)}")
    if group is None:
        print_w(f"Sampled group is None, resampling...")
        return sample_vehicle(c, noise_stddevs, init_group_index)
    sample = c.vehicle_data.loc[group.sample().index]

    # Add noise to the sample if requested.
    if noise_stddevs:
        for col_name, (_, stddev) in zip(
                noise_col_names, noise_per_column(c, noise_col_names)):
            print_d(
                f"col_name = {col_name}, stddev = {stddev:.2f},"
                + f"{noise_stddevs} x stddev = {noise_stddevs * stddev:.2f}")
            noise = np.random.normal(loc=0, scale=noise_stddevs * stddev)
            print_d(f"before =\n{sample[col_name]},\nnoise = {noise}")
            sample[col_name] = sample[col_name] + noise
            print_d(f"after =\n{sample[col_name]}")

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
