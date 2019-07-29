"""Load vehicle data from disk."""
import pandas as pd


# All column names of the vehicle data.
col_names = [
    "month", "day", "year", "hour", "min", "sec", "number", "lane", "type",
    "speed", "length", "total_weight", "weight_per_axle", "axle_distance"]


# Index column name of the vehicle data.
index_col_name = "number"


def load_vehicle_data(vehicle_data_path):
    """Load the vehicle data from disk."""
    return pd.read_csv(
        vehicle_data_path, usecols=col_names, index_col=index_col_name)
