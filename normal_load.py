import os
from functools import reduce

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

A16_RAW_DATA = "a16-data/A16.dat"
A16_CSV_DATA = "a16-data/a16.csv"

COL_NAMES = [
    "month", "day", "year", "hour", "min", "sec", "number", "lane", "type",
    "speed", "length", "total_weight", "weight_per_axle", "axle_distance"
]


def raw_to_df_csv(in_filepath, out_filepath, columns=COL_NAMES,
                  max_rows=10000):
    """Convert the raw A16 data to a csv written by Pandas."""
    with open(in_filepath) as f:
        rows = f.readlines()
    df = pd.DataFrame(columns=columns)
    part_filepath = lambda num: out_filepath.replace(".", f"{num}.")
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
        if i != 0 and i % 999 == 0:
            print(f"{i + 1} rows converted")
        if len(df) == max_rows or i == len(rows) - 1:
            df.to_csv(part_filepath(num))
            print(f"Saved {len(df)} rows to {part_filepath(num)}")
            df = pd.DataFrame(columns=columns)
            file_number += 1
    # Merge all saved csv's into a single DataFrame.
    df_merged = pd.DataFrame(columns=columns)
    for num in range(file_number):
        df = pd.read_csv(part_filepath)
        df_merged = df_merged.append(df, sort=False, ignore_index=True)
        print(f"Read file {part_filepath}")
    df.set_index("number")
    df_merged.to_csv(out_filepath)
    # Delete temporary files.
    for num in range(file_number):
        os.remove(part_filepath(num))


if __name__ == "__main__":
    # raw_to_df_csv(A16_RAW_DATA, A16_CSV_DATA)
    df = pd.read_csv(A16_CSV_DATA, index_col=0)
    print(df.head)
    plt.hist(df["total_weight"])
    plt.show()
