"""
Manipulate and sample A16 load distribution data.
"""
import os
from typing import List

import pandas as pd

from util import *


a16_col_names = [
    "month", "day", "year", "hour", "min", "sec", "number", "lane", "type",
    "speed", "length", "total_weight", "weight_per_axle", "axle_distance"]


def load_a16_data():
    """Load the A16 data from disk."""
    return pd.read_csv(
         "../data/a16-data/A16.csv", usecols=a16_col_names, index_col="number")


def length_groups(data: pd.DataFrame, lengths: List[int]):
    """Return the data grouped by maximum lengths."""
    assert sorted(lengths) == lengths
    # TODO Better A16 data format, should be meters.
    lengths = [l * 100 for l in lengths]

    def length_group(x):
        length = data.loc[x, "length"]
        for i, l in enumerate(lengths):
            if length < l:
                return i

    return data.groupby(by=length_group)


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
