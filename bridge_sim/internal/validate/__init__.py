import os

import pandas as pd

from bridge_sim.util import project_dir

# TNO provided files.
_meas_path = os.path.join(project_dir(), "data/validation/measurements_static_ZB.csv")
_displa_path = os.path.join(project_dir(), "data/validation/displasensors.txt")
_strain_path = os.path.join(project_dir(), "data/validation/strainsensors.txt")

_meas, _displa_sensors, _strain_sensors = None, None, None
if os.path.exists(_meas_path):
    _meas = pd.read_csv(_meas_path)
if os.path.exists(_displa_path):
    _displa_sensors = pd.read_csv(_displa_path, index_col=0)
if os.path.exists(_strain_path):
    _strain_sensors = pd.read_csv(_strain_path, index_col=0)


def _displa_sensor_xz(sensor_label):
    """X and z position of a displacement sensor in the experimental campaign."""
    sensor = _displa_sensors[_displa_sensors["label"] == sensor_label]
    sensor_x = sensor.iloc[0]["x"]
    sensor_z = sensor.iloc[0]["z"]
    return sensor_x, sensor_z


def _strain_sensor_xz(sensor_label):
    """X and z position of a strain sensor in the experimental campaign."""
    sensor = _strain_sensors[_strain_sensors["label"] == sensor_label]
    sensor_x = sensor.iloc[0]["x"]
    sensor_z = sensor.iloc[0]["z"]
    return sensor_x, sensor_z


def _truck1_x_pos():
    """X positions of Truck 1's front axle in the experimental campaign."""
    return sorted(set(_meas["xpostruck"]))
