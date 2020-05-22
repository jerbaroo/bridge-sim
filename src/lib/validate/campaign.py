import os

import pandas as pd

# TNO provided files.
meas_path = "data/validation/measurements_static_ZB.csv"
displa_path = "data/validation/displasensors.txt"
strain_path = "data/validation/strainsensors.txt"

meas, displa_sensors, strain_sensors = None, None, None
if os.path.exists(meas_path):
    meas = pd.read_csv(meas_path)
if os.path.exists(displa_path):
    displa_sensors = pd.read_csv( index_col=0)
if os.path.exists(strain_path):
    strain_sensors = pd.read_csv( index_col=0)


def truck_1_expt_xs():
    truck_xs_expt = set()
    for row in displa_sensors.itertuples():
        sensor_label = getattr(row, "label")
        responses = meas[meas["sensorlabel"] == sensor_label]
        for sensor_row in responses.itertuples():
            truck_xs_expt.add(getattr(sensor_row, "xpostruck"))
    return sorted(truck_xs_expt)


def displa_sensor_xz(sensor_label):
    """X and z position of a displacement sensor."""
    sensor = displa_sensors[displa_sensors["label"] == sensor_label]
    sensor_x = sensor.iloc[0]["x"]
    sensor_z = sensor.iloc[0]["z"]
    return sensor_x, sensor_z


def strain_sensor_xz(sensor_label):
    """X and z position of a strain sensor."""
    sensor = strain_sensors[strain_sensors["label"] == sensor_label]
    sensor_x = sensor.iloc[0]["x"]
    sensor_z = sensor.iloc[0]["z"]
    return sensor_x, sensor_z
