import numpy as np
import pandas as pd

A16_RAW_DATA = "a16-data/A16.dat"
A16_CSV_DATA = "a16-data/a16.csv"

col_names = [
    "month", "day", "year", "hour", "min", "sec", "number", "lane", "type",
    "speed", "length", "total_weight", "weight_per_axle", "axle_distance"
]


def convert_to_pandas_csv(in_filepath, out_filepath):
    """Convert the raw A16 data to a csv written by Pandas."""
    with open(in_filepath) as f:
        rows = f.readlines()
    df = pd.DataFrame(columns=col_names)
    for i, row in enumerate(rows[:2]):
        row = row.split()
        values_left = len(row) - 12
        len_axle_weight = (values_left // 2) + 1
        len_axle_distance = values_left - len_axle_weight
        simple_cols = row[:12]
        axle_weights = row[12:12 + len_axle_weight]
        axle_distances = row[
            12 + len_axle_weight:12 + len_axle_weight + len_axle_distance]
        row = simple_cols + [axle_weights] + [axle_distances]
        df.loc[i] = row
    print(df.head)
    df.to_csv(out_filepath)


def read_csv_to_dataframe(filepath):
    """The A16 csv data at given filepath as a Pandas DataFrame."""
    df = pd.read_csv(filepath)
    df.set_index("number")
    return filepath


if __name__ == "__main__":
    convert_to_pandas_csv(A16_RAW_DATA, A16_CSV_DATA)
    df = read_csv_to_dataframe(A16_CSV_DATA)
    print(df.head)
