import os

import pandas as pd

from bridge_sim.util import project_dir

# TNO provided files.
meas_path = os.path.join(project_dir(), "data/validation/measurements_static_ZB.csv")
displa_path = os.path.join(project_dir(), "data/validation/displasensors.txt")
strain_path = os.path.join(project_dir(), "data/validation/strainsensors.txt")

if os.path.exists(meas_path):
    meas = pd.read_csv(meas_path)
if os.path.exists(displa_path):
    displa_sensors = pd.read_csv(displa_path, index_col=0)
if os.path.exists(strain_path):
    strain_sensors = pd.read_csv(strain_path, index_col=0)


def displa_sensor_xz(sensor_label):
    """X and z position of a displacement sensor in the experimental campaign."""
    sensor = displa_sensors[displa_sensors["label"] == sensor_label]
    sensor_x = sensor.iloc[0]["x"]
    sensor_z = sensor.iloc[0]["z"]
    return sensor_x, sensor_z


def strain_sensor_xz(sensor_label):
    """X and z position of a strain sensor in the experimental campaign."""
    sensor = strain_sensors[strain_sensors["label"] == sensor_label]
    sensor_x = sensor.iloc[0]["x"]
    sensor_z = sensor.iloc[0]["z"]
    return sensor_x, sensor_z


def truck1_x_pos():
    """X positions of Truck 1's front axle in the experimental campaign."""
    return sorted(set(meas["xpostruck"]))
