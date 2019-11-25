"""Verification plots."""
import glob
import itertools
import os
from collections import defaultdict
from itertools import chain
from timeit import default_timer as timer
from typing import List, Optional

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
from config import Config
from fem.params import SimParams
from fem.responses import Responses, load_fem_responses
from fem.run.opensees import OSRunner
from fem.run.opensees.build.d3 import nodes_by_id
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_config
from model.load import DisplacementCtrl, MvVehicle, PointLoad
from model.response import ResponseType
from plot import plt
from plot.geom import top_view_bridge
from plot.responses import plot_contour_deck
from util import clean_generated, print_i, read_csv, safe_str

# Wagen 1 from the experimental campaign.
to_kn = 0.00980665
wagen1 = MvVehicle(
    kn=[
        (5050 * to_kn, 5300 * to_kn),
        (4600 * to_kn, 4000 * to_kn),
        (4350 * to_kn, 3700 * to_kn),
        (4050 * to_kn, 3900 * to_kn),
    ],
    axle_distances=[3.6, 1.32, 1.45],
    axle_width=2.5,
    kmph=40,
    lane=0,
    init_x_frac=0,
)

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


def sensor_subplots(
    c: Config,
    rows: int = 5,
    cols: int = 2,
    individual_sensors: List[str] = ["T4", "U3"],
):
    """Compare the bridge 705 measurement campaign to Diana and OpenSees.

    TODO: Move to plot.verification.705
    """
    size = 25  # Size of scatter plot points.

    ####################
    ###### Strain ######
    ####################

    # All strain measurements from TNO sensors (label start with "T"), except
    # ignore sensor T0 since no diana predictions are available.
    tno_strain_meas = meas.loc[meas["sensorlabel"].str.startswith("T")]
    tno_strain_meas = tno_strain_meas.loc[
        tno_strain_meas["sensorlabel"] != "T0"
    ]

    # Sort by sensor number and setup groupby sensor label.
    tno_strain_meas["sort"] = tno_strain_meas["sensorlabel"].apply(
        lambda x: int(x[1:])
    )
    tno_strain_meas = tno_strain_meas.sort_values(by=["sort"])
    strain_groupby = tno_strain_meas.groupby("sensorlabel", sort=False)

    # Find the min and max responses.
    amin, amax = np.inf, -np.inf
    for sensor_label, meas_group in strain_groupby:
        diana_group = diana[diana["sensorlabel"] == sensor_label]
        responses = (
            diana_group["infline1"].to_list()
            + meas_group["inflinedata"].to_list()
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
                    dirname="verification",
                    filename=f"strain-{plot_i}",
                    acc=False,
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
                    dirname="verification",
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
            diana_group["infline1"].to_list()
            + meas_group["inflinedata"].to_list()
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
            diana_group["xpostruck"],
            diana_group["infline1"],
            s=size,
            label="Diana",
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
                    dirname="verification",
                    filename=f"displa-{plot_i}",
                    acc=False,
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
                    dirname="verification",
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
    displa_meas: List[Tuple(str, float, float)] = []
    displa_diana: List[Tuple(str, float, float)] = []
    # List of sensor labels and positions in the same order as above.
    sensors = []
    # All truck positions used in measurements.
    truck_xs_meas = set()
    # { Sensor label : { truck x position : response value }}
    displa_diana_dict = defaultdict(dict)

    # For each sensor and truck x position record measurment and Diana response.
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
            displa_diana_dict[sensor_label][truck_x] = displa_diana[-1]
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
                Point(x=sensor_x, y=0, z=sensor_z)
                for _, sensor_x, sensor_z in sensors
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
    plt.subplot(3, 2, 1)
    x = list(map(lambda x: x[2], displa_meas))
    y = [
        displa_diana_dict[sensor_label][truck_x]
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
    plt.equal_ax_lims()
    plt.gca().set_aspect("equal")

    # Subplot: OpenSees against measurements.
    plt.subplot(3, 2, 3)
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
    plt.equal_ax_lims()
    plt.gca().set_aspect("equal")

    # Subplot: OpenSees against Diana.
    plt.subplot(3, 2, 5)
    x = [diana_response(sensor_label=sensor_label, truck_x=truck_x)
        for sensor_label, truck_x, _ in displa_meas]
    y = [get_os_meas(sensor_label=sensor_label, truck_x=truck_x)
        for sensor_label, truck_x, _ in displa_meas]
    plt.scatter(x, y)
    regressor = LinearRegression().fit(np.matrix(x).T, y)
    y_pred = regressor.predict(np.matrix(x).T)
    score = regressor.score(np.matrix(x).T, y)
    plt.plot(x, y_pred, color="red", label=f"R² = {score:.3f}")
    plt.legend()
    plt.title("Displacement: OpenSees vs. Diana")
    plt.xlabel("Displacement in Diana (mm)")
    plt.ylabel("Displacement in OpenSees (mm)")
    plt.equal_ax_lims()
    plt.gca().set_aspect("equal")
    plt.show()


def make_convergence_data(c: Config, run: bool, plot: bool):
    """Make convergence data file, increasing mesh density per simulation.

    NOTE: This is a simplistic plot. After running this function with argument
    'run=True' on a few different machines, the results should be gathered as
    specified in 'plot_convergence' and that function run to generate a better
    plot.

    Args:
        c: Config, global configuration object.
        run: bool, whether to re-run data collection simulations.
        plot: bool, whether to plot the resulting data.

    """
    response_type = ResponseType.YTranslation
    load_point = Point(x=35, y=0, z=9.4)
    bridge = bridge_705_3d()
    fem_params = SimParams(
        ploads=[
            PointLoad(
                x_frac=bridge.x_frac(load_point.x),
                z_frac=bridge.z_frac(load_point.z),
                kn=100,
            )
        ],
        response_types=[response_type],
    )
    x, z = 2, 2

    def bridge_overload(**kwargs):
        return bridge_705_3d(
            name=f"Bridge 705",
            accuracy="convergence",
            base_mesh_deck_nodes_x=x,
            base_mesh_deck_nodes_z=z,
            **kwargs,
        )

    c = bridge_705_config(bridge_overload)
    path = os.path.join(
        c.root_generated_images_dir, "convergence", "convergence_results"
    )

    if run:
        with open(path + ".txt", "w") as f:
            f.write(
                "xload, zload, xnodes, znodes, decknodes, piernodes, time, "
                + "min, max, ..."
            )
        steps = 100
        xs = np.linspace(2, c.bridge.length * 4, steps)
        zs = np.linspace(2, c.bridge.width * 4, steps)
        for step in range(steps):
            clean_generated(c)
            x, z = int(xs[step]), int(zs[step])
            with open(path + ".txt", "a") as f:
                f.write(f"\n{load_point.x}, {load_point.z}, {x}, {z}")
            c = bridge_705_config(bridge_overload)
            start = timer()
            try:
                responses = load_fem_responses(
                    c=c,
                    sim_params=fem_params,
                    response_type=response_type,
                    sim_runner=OSRunner(c),
                )
                deck_nodes = len([n for n in nodes_by_id.values() if n.deck])
                pier_nodes = len(
                    [
                        n
                        for n in nodes_by_id.values()
                        if n.pier is not None and not n.deck
                    ]
                )
                assert deck_nodes + pier_nodes == len(nodes_by_id)
                with open(path + ".txt", "a") as f:
                    f.write(
                        f", {deck_nodes}, {pier_nodes}, {timer() - start}"
                        + f", {responses.min()}, {responses.max()}"
                    )
            except ValueError as e:
                if "No responses found" in str(e):
                    print_i("Simulation failed. Time to plot results")
                else:
                    raise e

    if plot:
        results = read_results(path + ".txt", min_spaces=4)
        plt.plot([r[7] for r in results])
        plt.savefig(path)
        plt.close()


def plot_convergence(c: Config, only: Optional[List[str]] = None):
    """Plot convergence as mesh density is increased for multiple machines.

    Loads data from
        'os.path.join(Config.root_generated_images_dir, "convergence")'.

    Loads a file 'truth.txt' with three columns, two for the loading position
    (x, z), and one containing the maximum response recorded in the simulation.

    Also loads files named 'convergence-*'. These are files generated by
    'make_convergence' and renamed manually by you. Note that the '*' indicates
    the plot label/machine name.

    Args:
        c: Config, global configuration object.
        only: Optional[List[str]], an optional list of machine names to limit
            the plot to.

    """
    convergence_dir = os.path.join(c.root_generated_images_dir, "convergence")

    # Get all max responses that represent ground truth.
    results = read_results(os.path.join(convergence_dir, "truth.txt"))
    truth = dict()
    for x_load, z_load, max_response in results:
        truth[(x_load, z_load)] = max_response

    # Get all simulations results from each machine.
    machines = dict()
    for filepath in glob.glob(os.path.join(convergence_dir, "convergence-*")):
        machine_name = os.path.basename(filepath).split("-")[1].split(".")[0]
        if only is None or machine_name in only:
            machines[machine_name] = read_results(path=filepath, min_spaces=4)

    # Map simulation results by loading position.
    machine_results = defaultdict(lambda: defaultdict(list))
    for machine_name, results in machines.items():
        for line in results:
            x_load, z_load = line[:2]
            machine_results[machine_name][(x_load, z_load)].append(line)

    # Setup plotting data for each machine.
    err_lines, time_lines = [], []
    for machine_name, results_dict in machine_results.items():
        for (x_load, z_load), results in results_dict.items():
            if (x_load, z_load) not in truth:
                raise ValueError("No ground truth for ({x_load}, {z_load})")
            err, time = [], []
            deck_nodes = []
            for _, _, _, _, deck, sim_time, max_response in results:
                err.append(abs(truth[(x_load, z_load)] - max_response))
                time.append(sim_time)
                deck_nodes.append(deck)
            err_lines.append([machine_name, err])
            time_lines.append([machine_name, time])

    # Error plots.
    fig, ax1 = plt.subplots()
    for machine_name, err in err_lines:
        ax1.plot(err, label=machine_name)
    ax1.legend(loc="upper left")

    # Number of node plots.
    ax2 = ax1.twinx()
    ax2.plot(deck_nodes, label="deck nodes", color="orange")
    ax2.legend(loc="upper right")
    plt.savefig(os.path.join(convergence_dir, "error"))
    plt.close()

    # Time plots.
    fig, ax1 = plt.subplots()
    for machine_name, time in time_lines:
        ax1.plot(time, label=machine_name)
    ax1.legend(loc="upper left")

    # Number of node plots.
    ax2 = ax1.twinx()
    ax2.plot(deck_nodes, label="deck nodes", color="orange")
    ax2.legend(loc="upper right")
    plt.savefig(os.path.join(convergence_dir, "time"))
    plt.close()
