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

from classify.data.responses import responses_to_traffic_array
from classify.scenario.bridge import HealthyBridge, PierDispBridge
from config import Config
from fem.params import SimParams
from fem.responses import Responses, load_fem_responses
from fem.run.opensees import OSRunner
from fem.run.opensees.build.d3 import nodes_by_id
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_config
from model.load import DisplacementCtrl, PointLoad
from model.response import ResponseType
from plot import plt
from plot.geom import top_view_bridge
from plot.responses import plot_contour_deck
from util import clean_generated, print_i, read_csv, safe_str


def campaign_measurements(
        c: Config, rows: int=5, cols: int=2, individual_sensors: List[str] = ["T4", "U3"]):
    """Compare the bridge 705 measurement campaign to Diana and OpenSees."""
    size = 25

    meas = pd.read_csv("data/verification/measurements_static_ZB.csv")
    diana = pd.read_csv("data/verification/modelpredictions_april2019.csv")
    displa_sensors = pd.read_csv("data/verification/displasensors.txt")
    strain_sensors = pd.read_csv("data/verification/strainsensors.txt")

    ####################
    ###### Strain ######
    ####################

    # All strain measurements from TNO sensors (label start with "T").
    # But ignore sensor T0 since no diana predictions are available.
    strain_meas = meas.loc[meas["sensortype"] == "strains"]
    tno_strain_meas = meas.loc[meas["sensorlabel"].str.startswith("T")]
    tno_strain_meas = tno_strain_meas.loc[tno_strain_meas["sensorlabel"] != "T0"]

    def plot(sensor_label, meas_group):
        # Plot Diana predictions for the given sensor.
        diana_group = diana[diana["sensorlabel"] == sensor_label]
        plt.scatter(diana_group["xpostruck"], diana_group["infline1"], marker="o", s=size, label="Diana")

        # Plot measured values against truck position.
        plt.scatter(meas_group["xpostruck"], meas_group["inflinedata"], marker="o", s=size, label="measurement")

        plt.legend()
        plt.title(f"Strain at {sensor_label}")
        plt.xlabel("x position of truck front axle (m)")
        plt.ylabel("strain (m/m)")

    # Create a subplot for each strain sensor.
    plot_i, subplot_i = 0, 0
    strain_groupby = tno_strain_meas.groupby("sensorlabel")
    for i, (sensor_label, meas_group) in enumerate(strain_groupby):
        plt.subplot(rows, cols, subplot_i + 1)
        plot(sensor_label, meas_group)
        if subplot_i + 1 == rows * cols or i == len(strain_groupby) - 1:
            plt.savefig(c.get_data_path(
                dirname="verification",
                filename=f"strain-{plot_i}",
                acc=False))
            plt.close()
            plot_i += 1
            subplot_i = 0
        else:
            subplot_i += 1

    # Create any plots for individual sensors.
    for sensor_label, meas_group in strain_groupby:
        if sensor_label in individual_sensors:
            plot(sensor_label, meas_group)
            plt.savefig(c.get_data_path(
                dirname="verification",
                filename=f"strain-sensor-{sensor_label}",
                acc=False))
            plt.close()

    ##########################
    ###### Displacement ######
    ##########################

    # All displacement measurements.
    displa_meas = meas.loc[meas["sensortype"] == "displacements"]

    def plot(sensor_label, meas_group):
        # Plot Diana predictions for the given sensor.
        diana_group = diana[diana["sensorlabel"] == sensor_label]
        plt.scatter(diana_group["xpostruck"], diana_group["infline1"], marker="o", s=size, label="Diana")

        # Plot measured values sorted by truck position.
        plt.scatter(meas_group["xpostruck"], meas_group["inflinedata"], marker="o", s=size, label="measurement")

        plt.legend()
        plt.title(f"Displacement at {sensor_label}")
        plt.xlabel("x position of truck front axle (m)")
        plt.ylabel("displacement (mm)")

    # Create a subplot for each displacement sensor.
    plot_i, subplot_i = 0, 0
    displa_groupby = displa_meas.groupby("sensorlabel")
    for i, (sensor_label, meas_group) in enumerate(displa_groupby):
        plt.subplot(rows, cols, subplot_i + 1)
        plot(sensor_label, meas_group)
        if subplot_i + 1 == rows * cols or i == len(displa_groupby) - 1:
            plt.savefig(c.get_data_path(
                dirname="verification",
                filename=f"displa-{plot_i}",
                acc=False))
            plt.close()
            plot_i += 1
            subplot_i = 0
        else:
            subplot_i += 1

    # Create any plots for individual sensors.
    for sensor_label, meas_group in displa_groupby:
        if sensor_label in individual_sensors:
            plot(sensor_label, meas_group)
            plt.savefig(c.get_data_path(
                dirname="verification",
                filename=f"displa-sensor-{sensor_label}",
                acc=False))
            plt.close()

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


def plot_pier_displacement(c: Config):
    """Comparison of two calculations of pier displacement.

    One calculation is directly from a pier displacement simulation, while the
    second is from 'responses_to_traffic_array' where the 'TrafficArray' is set
    to 0.

    """
    pier_index = 5
    pier = c.bridge.supports[pier_index]
    response_type = ResponseType.YTranslation
    pier_displacement = DisplacementCtrl(
        displacement=c.pd_unit_disp, pier=pier_index
    )

    # Plot responses captured directly from a pier displacement simualtion.
    sim_params = SimParams(
        response_types=[response_type], displacement_ctrl=pier_displacement,
    )
    sim_responses = load_fem_responses(
        c=c,
        sim_params=sim_params,
        response_type=response_type,
        sim_runner=OSRunner(c),
    )
    plt.subplot(2, 1, 1)
    top_view_bridge(c.bridge, lanes=False, outline=False)
    _, _, norm = plot_contour_deck(
        c=c,
        responses=sim_responses,
        ploads=[
            PointLoad(
                x_frac=c.bridge.x_frac(pier.x),
                z_frac=c.bridge.z_frac(pier.z),
                kn=c.pd_unit_load_kn,
            )
        ],
    )
    plt.colorbar(norm=norm)

    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, 10),
            np.linspace(c.bridge.z_min, c.bridge.z_max, 10),
        )
    ]
    bridge_scenario = PierDispBridge(pier_displacement)
    wheel_zs = c.bridge.wheel_tracks(c)
    response_array = responses_to_traffic_array(
        c=c,
        traffic_array=np.zeros((10, len(wheel_zs) * c.il_num_loads)),
        response_type=response_type,
        bridge_scenario=bridge_scenario,
        points=points,
        fem_runner=OSRunner(c),
    )
    plt.subplot(2, 1, 2)
    top_view_bridge(c.bridge, lanes=False, outline=False)
    responses = Responses.from_responses(
        response_type=response_type,
        responses=[
            (response_array[0][p], point) for p, point in enumerate(points)
        ],
    )
    _, _, norm = plot_contour_deck(
        c=c,
        responses=responses,
        ploads=[
            PointLoad(
                x_frac=c.bridge.x_frac(pier.x),
                z_frac=c.bridge.z_frac(pier.z),
                kn=c.pd_unit_load_kn,
            )
        ],
    )
    plt.colorbar(norm=norm)

    plt.savefig(c.get_image_path("verification", "pier-displacement"))
