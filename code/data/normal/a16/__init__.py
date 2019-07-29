"""Manipulate and sample vehicle information."""
import os
from typing import List

import numpy as np
import pandas as pd
from scipy import stats

from config import Config
from model import *
from util import *


# All column names of the vehicle data.
col_names = [
    "month", "day", "year", "hour", "min", "sec", "number", "lane", "type",
    "speed", "length", "total_weight", "weight_per_axle", "axle_distance"]


# Column names of the vehicle data which are floats.
float_col_names = ["speed", "length", "total_weight"]


def load_a16_data():
    """Load the vehicle data from disk."""
    return pd.read_csv(
         "../data/a16-data/A16.csv", usecols=col_names, index_col="number")


def length_groups(c: Config, col=None, lengths: List[int]=None):
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

    return c.vehicle_data[col].groupby(by=length_group)


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


def vehicle_data_noise_stats(c: Config, col_names=float_col_names):
    """Human readable statistics on noise for vehicle data columns."""
    noise_data = noise_per_column(c, col_names)
    data_len = len(c.vehicle_data[col_names[0]])
    return (
        "Noise info:"
        + "\n" + "\n".join([
            f"\"{col_name}\":"
            + f"\n\tremoved {noise_data[i][0]}"
            + f" or {noise_data[i][0] / data_len:.4f}% outliers"
            + f"\n\tstd. dev. of remaining is {noise_data[i][1]:.4f}"
            for i, col_name in enumerate(col_names)]))


def noise_per_column(c: Config, col_names):
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


def sample_vehicle(c: Config, noise=1) -> Vehicle:
    """Return a sample vehicle from a c.vehicle_density group."""
    rand = np.random.uniform()
    min, max = 0, c.vehicle_density[-1][0]
    print_d(f"rand = {rand}")
    print_d(f"min = {min}, max = {max}")
    running_fraction = 0
    print_d(f"vehicle density = {c.vehicle_density}")
    for i, (_, percent) in enumerate(c.vehicle_density):
        running_fraction += percent / 100
        print(f"i = {i}, running_fraction = {running_fraction}")
        if rand < running_fraction:
            group = i
            print_d(f"Group is {i}")
            break
    groups_dict = {i: None for _ in range(len(c.vehicle_density))}
    print_d(groups_dict.items())
    for i, group in length_groups(c):
        print_d(f"i = {i}")
        groups_dict[i] = group
    group = groups_dict[i]
    print(f"group = {type(group)}")
    if group is None:
        print_w(f"Sampled group is None, resampling...")
    sample = c.vehicle_data.loc[group.sample().index]
    return sample
    

# def gen_hist_per_type(c: Config, a16_data: DataFrame):
#     """Plot a histogram per vehicle type."""
#     groups = a16_data.groupby(
#         by=lambda x: a16_data.loc[x, "type"].replace("\"", "")[0]
#     )["total_weight"]
#     plt.bar(range(len(groups)), groups.count())
#     plt.xticks(plt.xticks()[0], [""] + [type_ for type_, _ in groups])
#     plt.savefig(os.path.join(c.images_dir, "a16-vehicle-types"))
#     plt.close()
#     for type_, group in groups:
#         if type_ == "*":
#             type_ = "all"
#         plot_hist(
#             group, density=False, title=f"Type {type_}",
#             save=os.path.join(c.images_dir, f"a16-vehicle-type-{type_}"))


# def gen_hists(c: Config, a16_data: DataFrame):
#     """Generate histograms of weight and vehicle type."""
#     # Histogram of weight distribution.
#     plot_hist(
#         a16_data["total_weight"], bins=100, title="Vehicle weight on A16",
#         ylabel="density", xlabel="weight (kg)",
#         save=os.path.join(c.images_dir, "a16-weight-distribution"))
#     # Histogram of weight distribution and KDE.
#     plot_hist(
#         a16_data["total_weight"], bins=100, kde=True,
#         title="Vehicle weight and KDE on A16", ylabel="density",
#         xlabel="weight (kg)",
#         save=os.path.join(c.images_dir, "a16-weight-distribution-and-kde"))
#     # KDE of weight and a histogram of samples from the KDE.
#     plot_kde_and_kde_samples_hist(
#         a16_data["total_weight"], title="Vehicle weight on A16",
#         ylabel="density", xlabel="weight (kg)",
#         save=os.path.join(c.images_dir, "a16-weight-kde-and-samples"))
#     gen_hist_per_type(c, a16_data)


# def axle_array_and_count(axle_array_str: str) -> int:
#     """Return an axle array and count of non zero values from a string."""
#     axle_array_str = axle_array_str.replace(
#         "'", "").replace("[", "").replace("]", "")
#     axle_array = list(map(float, axle_array_str.split(",")))
#     count_non_zero = len(list(filter(lambda x: x != 0, axle_array)))
#     return axle_array, count_non_zero


# def gen_scatter_plots(c: Config, a16_data: DataFrame):
#     """Generate scatter plots of the A16 data."""
#     # Length against weight.
#     plt.scatter(a16_data["total_weight"], a16_data["length"], s=10, alpha=0.1)
#     plt.title("Vehicle length against weight on A16")
#     plt.ylabel("length (m)")
#     plt.xlabel("weight (kg)")
#     plt.savefig(os.path.join(c.images_dir, "a16-weight-vs-length"))
#     plt.close()

#     # Length against number of axles.
#     num_axles_column = a16_data["weight_per_axle"].apply(
#         lambda s: axle_array_and_count(s)[1])
#     plt.scatter(num_axles_column, a16_data["length"], s=10, alpha=0.1)
#     plt.title("Vehicle length against number of axles on A16")
#     plt.ylabel("length (m)")
#     plt.xlabel("number of axles")
#     plt.savefig(os.path.join(c.images_dir, "a16-length-vs-num-axles"))
#     plt.close()

#     # Weight against number of axles.
#     plt.scatter(num_axles_column, a16_data["total_weight"], s=10, alpha=0.1)
#     plt.title("Vehicle weight against number of axles on A16")
#     plt.ylabel("weight (kg)")
#     plt.xlabel("number of axles")
#     plt.savefig(os.path.join(c.images_dir, "a16-weight-vs-num-axles"))
#     plt.close()

#     # Fair amount of load per axle.
#     axle_weights_and_counts = a16_data["weight_per_axle"].apply(
#         axle_array_and_count)
#     axle_nums = []
#     axle_fair_amounts = []
#     for axle_weights, num_axles in axle_weights_and_counts:
#         total_weight = sum(axle_weights)
#         for i in range(len(axle_weights)):
#             if axle_weights[i] != 0:
#                 axle_nums.append(i + 1)
#                 axle_fair_amounts.append(
#                     (axle_weights[i] / total_weight) * num_axles)
#     plt.scatter(axle_nums, axle_fair_amounts, s=10, alpha=0.1)
#     plt.title("Weight distribution per axle on A16")
#     plt.ylabel("(weight / total weight) x #axles")
#     plt.xlabel("axle position")
#     plt.savefig(os.path.join(c.images_dir, "a16-fair-amount-per-axle"))
