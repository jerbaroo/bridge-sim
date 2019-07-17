"""Convert received A16 data to a more convenient CSV."""
import pandas as pd

from config import Config
from data.normal.a16 import a16_col_names


def raw_to_df_csv(c: Config, a16_raw_path: str, max_rows=10000):
    """Convert the raw A16 data to a csv written by Pandas."""
    with open(a16_raw_path) as f:
        rows = f.readlines()
    df = pd.DataFrame(columns=a16_col_names)
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
            df = pd.DataFrame(columns=a16_col_names)
            file_number += 1
    # Merge all saved CSV's into a single DataFrame.
    df_merged = pd.DataFrame(columns=a16_col_names)
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
