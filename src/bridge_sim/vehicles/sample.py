"""Sample vehicles from the vehicles data."""

from timeit import default_timer as timer
from typing import List, Tuple, Union, NewType

import numpy as np
import pandas as pd
import scipy.stats as stats

from bridge_sim.model import Vehicle, Config
from bridge_sim.util import print_d, print_s, print_w

# Print debug information for this file.
# D: str = "vehicles.sample"
D: bool = False

# Column names of the vehicles data to add noise.
noise_col_names = []

VehicleData = NewType("VehicleData", pd.DataFrame)


def _vehicle_pdf_groups(vehicle_data: VehicleData, col: str, lengths: List[int]):
    """Vehicle data grouped by a maximum value per group."""
    print_d(D, f"Vehicle PDF column is {repr(col)}")
    print_d(D, str(lengths))
    assert sorted(lengths) == lengths
    # TODO Better vehicles data format, should be meters.
    if col == "length":
        lengths = [length * 100 for length in lengths]

    def group_by(x):
        length = vehicle_data.loc[x, col]
        for i, l in enumerate(lengths):
            if length < l:
                return i

    return vehicle_data.groupby(by=group_by)


def vehicle_pdf_groups(c: Config):
    """Return vehicles PDF groups, only ever calculated once."""
    if not hasattr(c, "_vehicle_pdf_groups"):
        start = timer()
        c._vehicle_pdf_groups = _vehicle_pdf_groups(
            c.vehicle_data, c.vehicle_pdf_col, list(map(lambda x: x[0], c.vehicle_pdf)),
        )
        print_s(f"Vehicle PDF groups loaded in {timer() - start}")
    return c._vehicle_pdf_groups


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
    c: Config,
    group_index: int = None,
    noise_col_names: List[str] = [],
    pd_row: bool = False,
) -> Union[Vehicle, Tuple[Vehicle, pd.DataFrame]]:
    """Sample a vehicles from a c.vehicle_density group.

    Args:
        c: Config, config from which to load vehicles data and density info.
        init_group_index: int, sample from a given group index or all (None).
        noise_col_names: List[str], a list of columns to apply noise to.
        pd_row: bool, if true return a tuple of Vehicle and the corresponding
            row from the Pandas DataFrame, else return just a Vehicle.

    """
    # Select a vehicles group randomly, if no group is specified.
    if group_index is None:
        rand = np.random.uniform()
        # print(rand)
        # print_d(D, f"Vehicle PDF = {c.vehicle_pdf}")
        # Group's are tuples of group maximum and percentage of all groups.
        min, max = 0, c.vehicle_pdf[-1][0]
        print_d(D, f"rand = {rand}")
        print_d(D, f"min = {min}, max = {max}")
        running_fraction = 0
        # Iterate through group percentage's until the randomly selected one.
        # print(c.vehicle_pdf)
        for i, (_, group_fraction) in enumerate(c.vehicle_pdf):
            running_fraction += group_fraction
            # print(f"running fraction = {running_fraction}")
            # print(f"i = {i}, running_fraction = {running_fraction}")
            if rand < running_fraction:
                group_index = i
                break
    # print(D, f"group_index = {group_index}")

    # Sample a vehicles uniformly randomly from the group.
    groups_dict = {i: None for i in range(len(c.vehicle_pdf))}
    print_d(D, groups_dict.items())
    for i, (_, group) in enumerate(vehicle_pdf_groups(c)):
        # print(D, f"i = {i}")
        groups_dict[i] = group
    group = groups_dict[group_index]

    # print(f"group = {type(group)}")
    if group is None:
        print_w(f"Sampled group is None, resampling...")
        return sample_vehicle(c, group_index)
    sample = c.vehicle_data.loc[group.sample().index]

    # Add noise to the sample if requested.
    if c.perturb_stddev:
        # print(f"perturb")
        for col_name, (_, stddev) in zip(
            noise_col_names, noise_per_column(c, noise_col_names)
        ):
            print_d(
                D,
                f"col_name = {col_name}, stddev = {stddev:.2f}"
                + f",{c.perturb_stddev} x stddev"
                + f" {c.perturb_stddev * stddev:.2f}",
            )
            noise = np.random.normal(loc=0, scale=c.perturb_stddev * stddev)
            print_d(D, f"before =\n{sample[col_name]},\nnoise = {noise}")
            sample[col_name] = sample[col_name] + noise
            print_d(D, f"after =\n{sample[col_name]}")

    # Convert sample to Vehicle and return it.
    row = sample.iloc[0]
    axle_distances = axle_array_and_count(row["axle_distance"])
    axle_weights = [
        a / 1e3 for a in axle_array_and_count(row["weight_per_axle"])
    ]  # From kN to N.
    # TODO: Fix units in database.
    # print(axle_distances)
    # print(axle_weights)
    # print(row["total_weight"])
    vehicle = Vehicle(
        kmph=40,
        load=axle_weights,
        axle_width=c.axle_width,
        axle_distances=np.array(axle_distances) / 100,
    )
    return (vehicle, sample) if pd_row else vehicle


col_names = [
    # "month",
    # "day",
    # "year",
    # "hour",
    # "min",
    # "sec",
    # "number",
    # "lane",
    # "type",
    # "speed",
    "number",
    "length",
    "total_weight",
    "weight_per_axle",
    "axle_distance",
]
index_col_name = "number"


def load_vehicle_data(vehicle_data_path) -> VehicleData:
    """Load the vehicles data from disk."""
    return pd.read_csv(vehicle_data_path, usecols=col_names, index_col=index_col_name)


def axle_array_and_count(axle_array_str: str) -> int:
    """Return an axle array of non zero values from a string."""
    axle_array_str = axle_array_str.replace("'", "").replace("[", "").replace("]", "")
    axle_array = list(map(float, axle_array_str.split(",")))
    return list(filter(lambda x: x != 0, axle_array))


def vehicle_density_stats(c: Config):
    """Human readable statistics on vehicles density."""
    num_bins = len(c.vehicle_density)
    groups = vehicle_pdf_groups(c)
    lengths_dict = {i: 0 for i in range(num_bins)}
    for i, group in groups:
        lengths_dict[i] = len(group)
    lengths_list = list(lengths_dict.values())
    return (
        "Vehicle density info:"
        + "\n"
        + "\n".join(
            [
                f"Vehicles < than {length} in {c.vehicle_density_col}:"
                + f" {lengths_dict[i]}"
                for i, length in enumerate(map(lambda x: x[0], c.vehicle_density))
            ]
        )
        + f"\nmean vehicles per group: {int(np.mean(lengths_list))}"
        + f"\nmin vehicles per group: {np.min(lengths_list)}"
        + f"\nmax vehicles per group: {np.max(lengths_list)}"
        + f"\nstd vehicles per group: {np.std(lengths_list):.2f}"
    )


def vehicle_data_noise_stats(c: Config, noise_col_names: List[str] = noise_col_names):
    """Human readable statistics on noise for vehicles data columns."""
    noise_data = noise_per_column(c, noise_col_names)
    data_len = len(c.vehicle_data[noise_col_names[0]])
    return (
        "Noise info:"
        + "\n"
        + "\n".join(
            [
                f'"{col_name}":'
                + f"\n\tremoved {noise_data[i][0]}"
                + f" or {noise_data[i][0] / data_len:.4f}% outliers"
                + f"\n\tstd. dev. of remaining is {noise_data[i][1]:.4f}"
                for i, col_name in enumerate(noise_col_names)
            ]
        )
    )
