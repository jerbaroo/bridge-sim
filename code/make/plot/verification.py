"""Verification plots."""
import glob
import itertools
import math
import os
from collections import defaultdict
from itertools import chain
from timeit import default_timer as timer
from typing import List, Optional, Tuple

import matplotlib.cm as cm
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression

from classify.data.responses import (
    responses_to_traffic_array,
    responses_to_loads,
    responses_to_loads_,
    responses_to_vehicles_,
)
from classify.scenario.bridge import HealthyBridge, PierDispBridge
from classify.vehicle import wagen1
from config import Config
from fem.build import det_nodes, det_shells
from fem.model import Shell
from fem.params import SimParams
from fem.responses import Responses, load_fem_responses
from fem.run.build.elements import shells_by_id
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_config
from model.load import DisplacementCtrl, MvVehicle, PointLoad
from model.response import ResponseType
from plot import plt
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck
from util import clean_generated, flatten, print_i, print_w, read_csv, round_m, safe_str

# Positions of truck front axle.
truck_front_x = np.arange(1, 116.1, 1)

# TNO provided files.
meas = pd.read_csv("data/verification/measurements_static_ZB.csv")
diana = pd.read_csv("data/verification/modelpredictions_april2019.csv")
displa_sensors = pd.read_csv("data/verification/displasensors.txt")
strain_sensors = pd.read_csv("data/verification/strainsensors.txt")


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


# Interpolation function for each sensor position.
diana_interp_funcs = dict()


def diana_response(sensor_label: str, truck_x: float):
    """Strain or displacement from Diana for a sensor and truck position."""
    if sensor_label not in diana_interp_funcs:
        all_sensors = diana[diana["sensorlabel"] == sensor_label]
        diana_interp_funcs[sensor_label] = interp1d(
            all_sensors["xpostruck"], all_sensors["infline1"]
        )
    return diana_interp_funcs[sensor_label](truck_x)


def per_sensor_plots(
    c: Config,
    rows: int = 5,
    cols: int = 2,
    individual_sensors: List[str] = ["T4", "U3"],
):
    """Compare the bridge 705 measurement campaign to Diana and OpenSees."""
    size = 25  # Size of scatter plot points.

    ####################
    ###### Strain ######
    ####################

    # All strain measurements from TNO sensors (label start with "T"), except
    # ignore sensor T0 since no diana predictions are available.
    tno_strain_meas = meas.loc[meas["sensorlabel"].str.startswith("T")]
    tno_strain_meas = tno_strain_meas.loc[tno_strain_meas["sensorlabel"] != "T0"]

    # Sort by sensor number and setup groupby sensor label.
    tno_strain_meas["sort"] = tno_strain_meas["sensorlabel"].apply(lambda x: int(x[1:]))
    tno_strain_meas = tno_strain_meas.sort_values(by=["sort"])
    strain_groupby = tno_strain_meas.groupby("sensorlabel", sort=False)

    # Find the min and max responses.
    amin, amax = np.inf, -np.inf
    for sensor_label, meas_group in strain_groupby:
        diana_group = diana[diana["sensorlabel"] == sensor_label]
        responses = (
            diana_group["infline1"].to_list() + meas_group["inflinedata"].to_list()
        )
        amin = min(amin, np.amin(responses))
        amax = max(amax, np.amax(responses))
    amin *= 1.1
    amax *= 1.1

    def plot(sensor_label, meas_group):
        # Plot Diana predictions for the given sensor.
        diana_group = diana[diana["sensorlabel"] == sensor_label]
        plt.scatter(
            diana_group["xpostruck"],
            diana_group["infline1"],
            marker="o",
            s=size,
            label="Diana",
        )

        # Plot measured values against truck position.
        plt.scatter(
            meas_group["xpostruck"],
            meas_group["inflinedata"],
            marker="o",
            s=size,
            label="measurement",
        )

        plt.legend()
        plt.title(f"Strain at {sensor_label}")
        plt.xlabel("x position of truck front axle (m)")
        plt.ylabel("strain (m/m)")
        plt.ylim((amin, amax))

    # Create a subplot for each strain sensor.
    plot_i, subplot_i = 0, 0
    for i, (sensor_label, meas_group) in enumerate(strain_groupby):
        plt.subplot(rows, cols, subplot_i + 1)
        plot(sensor_label, meas_group)
        if subplot_i + 1 == rows * cols or i == len(strain_groupby) - 1:
            plt.savefig(
                c.get_image_path(
                    dirname="validation", filename=f"strain-{plot_i}", acc=False,
                )
            )
            plt.close()
            plot_i += 1
            subplot_i = 0
        else:
            subplot_i += 1

    # Create any plots for individual sensors.
    for sensor_label, meas_group in strain_groupby:
        if sensor_label in individual_sensors:
            plot(sensor_label, meas_group)
            plt.savefig(
                c.get_image_path(
                    dirname="validation",
                    filename=f"strain-sensor-{sensor_label}",
                    acc=False,
                )
            )
            plt.close()

    ##########################
    ###### Displacement ######
    ##########################

    # All displacement measurements.
    displa_meas = meas.loc[meas["sensortype"] == "displacements"]

    # Sort by sensor number and setup groupby sensor label. Also silence a
    # Pandas warning.
    displa_meas["sort"] = displa_meas["sensorlabel"].apply(lambda x: int(x[1:]))
    displa_meas = displa_meas.sort_values(by=["sort"])
    displa_groupby = displa_meas.groupby("sensorlabel", sort=False)
    displa_sensor_labels = [sensor_label for sensor_label, _ in displa_groupby]
    displa_sensor_xzs = list(map(displa_sensor_xz, displa_sensor_labels))

    # Find the min and max responses.
    amin, amax = np.inf, -np.inf
    for sensor_label, meas_group in displa_groupby:
        diana_group = diana[diana["sensorlabel"] == sensor_label]
        responses = (
            diana_group["infline1"].to_list() + meas_group["inflinedata"].to_list()
        )
        amin = min(amin, np.amin(responses))
        amax = max(amax, np.amax(responses))
    amin *= 1.1
    amax *= 1.1

    # Calculate displacement with OpenSees via direct simulation.
    os_displacement = (
        responses_to_vehicles_(
            c=c,
            mv_vehicles=[wagen1],
            times=[wagen1.time_at(x=x, bridge=c.bridge) for x in truck_front_x],
            response_type=ResponseType.YTranslation,
            bridge_scenario=HealthyBridge(),
            points=[
                Point(x=sensor_x, y=0, z=sensor_z)
                for sensor_x, sensor_z in displa_sensor_xzs
            ],
            sim_runner=OSRunner(c),
        ).T
        * 1000
    )
    amin = min(amin, np.amin(os_displacement))
    amax = max(amax, np.amax(os_displacement))

    def plot(i, sensor_label, meas_group):
        # Plot Diana predictions for the given sensor.
        diana_group = diana[diana["sensorlabel"] == sensor_label]
        plt.scatter(
            diana_group["xpostruck"], diana_group["infline1"], s=size, label="Diana",
        )

        # Plot values from OpenSees.
        plt.scatter(truck_front_x, os_displacement[i], s=size, label="OpenSees")

        # Plot measured values sorted by truck position.
        plt.scatter(
            meas_group["xpostruck"],
            meas_group["inflinedata"],
            s=size,
            label=f"Sensor {sensor_label}",
        )

        plt.legend()
        sensor_x, sensor_z = displa_sensor_xzs[i]
        plt.title(
            f"Displacement at sensor {sensor_label}, x = {sensor_x:.3f}, z = {sensor_z:.3f}"
        )
        plt.xlabel("x position of truck front axle (m)")
        plt.ylabel("displacement (mm)")
        plt.ylim((amin, amax))

    # Create a subplot for each displacement sensor.
    plot_i, subplot_i = 0, 0
    for i, (sensor_label, meas_group) in enumerate(displa_groupby):
        plt.subplot(rows, cols, subplot_i + 1)
        plot(i, sensor_label, meas_group)
        if subplot_i + 1 == rows * cols or i == len(displa_groupby) - 1:
            plt.savefig(
                c.get_image_path(
                    dirname="validation", filename=f"displa-{plot_i}", acc=False,
                )
            )
            plt.close()
            plot_i += 1
            subplot_i = 0
        else:
            subplot_i += 1

    # Create any plots for individual sensors.
    for i, (sensor_label, meas_group) in enumerate(displa_groupby):
        if sensor_label in individual_sensors:
            plot(i, sensor_label, meas_group)
            plt.savefig(
                c.get_image_path(
                    dirname="validation",
                    filename=f"displa-sensor-{sensor_label}",
                    acc=False,
                )
            )
            plt.close()


def r2_plots(c: Config):
    """R² plots for displacement and strain."""

    ##########################
    ###### Displacement ######
    ##########################

    # Sensor label, truck x position, and response value.
    displa_meas: List[Tuple[str, float, float]] = []
    displa_diana: List[Tuple[str, float, float]] = []
    # List of sensor labels and positions in the same order as above.
    sensors = []
    # All truck positions used in measurements.
    truck_xs_meas = set()

    # For each sensor and truck x position plot the recorded measurement and
    # Diana response.
    for row in displa_sensors.itertuples():
        sensor_label = getattr(row, "label")
        x, z = displa_sensor_xz(sensor_label)
        sensors.append((sensor_label, x, z))
        responses = meas[meas["sensorlabel"] == sensor_label]
        for sensor_row in responses.itertuples():
            truck_x = getattr(sensor_row, "xpostruck")
            truck_xs_meas.add(truck_x)
            response = getattr(sensor_row, "inflinedata")
            displa_meas.append((sensor_label, truck_x, response))
            displa_diana.append(
                diana_response(sensor_label=sensor_label, truck_x=truck_x)
            )
    truck_xs_meas = sorted(truck_xs_meas)

    # Displacement in OpenSees via direct simulation (measurement points).
    displa_os_meas = (
        responses_to_vehicles_(
            c=c,
            mv_vehicles=[wagen1],
            times=[wagen1.time_at(x=x, bridge=c.bridge) for x in truck_xs_meas],
            response_type=ResponseType.YTranslation,
            bridge_scenario=HealthyBridge(),
            points=[
                Point(x=sensor_x, y=0, z=sensor_z) for _, sensor_x, sensor_z in sensors
            ],
            sim_runner=OSRunner(c),
        )
        * 1000
    )

    def get_os_meas(sensor_label: str, truck_x: float):
        for i, truck_x_ in enumerate(truck_xs_meas):
            if truck_x_ == truck_x:
                for j, (sensor_label_, _, _) in enumerate(sensors):
                    if sensor_label_ == sensor_label:
                        return displa_os_meas[i][j]
        raise ValueError(
            f"No match. sensor_label = {sensor_label}, truck_x = {truck_x}"
        )

    # Subplot: Diana against measurements.
    plt.portrait()
    plt.subplot(3, 1, 1)
    x = list(map(lambda x: x[2], displa_meas))
    y = [
        diana_response(sensor_label=sensor_label, truck_x=truck_x)
        for sensor_label, truck_x, _ in displa_meas
    ]
    plt.scatter(x, y)
    regressor = LinearRegression().fit(np.matrix(x).T, y)
    y_pred = regressor.predict(np.matrix(x).T)
    score = regressor.score(np.matrix(x).T, y)
    plt.plot(x, y_pred, color="red", label=f"R² = {score:.3f}")
    plt.legend()
    plt.title("Displacement: Diana vs. measurements")
    plt.xlabel("Displacement measurement (mm)")
    plt.ylabel("Displacement in Diana (mm)")

    # Subplot: OpenSees against measurements.
    plt.subplot(3, 1, 2)
    x = list(map(lambda x: x[2], displa_meas))
    y = [
        get_os_meas(sensor_label=sensor_label, truck_x=truck_x)
        for sensor_label, truck_x, _ in displa_meas
    ]
    plt.scatter(x, y)
    regressor = LinearRegression().fit(np.matrix(x).T, y)
    y_pred = regressor.predict(np.matrix(x).T)
    score = regressor.score(np.matrix(x).T, y)
    plt.plot(x, y_pred, color="red", label=f"R² = {score:.3f}")
    plt.legend()
    plt.title("Displacement: OpenSees vs. measurements")
    plt.xlabel("Displacement measurement (mm)")
    plt.ylabel("Displacement in OpenSees (mm)")

    # Subplot: OpenSees against Diana.
    plt.subplot(3, 1, 3)
    x = [
        diana_response(sensor_label=sensor_label, truck_x=truck_x)
        for sensor_label, truck_x, _ in displa_meas
    ]
    y = [
        get_os_meas(sensor_label=sensor_label, truck_x=truck_x)
        for sensor_label, truck_x, _ in displa_meas
    ]
    plt.scatter(x, y)
    regressor = LinearRegression().fit(np.matrix(x).T, y)
    y_pred = regressor.predict(np.matrix(x).T)
    score = regressor.score(np.matrix(x).T, y)
    plt.plot(x, y_pred, color="red", label=f"R² = {score:.3f}")
    plt.legend()
    plt.title("Displacement: OpenSees vs. Diana")
    plt.xlabel("Displacement in Diana (mm)")
    plt.ylabel("Displacement in OpenSees (mm)")

    plt.savefig(c.get_image_path("validation/regression", "regression-displa.pdf"))
    plt.close()

    ####################
    ###### Strain ######
    ####################

    # Sensor label, truck x position, and response value.
    strain_meas: List[Tuple[str, float, float]] = []
    strain_diana: List[Tuple[str, float, float]] = []
    # List of sensor labels and positions in the same order as above.
    sensors = []

    # For each sensor and truck x position record measurment and Diana response.
    count_nan = 0
    for row in strain_sensors.itertuples():
        sensor_label = getattr(row, "label")
        x, z = strain_sensor_xz(sensor_label)
        sensors.append((sensor_label, x, z))
        responses = meas[meas["sensorlabel"] == sensor_label]
        for sensor_row in responses.itertuples():
            truck_x = getattr(sensor_row, "xpostruck")
            response = getattr(sensor_row, "inflinedata")
            if not np.isnan(response):
                strain_meas.append((sensor_label, truck_x, response))
                strain_diana.append(
                    diana_response(sensor_label=sensor_label, truck_x=truck_x)
                )
            else:
                count_nan += 1

    print_i(f"Count nan = {count_nan}")

    # Strain in OpenSees via direct simulation (measurement points).
    strain_os_meas = responses_to_vehicles_(
        c=c,
        mv_vehicles=[wagen1],
        times=[wagen1.time_at(x=x, bridge=c.bridge) for x in truck_xs_meas],
        response_type=ResponseType.Strain,
        bridge_scenario=HealthyBridge(),
        points=[
            Point(x=sensor_x, y=0, z=sensor_z) for _, sensor_x, sensor_z in sensors
        ],
        sim_runner=OSRunner(c),
    )

    def get_os_meas(sensor_label: str, truck_x: float):
        for i, truck_x_ in enumerate(truck_xs_meas):
            if truck_x_ == truck_x:
                for j, (sensor_label_, _, _) in enumerate(sensors):
                    if sensor_label_ == sensor_label:
                        return strain_os_meas[i][j]
        raise ValueError(
            f"No match. sensor_label = {sensor_label}, truck_x = {truck_x}"
        )

    # Subplot: Diana against measurements.
    plt.subplot(3, 1, 1)
    x = list(map(lambda x: x[2], strain_meas))
    y = [
        diana_response(sensor_label=sensor_label, truck_x=truck_x)
        for sensor_label, truck_x, _ in strain_meas
    ]
    plt.scatter(x, y)
    regressor = LinearRegression().fit(np.matrix(x).T, y)
    y_pred = regressor.predict(np.matrix(x).T)
    score = regressor.score(np.matrix(x).T, y)
    plt.plot(x, y_pred, color="red", label=f"R² = {score:.3f}")
    plt.legend()
    plt.title("Strain: Diana vs. measurements")
    plt.xlabel("Strain measurement (m/m)")
    plt.ylabel("Strain in Diana (m/m)")

    # Subplot: OpenSees against measurements.
    plt.subplot(3, 1, 2)
    x = list(map(lambda x: x[2], strain_meas))
    y = np.array(
        [
            get_os_meas(sensor_label=sensor_label, truck_x=truck_x)
            for sensor_label, truck_x, _ in strain_meas
        ]
    )
    plt.scatter(x, y)
    regressor = LinearRegression().fit(np.matrix(x).T, y)
    y_pred = regressor.predict(np.matrix(x).T)
    score = regressor.score(np.matrix(x).T, y)
    plt.plot(x, y_pred, color="red", label=f"R² = {score:.3f}")
    plt.legend()
    plt.title("Strain: OpenSees vs. measurements")
    plt.xlabel("Strain measurement (m/m)")
    plt.ylabel("Strain in OpenSees (m/m)")

    # Subplot: OpenSees against Diana.
    plt.subplot(3, 1, 3)
    x = [
        diana_response(sensor_label=sensor_label, truck_x=truck_x)
        for sensor_label, truck_x, _ in strain_meas
    ]
    y = [
        get_os_meas(sensor_label=sensor_label, truck_x=truck_x)
        for sensor_label, truck_x, _ in strain_meas
    ]
    plt.scatter(x, y)
    regressor = LinearRegression().fit(np.matrix(x).T, y)
    y_pred = regressor.predict(np.matrix(x).T)
    score = regressor.score(np.matrix(x).T, y)
    plt.plot(x, y_pred, color="red", label=f"R² = {score:.3f}")
    plt.legend()
    plt.title("Strain: OpenSees vs. Diana")
    plt.xlabel("Strain in Diana (m/m)")
    plt.ylabel("Strain in OpenSees (m/m)")

    plt.savefig(c.get_image_path("validation/regression", "regression-strain.pdf"))


def make_convergence_data(c: Config):
    """Make convergence data file, increasing mesh density per simulation."""
    load_point = Point(x=35, y=0, z=9.65)
    bridge = bridge_705_3d()
    fem_params = SimParams(
        ploads=[
            PointLoad(
                x_frac=bridge.x_frac(load_point.x),
                z_frac=bridge.z_frac(load_point.z),
                kn=100,
            )
        ],
        response_types=[ResponseType.YTranslation, ResponseType.Strain],
    )
    max_shell_len = 10

    def bridge_overload(**kwargs):
        return bridge_705_3d(
            name=f"Bridge 705",
            accuracy="convergence",
            base_mesh_deck_max_x=max_shell_len,
            base_mesh_deck_max_z=max_shell_len,
            base_mesh_pier_max_long=max_shell_len,
            **kwargs,
        )

    # A grid of points over which to calculate the mean response. The reason for
    # this is because if the number of nodes increases, as model size increases,
    # then there will be an increase in nodes where responses are large, thus
    # model size will influence the mean/min calculation.
    grid = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, int(c.bridge.length)),
            np.linspace(c.bridge.z_min, c.bridge.z_max, int(c.bridge.width)),
        )
    ]

    # Write the header information to the results file.
    c = bridge_705_config(bridge_overload)
    path = c.get_image_path("convergence", "convergence_results", bridge=False)
    with open(path + ".txt", "w") as f:
        f.write(
            "xload,zload,max_mesh,decknodes,piernodes,time"
            + ",min_d,max_d,mean_d,min_s,max_s,mean_s,shell-size,deck-size,pier-size"
        )

    max_shell_lens = list(np.arange(10, 2 - 0.00001, -1))
    max_shell_lens += list(np.arange(1.9, 1 - 0.00001, -0.1))
    max_shell_lens += list(np.arange(0.9, 0.1 - 0.00001, -0.01))
    max_shell_lens = list(map(round_m, max_shell_lens))

    for max_shell_len in max_shell_lens:

        print(f"max shell len = {max_shell_len}")

        with open(path + ".txt", "a") as f:
            f.write(f"\n{load_point.x}, {load_point.z}, {max_shell_len}")

        c = bridge_705_config(bridge_overload)
        try:
            # Start timing and run the simulation.
            start = timer()
            displacements = load_fem_responses(
                c=c,
                sim_params=fem_params,
                response_type=ResponseType.YTranslation,
                sim_runner=OSRunner(c),
                run=True,
            )
            end = timer()

            # Determine amount of nodes.
            nodes = det_nodes(fem_params.bridge_nodes)
            deck_nodes = len([n for n in nodes if n.deck])
            pier_nodes = len([n for n in nodes if not n.deck])

            # Determine shell sizes for the deck, pier and whole bridge.
            shells = det_shells(fem_params.bridge_shells)
            avg_deck_size = np.mean([s.area() for s in shells if not s.pier])
            avg_pier_size = np.mean([s.area() for s in shells if s.pier])
            avg_shell_size = np.mean([s.area() for s in shells])

            # TODO: Remove to deck interpolation test.
            for x in displacements.xs:
                if 0 in displacements.zs[x]:
                    for z in displacements.zs[x][0]:
                        og = displacements.responses[0][x][0][z].value
                        ip = displacements.at_deck(Point(x=x, y=0, z=z), interp=True)
                        assert np.isclose(og, ip)

            # Determine min, max and mean displacements.
            all_displacements = list(displacements.values())
            grid_displacements = np.array([displacements.at_deck(point, interp=True) for point in grid])
            min_d = np.min(grid_displacements)
            max_d = np.max(all_displacements)
            mean_d = np.mean(grid_displacements)
            assert len(min_d) == 1; assert len(mean_d) == 1
            min_d = min_d[0]; mean_d = mean_d[0]

            strains = load_fem_responses(
                c=c,
                sim_params=fem_params,
                response_type=ResponseType.Strain,
                sim_runner=OSRunner(c),
            )
            all_strains = list(strains.values())
            grid_strains = np.array([strains.at_deck(point, interp=True) for point in grid])
            min_s = np.min(grid_strains)
            max_s = np.max(all_strains)
            mean_s = np.mean(grid_strains)
            try:
                min_s = min_s[0]
            except:
                pass
            assert len(mean_s) == 1
            mean_s = mean_s[0]

            # Write results for this simulation to disk.
            with open(path + ".txt", "a") as f:
                f.write(
                    f", {deck_nodes}, {pier_nodes}, {end - start}"
                    f", {min_d}, {max_d}, {mean_d}"
                    f", {min_s}, {max_s}, {mean_s}"
                    f", {avg_shell_size}, {avg_deck_size}, {avg_pier_size}"
                )

        except ValueError as e:
            if "No responses found" in str(e):
                print_i("Simulation failed. Time to plot results")
            else:
                raise e


def plot_convergence(c: Config):
    """Plot convergence as model size is increased for multiple machines.

    Loads files named 'convergence-*', generated by 'make_convergence' and
    renamed manually by you. Note that the '*' indicates the plot label/machine
    name.

    """
    convergence_dir = os.path.dirname(c.get_image_path("convergence", "_", bridge=False))

    # Get all simulations results from each machine.
    machines = dict()
    for filepath in glob.glob(os.path.join(convergence_dir, "convergence-*")):
        machine_name = os.path.basename(filepath).split("-")[1].split(".")[0]
        machines[machine_name] = pd.read_csv(filepath).dropna()

    if len(machines) == 0:
        raise ValueError(f"No results found in {convergence_dir}")

    # Map from machine name to loading position to list of Series.
    machine_results = defaultdict(lambda: defaultdict(list))
    for machine_name, df in machines.items():
        for _, row in df.iterrows():
            x_load, z_load = row["xload"], row["zload"]
            machine_results[machine_name][(x_load, z_load)].append(row)

    # Map from machine name to loading position to list of lines to plot.
    results = defaultdict(dict)
    for machine_name, loading_pos_dict in machine_results.items():
        for (x_load, z_load), rows in loading_pos_dict.items():
            (
                max_mesh,
                mins_d,
                maxes_d,
                means_d,
                mins_s,
                maxes_s,
                means_s,
                time,
                ndeck,
                npier,
                shell_size,
                deck_shell_size,
                pier_shell_size,
            ) = (
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            )
            for row in rows:
                max_mesh.append(row["max_mesh"])
                mins_d.append(row["min_d"])
                maxes_d.append(row["max_d"])
                means_d.append(row["mean_d"])
                mins_s.append(row["min_s"])
                maxes_s.append(row["max_s"])
                means_s.append(row["mean_s"])
                time.append(row["time"])
                ndeck.append(row["decknodes"])
                npier.append(row["piernodes"])
                shell_size.append(row["shell-size"])
                deck_shell_size.append(row["deck-size"])
                pier_shell_size.append(row["pier-size"])
            results[machine_name][(x_load, z_load)] = list(
                map(
                    np.array,
                    [
                        max_mesh,
                        mins_d,
                        maxes_d,
                        means_d,
                        mins_s,
                        maxes_s,
                        means_s,
                        time,
                        ndeck,
                        npier,
                        shell_size,
                        deck_shell_size,
                        pier_shell_size,
                    ],
                )
            )

    def plot_intersection(x, xs, ys, of=None, units=None):
        y = np.interp(x, xs, ys)
        y_frac = y / ys[-1]
        y_percent = y_frac * 100
        label = None
        if of is not None:
            label = f"{y_percent:.2f}% of {of}"
        if units is not None:
            label = f"{units} = {y:.2f}"
        plt.axvline(x, label=label, color="black")

    CHOSEN_NUM_NODES = 25000

    ########################################
    ###### Min. and max. per machine #######
    ########################################

    # Displacement
    plt.landscape()
    for machine_name, loading_pos_dict in results.items():
        for (x_load, z_load), lines in loading_pos_dict.items():
            (
                max_mesh,
                mins_d,
                maxes_d,
                means_d,
                mins_s,
                maxes_s,
                means_s,
                time,
                ndeck,
                npier,
                shell_size,
                deck_shell_size,
                pier_shell_size,
            ) = lines

            num_nodes = ndeck + npier
            final_mean_d = np.mean(means_d[-5:])
            final_max_d = np.mean(maxes_d[-5:])
            final_min_d = np.mean(mins_d[-5:])
            plt.plot(
                num_nodes, mins_d / final_min_d, color="red", label="Min. response"
            )
            plt.plot(
                num_nodes,
                maxes_d / final_max_d,
                color="orange",
                label="Max. response",
            )
            plt.plot(
                num_nodes,
                means_d / final_mean_d,
                color="green",
                label="Mean response",
            )
            plot_intersection(CHOSEN_NUM_NODES, num_nodes, mins_d / final_min_d, "min")
            plot_intersection(CHOSEN_NUM_NODES, num_nodes, maxes_d / final_max_d, "max")
            plot_intersection(CHOSEN_NUM_NODES, num_nodes, means_d / final_mean_d, "mean")
        break

    # plt.xlim(plt.xlim()[1], plt.xlim()[0])
    plt.title("Normalized displacement as a function of number of nodes")
    plt.xlabel("Number of nodes")
    plt.ylabel("Normalized displacement")
    plt.legend()
    plt.savefig(c.get_image_path("convergence", "min-max-displacement.pdf", bridge=False))
    plt.close()

    # Strain
    plt.landscape()
    for machine_name, loading_pos_dict in results.items():
        for (x_load, z_load), lines in loading_pos_dict.items():
            (
                max_mesh,
                mins_d,
                maxes_d,
                means_d,
                mins_s,
                maxes_s,
                means_s,
                time,
                ndeck,
                npier,
                shell_size,
                deck_shell_size,
                pier_shell_size,
            ) = lines

            num_nodes = ndeck + npier
            final_mean_s = np.mean(means_s[-5:])
            final_max_s = np.mean(maxes_s[-5:])
            final_min_s = np.mean(mins_s[-5:])
            plt.plot(
                num_nodes, mins_s / final_min_s, color="red", label="Min. response"
            )
            plt.plot(
                num_nodes,
                maxes_s / final_max_s,
                color="orange",
                label="Max. response",
            )
            plt.plot(
                num_nodes,
                means_s / final_mean_s,
                color="green",
                label="Mean response",
            )
            plot_intersection(CHOSEN_NUM_NODES, num_nodes, mins_s / final_min_s, "min")
            plot_intersection(CHOSEN_NUM_NODES, num_nodes, maxes_s / final_max_s, "max")
            plot_intersection(CHOSEN_NUM_NODES, num_nodes, means_s / final_mean_s, "mean")

    # plt.xlim(plt.xlim()[1], plt.xlim()[0])
    plt.title("Normalized strain as a function of number of nodes")
    plt.xlabel("Number of nodes")
    plt.ylabel("Normalized strain")
    plt.legend()
    plt.savefig(c.get_image_path("convergence", "min-max-strain.pdf", bridge=False))
    plt.close()

    #########################
    ###### Model size #######
    #########################

    # This should be the same for each machine, so skip the rest.
    for machine_name, loading_pos_dict in results.items():
        for (x_load, z_load), lines in loading_pos_dict.items():
            (
                max_mesh,
                mins_d,
                maxes_d,
                means_d,
                mins_s,
                maxes_s,
                means_s,
                time,
                ndeck,
                npier,
                shell_size,
                deck_shell_size,
                pier_shell_size,
            ) = lines
            num_nodes = ndeck + npier
            plt.plot(num_nodes, shell_size, label="Mean shell area")
            plot_intersection(CHOSEN_NUM_NODES, num_nodes, shell_size, units="Shell area (m²)")
        break

    # plt.ylim(plt.ylim()[1], plt.ylim()[0])
    plt.title("Mean shell area as a function of number of nodes")
    plt.xlabel("Number of nodes")
    plt.ylabel("Shell area (m²)")
    plt.legend()
    plt.savefig(c.get_image_path("convergence", "model-size.pdf", bridge=False))
    plt.close()

    # This should be the same for each machine, so skip the rest.
    for machine_name, loading_pos_dict in results.items():
        for (x_load, z_load), lines in loading_pos_dict.items():
            (
                max_mesh,
                mins_d,
                maxes_d,
                means_d,
                mins_s,
                maxes_s,
                means_s,
                time,
                ndeck,
                npier,
                shell_size,
                deck_shell_size,
                pier_shell_size,
            ) = lines
            # plt.plot(max_mesh, max_mesh, label="Max. shell length parameter")
            plt.plot(max_mesh, shell_size)
        break

    # plt.xlim(plt.xlim()[1], plt.xlim()[0])
    # plt.ylim(plt.ylim()[1], plt.ylim()[0])
    plt.title("Mean shell area as a function of max. shell length parameter")
    plt.xlabel("Max. shell length parameter (m)")
    plt.ylabel("Shell area (m²)")
    # plt.legend()
    plt.savefig(c.get_image_path("convergence", "model-size-param.pdf", bridge=False))
    plt.close()

    # This should be the same for each machine, so skip the rest.
    for machine_name, loading_pos_dict in results.items():
        for (x_load, z_load), lines in loading_pos_dict.items():
            (
                max_mesh,
                mins_d,
                maxes_d,
                means_d,
                mins_s,
                maxes_s,
                means_s,
                time,
                ndeck,
                npier,
                shell_size,
                deck_shell_size,
                pier_shell_size,
            ) = lines
            num_nodes = ndeck + npier
            plt.plot(num_nodes, max_mesh)
            plot_intersection(CHOSEN_NUM_NODES, num_nodes, max_mesh, units="Shell length (m)")
        break

    # plt.ylim(plt.ylim()[1], plt.ylim()[0])
    plt.title("Max. shell length parameter as a function of number of nodes")
    plt.xlabel("Number of nodes")
    plt.ylabel("Max. shell length parameter (m)")
    plt.legend()
    plt.savefig(c.get_image_path("convergence", "chosen-param.pdf", bridge=False))
    plt.close()

    ###################################
    ###### Run time per machine #######
    ###################################

    for machine_name, loading_pos_dict in results.items():
        for (x_load, z_load), lines in loading_pos_dict.items():
            (
                max_mesh,
                mins_d,
                maxes_d,
                means_d,
                mins_s,
                maxes_s,
                means_s,
                time,
                ndeck,
                npier,
                shell_size,
                deck_shell_size,
                pier_shell_size,
            ) = lines
            num_nodes = (ndeck + npier)[:-1]
            times = time[:-1]
            plt.plot(num_nodes, times)
            plot_intersection(CHOSEN_NUM_NODES, num_nodes, times, units="Run time (s)")
            print_w("Removed one outlier!")
        break

    # plt.xlim(plt.xlim()[1], plt.xlim()[0])
    plt.title("Run-time as a function of number of nodes")
    plt.xlabel("Number of nodes")
    plt.ylabel("Run-time (s)")
    plt.legend()
    plt.savefig(c.get_image_path("convergence", "run-time.pdf", bridge=False))
    plt.close()

    #########################################
    ###### Individual: min, max, mean #######
    #########################################

    for machine_name, loading_pos_dict in results.items():
        for (x_load, z_load), lines in loading_pos_dict.items():
            (
                max_mesh,
                mins_d,
                maxes_d,
                means_d,
                mins_s,
                maxes_s,
                means_s,
                time,
                ndeck,
                npier,
                shell_size,
                deck_shell_size,
                pier_shell_size,
            ) = lines

            plt.plot(ndeck + npier, maxes_d)
            plt.title("Maximum displacement as a function of number of nodes")
            plt.xlabel("Number of nodes")
            plt.ylabel("Maximum displacement (mm)")
            plt.savefig(
                c.get_image_path(
                    "convergence", f"displacement-max-{machine_name}.pdf", bridge=False
                )
            )
            plt.close()

            plt.plot(ndeck + npier, mins_d)
            plt.title("Minimum displacement as a function of number of nodes")
            plt.xlabel("Number of nodes")
            plt.ylabel("Minimum displacement (mm)")
            plt.savefig(
                c.get_image_path(
                    "convergence", f"displacement-min-{machine_name}.pdf", bridge=False
                )
            )
            plt.close()

            plt.plot(ndeck + npier, means_d)
            plt.title("Mean displacement as a function of number of nodes")
            plt.xlabel("Number of nodes")
            plt.ylabel("Mean displacement (mm)")
            plt.savefig(
                c.get_image_path(
                    "convergence", f"displacment-mean-{machine_name}.pdf", bridge=False
                )
            )
            plt.close()

            ############################################
            ###### Individual: Mean element size #######
            ############################################

            plt.plot(shell_size, shell_size, label="Mean shell area")
            plt.plot(shell_size, deck_shell_size, label="Mean deck shell area")
            plt.plot(shell_size, pier_shell_size, label="Mean pier shell area")
            # plt.xlim(plt.xlim()[1], plt.xlim()[0])
            # plt.ylim(plt.ylim()[1], plt.ylim()[0])
            plt.legend()
            plt.title("Mean element area")
            plt.xlabel("Mean shell area (m²)")
            plt.ylabel("Shell area (m²)")
            plt.savefig(
                c.get_image_path(
                    "convergence", f"mean-element-size-{machine_name}.pdf", bridge=False
                )
            )
            plt.close()


def axis_comparison(c: Config):
    """"""
    if len(c.bridge.sections) > 1:
        raise ValueError("Bridge deck has more than one section")
    for pier in c.bridge.supports:
        if len(pier.sections) > 1:
            raise ValueError(f"Bridge pier {pier} has more than one section")

    ###############################
    ###### Point load plots #######
    ###############################

    positions = [(35, 25 - 16.6)]
    response_types = [ResponseType.YTranslation]
    for response_type in response_types:
        for load_x, load_z in positions:
            loads = [
                PointLoad(
                    x_frac=c.bridge.x_frac(load_x),
                    z_frac=c.bridge.z_frac(load_z),
                    kn=100,
                )
            ]
            fem_responses = load_fem_responses(
                c=c,
                response_type=response_type,
                sim_runner=OSRunner(c),
                sim_params=SimParams(ploads=loads, response_types=response_types),
            )
            title = (
                f"{response_type.name()} from a {loads[0].kn} kN point load"
                + f" at x = {load_x:.3f}m, z = {load_z:.3f}m"
            )
            save = lambda prefix: c.get_image_path(
                "contour-axis-comparison",
                safe_str(
                    f"{prefix}{response_type.name()}-loadx={load_x:.3f}-loadz={load_z:.3f}"
                ),
            )
            top_view_bridge(c.bridge, piers=True, abutments=True)
            plot_contour_deck(
                c=c, responses=fem_responses, ploads=loads, title=title,
            )
            plt.savefig(save(""))
            plt.close()
