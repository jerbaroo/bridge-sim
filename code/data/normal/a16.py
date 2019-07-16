"""
Manipulate and sample A16 load distribution data.
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats

from config import Config, bridge_705_config
from util import *


def load_a16_data(c: Config):
    """Load the A16 data from disk."""
    return pd.read_csv(
        c.a16_csv_path, usecols=c.a16_col_names, index_col="number")


def raw_to_df_csv(c: Config, a16_raw_path: str, max_rows=10000):
    """Convert the raw A16 data to a csv written by Pandas."""
    with open(a16_raw_path) as f:
        rows = f.readlines()
    df = pd.DataFrame(columns=c.a16_col_names)
    part_filepath = lambda num: c.a16_csv_path.replace(".", f"{num}.")
    # After max rows, or last row reached, save to csv.
    file_number = 0
    for i, row in enumerate(rows):
        row = row.split()
        values_left = len(row) - 12
        len_axle_weight = (values_left // 2) + 1
        len_axle_distance = values_left - len_axle_weight
        simple_cols = row[:12]
        axle_weights = row[12:12 + len_axle_weight]
        axle_distances = row[
            12 + len_axle_weight:12 + len_axle_weight + len_axle_distance]
        row = simple_cols + [axle_weights] + [axle_distances]
        df.loc[i % max_rows] = row
        if i != 0 and (i + 1) % 1000 == 0:
            print(f"{i + 1} rows converted")
        if len(df) == max_rows or i == len(rows) - 1:
            df.to_csv(part_filepath(num))
            print(f"Saved {len(df)} rows to {part_filepath(num)}")
            df = pd.DataFrame(columns=c.a16_col_names)
            file_number += 1
    # Merge all saved CSV's into a single DataFrame.
    df_merged = pd.DataFrame(columns=c.a16_col_names)
    for num in range(file_number):
        df = pd.read_csv(part_filepath)
        df_merged = df_merged.append(df, sort=False, ignore_index=True)
        print(f"Read file {part_filepath(num)}")
    df.set_index("number")
    df_merged.to_csv(out_filepath)
    print(f"Generated file out_filepath")
    # Delete temporary files.
    for num in range(c.a16_csv_path):
        os.remove(part_filepath(num))
        print(f"Deleted file {part_filepath(num)}")


def kde_sampler(data, print_=False):
    """A generator which returns samples from a KD estimate of the data."""
    kde = stats.gaussian_kde(data)
    i = 1
    while True:
        if print_ and i % 100 == 0:
            print(i, end=", ", flush=True)
        i += 1
        yield kde.resample(1)[0][0]


def plot_hist_and_kde(data, bins=None, density=True, title=None):
    """Plot a histogram and KDE of given data."""
    _, x, _ = plt.hist(data, bins=bins, density=density)
    kde = stats.gaussian_kde(data)
    plt.plot(x, kde(x))
    if title:
        plt.title(title)
    plt.show()


def plot_kde_and_kde_samples_hist(data, samples=5000):
    """Plot the KDE of given data and a histogram of samples from the KDE."""
    kde = stats.gaussian_kde(data)
    x = np.linspace(data.min(), data.max(), 100)
    plt.plot(x, kde(x))
    sampler = kde_sampler(data)
    plt.hist([next(sampler) for _ in range(samples)], bins=25, density=True)
    plt.show()


def plot_hist_and_kde_per_type(df):
    """Plot a histogram and KDE per vehicle type."""
    groups = df.groupby(
        by=lambda x: df.loc[x, "type"].replace("\"", "")[0])["total_weight"]
    plt.bar(range(len(groups)), groups.count())
    plt.xticks(plt.xticks()[0], [""] + [type_ for type_, _ in groups])
    plt.show()
    for type_, group in groups:
        plot_hist_and_kde(group, density=False, title=f"Type {type_}")


def num_axles(axle_distances: str) -> int:
    """The number of axles from an axle_distance array as a string."""
    distances = axle_distances.replace(
        "'", "").replace("[", "").replace("]", "")
    distances = list(
        filter(lambda x: x != 0, map(float, distances.split(","))))
    return len(distances)


def scatter_plots(c: Config, a16_data: pd.DataFrame, show=False, save=False):
    # Length against weight.
    plt.scatter(a16_data["total_weight"], a16_data["length"])
    plt.title("Vehicle length against weight on A16")
    plt.ylabel("length (m)")
    plt.xlabel("weight (kg)")
    if save:
        plt.savefig(os.path.join(c.images_dir, "a16-weight-vs-length"))
    if show: plt.show()
    if save or show: plt.close()

    # Length against number of axles.
    num_axles_column = a16_data["axle_distance"].apply(num_axles)
    plt.scatter(num_axles_column, a16_data["length"])
    plt.title("Vehicle length against number of axles on A16")
    plt.ylabel("length (m)")
    plt.xlabel("number of axles")
    if save:
        plt.savefig(os.path.join(c.images_dir, "a16-length-vs-num-axles"))
    if show: plt.show()
    if save or show: plt.close()

    # Weight against number of axles.
    plt.scatter(num_axles_column, a16_data["total_weight"])
    plt.title("Vehicle weight against number of axles on A16")
    plt.ylabel("weight (kg)")
    plt.xlabel("number of axles")
    if save:
        plt.savefig(os.path.join(c.images_dir, "a16-weight-vs-num-axles"))
    if show: plt.show()
    if save or show: plt.close()


if __name__ == "__main__":
    c = bridge_705_config()
    # raw_to_df_csv(c, "../data/a16-data/A16.dat")
    a16_data = load_a16_data(c)
    scatter_plots(c, a16_data, save=True)
    print(a16_data.loc[:10, :"total_weight"])
    print(a16_data.loc[:10, "weight_per_axle":])
    # plot_hist_and_kde(df["total_weight"], bins=100)
    # plot_kde_and_kde_samples_hist(df["total_weight"])
    # plot_hist_and_kde_per_type(df)
