"""Verification plots."""

import glob
import itertools
import os
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from timeit import default_timer as timer
from typing import List, Optional, Tuple

import matplotlib
import matplotlib.cm as cm
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression

from bridge_sim.internal.plot import plt
from bridge_sim.model import Config, PierSettlement, Point, PointLoad, ResponseType
from bridge_sim.sim.responses import to_vehicles_direct
from bridge_sim.vehicles import truck1
from bridge_sim.sim.build import det_nodes, det_shells
from bridge_sim.sim.model import SimParams
from bridge_sim.sim.responses import load_fem_responses
from bridge_sim.sim.run.opensees import OSRunner
from bridge_sim.plot.util import legend_marker_size
from bridge_sim.plot import contour_responses, top_view_bridge
from bridge_sim.internal.plot.validation import (
    plot_mmm_strain_convergence,
    plot_nesw_convergence,
)
from bridge_sim.util import (
    print_i,
    print_w,
    round_m,
    safe_str,
    scalar,
)
from bridge_sim.internal.validate import (
    _meas,
    _displa_sensors,
    _strain_sensors,
    _strain_sensor_xz,
    _displa_sensor_xz,
)

# Positions of truck front axle.
truck_front_x = np.arange(1, 116.1, 1)

diana_path = "data/validation/modelpredictions_april2019.csv"
if os.path.exists(diana_path):
    diana = pd.read_csv(diana_path)

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
    rows: int = 3,
    strain_sensors_startwith: str = "T",
    strain_sensors_ignore: List[str] = ["T0"],
    individual_sensors: List[str] = ["T4", "U3"],
    plot_diana: bool = False,
):
    """Compare the bridge 705 measurement campaign to Diana and OpenSees."""
    plt.portrait()
    size = 80  # Size of scatter plot points.
    lw = 4  # Line width of plots.

    ##########
    # Strain #
    ##########

    print_i("All strain sensors = ")
    print_i(f"  {sorted(set(_meas['sensorlabel']))}")
    # All strain measurements for a given sensor set (strain_sensors_startwith),
    # except ignore sensors in ignore set (strain_sensors_ignore).
    tno_strain_meas = _meas.loc[
        _meas["sensorlabel"].str.startswith(strain_sensors_startwith)
    ]
    labels_before_ignore = set(tno_strain_meas["sensorlabel"])
    tno_strain_meas = tno_strain_meas.loc[
        ~tno_strain_meas["sensorlabel"].isin(strain_sensors_ignore)
    ]
    labels_after_ignore = set(tno_strain_meas["sensorlabel"])
    labels_ignored = sorted(
        l for l in labels_before_ignore if l not in labels_after_ignore
    )
    print_i(f"Strain sensors ignored = {labels_ignored}")

    # Ignore sensors with missing positions.
    positions_available = set(
        _strain_sensors[_strain_sensors["direction"] == "X"]["label"]
    )
    labels_before_ignore = set(tno_strain_meas["sensorlabel"])
    tno_strain_meas = tno_strain_meas.loc[
        tno_strain_meas["sensorlabel"].isin(positions_available)
    ]
    labels_after_ignore = set(tno_strain_meas["sensorlabel"])
    labels_ignored = sorted(
        l for l in labels_before_ignore if l not in labels_after_ignore
    )
    print_i(f"Microstrain XXB sensors with missing positions = {labels_ignored}")

    # Sort by sensor number and setup groupby sensor label.
    tno_strain_meas["sort"] = tno_strain_meas["sensorlabel"].apply(lambda x: int(x[1:]))
    print_i(f"Filtered strain sensors starting with {strain_sensors_startwith} =")
    print_i(f"  {sorted(set(map(int, tno_strain_meas['sort'])))}")

    tno_strain_meas = tno_strain_meas.sort_values(by=["sort"])
    strain_groupby = tno_strain_meas.groupby("sensorlabel", sort=False)
    strain_sensor_labels = [sensor_label for sensor_label, _ in strain_groupby]
    strain_sensor_xzs = list(map(_strain_sensor_xz, strain_sensor_labels))
    print(f"strain sensor xsz = {strain_sensor_xzs}")

    # Find the min and max fem.
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

    # Calculate displacement with OpenSees via direct simulation.
    print(f"Parallel {c.parallel}")
    os_strain = (
        to_vehicles_direct(
            c=c,
            vehicles=[truck1],
            times=[truck1.time_at(x=x, bridge=c.bridge) for x in truck_front_x],
            response_type=ResponseType.StrainXXB,
            points=[
                Point(x=sensor_x, y=0, z=sensor_z)
                for sensor_x, sensor_z in strain_sensor_xzs
            ],
        ).T
        * 1e6
    )
    os_strain_shape = np.array(os_strain).shape
    if len(os_strain_shape) == 3 and os_strain_shape[0] == 1:
        os_strain = os_strain[0]
    amin = min(amin, np.amin(os_strain))
    amax = max(amax, np.amax(os_strain))

    def plot(i, sensor_label, meas_group):
        # Plot Diana predictions for the given sensor.
        if plot_diana:
            diana_sensor_group = diana[diana["sensorlabel"] == sensor_label]
            plt.plot(
                diana_sensor_group["xpostruck"],
                diana_sensor_group["infline1"],
                lw=lw,
                label="Diana",
            )

        # Plot values from OpenSees.
        plt.plot(truck_front_x, os_strain[i], lw=lw, label="OpenSees", c="tab:blue")

        # Plot measured values against truck position.
        sensor_x, sensor_z = strain_sensor_xzs[i]
        plt.scatter(
            meas_group["xpostruck"],
            meas_group["inflinedata"],
            marker="o",
            s=size,
            label="Measurement",
            zorder=3,
            color="tab:red",
        )

        plt.scatter(
            [0],
            [0],
            label=f"{sensor_label}: x = {np.around(sensor_x, 3)} m, z = {np.around(sensor_z, 3)} m",
            alpha=0,
            zorder=4,
        )
        legend_marker_size(plt.legend(), 80)
        plt.ylabel("Microstrain XXB")
        plt.ylim((amin, amax))

    # Create a subplot for each strain sensor.
    plot_i, subplot_i = 0, 0
    for i, (sensor_label, meas_group) in enumerate(strain_groupby):
        plt.subplot(rows, 1, subplot_i + 1)
        plot(i, sensor_label, meas_group)
        if (subplot_i == rows - 1) or i == len(strain_groupby) - 1:
            plt.xlabel("X position of Truck 1's front axle (m)")
            plt.suptitle(
                "Microstrain XXB from Truck 1 on bridge 705\nstatic simulation vs. static test"
            )
            plt.tight_layout(rect=[0, 0.03, 1, 0.93])
            plt.savefig(
                c.get_image_path(
                    "validation/sensors",
                    f"strain-{strain_sensors_startwith}-{plot_i}.pdf",
                )
            )
            plt.close()
            subplot_i = 0
            plot_i += 1
        else:
            plt.tick_params(axis="x", bottom=False, labelbottom=False)
            subplot_i += 1

    # Create any plots for individual strain sensors.
    for i, (sensor_label, meas_group) in enumerate(strain_groupby):
        if sensor_label in individual_sensors:
            plt.landscape()
            plot(i, sensor_label, meas_group)
            plt.tight_layout()
            plt.savefig(
                c.get_image_path(
                    "validation/sensors", f"strain-sensor-{sensor_label}.pdf"
                )
            )
            plt.close()
            plt.portrait()

    ################
    # Vert. trans. #
    ################

    # All displacement measurements.
    displa_meas = pd.DataFrame(_meas.loc[_meas["sensortype"] == "displacements"])

    # Sort by sensor number and setup groupby sensor label.
    displa_meas["sort"] = displa_meas["sensorlabel"].apply(lambda x: int(x[1:]))
    displa_meas = displa_meas.sort_values(by=["sort"])
    displa_groupby = displa_meas.groupby("sensorlabel", sort=False)
    displa_sensor_labels = [sensor_label for sensor_label, _ in displa_groupby]
    displa_sensor_xzs = list(map(_displa_sensor_xz, displa_sensor_labels))

    # Find the min and max fem.
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
        to_vehicles_direct(
            c=c,
            vehicles=[truck1],
            times=[truck1.time_at(x=x, bridge=c.bridge) for x in truck_front_x],
            response_type=ResponseType.YTrans,
            points=[
                Point(x=sensor_x, y=0, z=sensor_z)
                for sensor_x, sensor_z in displa_sensor_xzs
            ],
        ).T
        * 1000
    )
    amin = min(amin, np.amin(os_displacement))
    amax = max(amax, np.amax(os_displacement))

    def plot(i, sensor_label, meas_group):
        # Plot Diana predictions for the given sensor.
        if plot_diana:
            diana_sensor_group = diana[diana["sensorlabel"] == sensor_label]
            plt.plot(
                diana_sensor_group["xpostruck"],
                diana_sensor_group["infline1"],
                lw=lw,
                label="Diana",
            )

        # Plot values from OpenSees.
        plt.plot(
            truck_front_x, os_displacement[i], lw=lw, label="OpenSees", c="tab:blue"
        )
        if i == 0:
            print(os_displacement[i])
            print(f"Truck front (head) = {truck_front_x[:7]}")
            print(f"Printed os_displacement")

        # Plot measured values sorted by truck position.
        sensor_x, sensor_z = displa_sensor_xzs[i]
        plt.scatter(
            meas_group["xpostruck"],
            meas_group["inflinedata"],
            s=size,
            label="Measurement",
            zorder=3,
            color="tab:red",
        )

        plt.scatter(
            [0],
            [0],
            label=f"{sensor_label}: x = {np.around(sensor_x, 3)} m, z = {np.around(sensor_z, 3)} m",
            alpha=0,
        )

        legend_marker_size(plt.legend(), 80)
        plt.ylabel(f"{ResponseType.YTrans.name()} (mm)")
        plt.ylim((amin, amax))

    # Create a subplot for each displacement sensor.
    plot_i, subplot_i = 0, 0
    for i, (sensor_label, meas_group) in enumerate(displa_groupby):
        plt.subplot(rows, 1, subplot_i + 1)
        plot(i, sensor_label, meas_group)
        if (subplot_i == rows - 1) or i == len(displa_groupby) - 1:
            plt.xlabel("X position of Truck 1's front axle (m)")
            plt.suptitle(
                "Y translation from Truck 1 on bridge 705\nstatic simulation vs. static test"
            )
            plt.tight_layout(rect=[0, 0.03, 1, 0.93])
            plt.savefig(c.get_image_path("validation/sensors", f"displa-{plot_i}.pdf"))
            plt.close()
            subplot_i = 0
            plot_i += 1
        else:
            plt.tick_params(axis="x", bottom=False, labelbottom=False)
            subplot_i += 1

    # Create any plots for individual sensors.
    plt.landscape()
    for i, (sensor_label, meas_group) in enumerate(displa_groupby):
        if sensor_label in individual_sensors:
            plot(i, sensor_label, meas_group)
            plt.tight_layout()
            plt.savefig(
                c.get_image_path(
                    "validation/sensors", f"displa-sensor-{sensor_label}.pdf",
                )
            )
            plt.close()


def r2_plots(c: Config):
    """R² plots for displacement and strain."""
    rt_y = ResponseType.YTrans
    rt_s = ResponseType.StrainXXB

    ################
    # Displacement #
    ################

    # Sensor label, truck x position, and response value.
    displa_meas: List[Tuple[str, float, float]] = []
    displa_diana: List[Tuple[str, float, float]] = []
    # List of sensor labels and positions in the same order as above.
    sensors = []
    # All truck positions used in measurements.
    truck_xs_meas = set()

    # For each sensor and truck x position plot the recorded measurement and
    # Diana response.
    for row in _displa_sensors.itertuples():
        sensor_label = getattr(row, "label")
        x, z = _displa_sensor_xz(sensor_label)
        sensors.append((sensor_label, x, z))
        responses = _meas[_meas["sensorlabel"] == sensor_label]
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
        to_vehicles_direct(
            c=c,
            vehicles=[truck1],
            times=[truck1.time_at(x=x, bridge=c.bridge) for x in truck_xs_meas],
            response_type=rt_y,
            points=[
                Point(x=sensor_x, y=0, z=sensor_z) for _, sensor_x, sensor_z in sensors
            ],
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
    plt.scatter(x, y, color="tab:blue")
    regressor = LinearRegression().fit(np.matrix(x).T, y)
    y_pred = regressor.predict(np.matrix(x).T)
    score = regressor.score(np.matrix(x).T, y)
    plt.plot(x, y_pred, color="tab:red", label=f"R² = {score:.3f}")
    plt.legend()
    plt.title(f"{rt_y.name()}: Diana vs. measurements")
    plt.xlabel(f"{rt_y.name()} measurement (mm)")
    plt.ylabel(f"{rt_y.name()} in Diana (mm)")

    # Subplot: OpenSees against measurements.
    plt.subplot(3, 1, 2)
    x = list(map(lambda x: x[2], displa_meas))
    y = [
        get_os_meas(sensor_label=sensor_label, truck_x=truck_x)
        for sensor_label, truck_x, _ in displa_meas
    ]
    plt.scatter(x, y, color="tab:blue")
    regressor = LinearRegression().fit(np.matrix(x).T, y)
    y_pred = regressor.predict(np.matrix(x).T)
    score = regressor.score(np.matrix(x).T, y)
    plt.plot(x, y_pred, color="tab:red", label=f"R² = {score:.3f}")
    plt.legend()
    plt.title(f"{rt_y.name()}: OpenSees vs. measurements")
    plt.xlabel(f"{rt_y.name()} measurement (mm)")
    plt.ylabel(f"{rt_y.name()} in OpenSees (mm)")

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
    plt.plot(x, y_pred, color="tab:red", label=f"R² = {score:.3f}")
    plt.legend()
    plt.title(f"{rt_y.name()}: OpenSees vs. Diana")
    plt.xlabel(f"{rt_y.name()} in Diana (mm)")
    plt.ylabel(f"{rt_y.name()} in OpenSees (mm)")

    plt.tight_layout()
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
    for row in _strain_sensors.itertuples():
        sensor_label = getattr(row, "label")
        x, z = _strain_sensor_xz(sensor_label)
        sensors.append((sensor_label, x, z))
        responses = _meas[_meas["sensorlabel"] == sensor_label]
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
    strain_os_meas = to_vehicles_direct(
        c=c,
        vehicles=[truck1],
        times=[truck1.time_at(x=x, bridge=c.bridge) for x in truck_xs_meas],
        response_type=rt_s,
        points=[
            Point(x=sensor_x, y=0, z=sensor_z) for _, sensor_x, sensor_z in sensors
        ],
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
    plt.plot(x, y_pred, color="tab:red", label=f"R² = {score:.3f}")
    plt.legend()
    plt.title("Strain XXB: Diana vs. measurements")
    plt.xlabel("Microstrain XXB measurement")
    plt.ylabel("Microstrain XXB in Diana")

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
    plt.plot(x, y_pred, color="tab:red", label=f"R² = {score:.3f}")
    plt.legend()
    plt.title("Strain XXB: OpenSees vs. measurements")
    plt.xlabel("Microstrain XXB measurement")
    plt.ylabel("Microstrain XXB in OpenSees")

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
    plt.plot(x, y_pred, color="tab:red", label=f"R² = {score:.3f}")
    plt.legend()
    plt.title("Strain: OpenSees vs. Diana")
    plt.xlabel("Microstrain XXB in Diana")
    plt.ylabel("Microstrain XXB in OpenSees")

    plt.tight_layout()
    plt.savefig(c.get_image_path("validation/regression", "regression-strain.pdf"))


def plot_pier_convergence(
    c: Config,
    process: int,
    pier_i: int,
    max_nodes: int,
    strain_ignore_radius: float,
    nesw_location: int,
    nesw_max_dist: float,
    min_shell_len: float,
    max_shell_len: Optional[float] = None,
):
    """Plot pier convergence, increasing mesh density per simulation."""
    # We will be modifying the 'Config', so make a copy.
    og_c = c
    c = deepcopy(c)
    sim_params = SimParams(
        response_types=[ResponseType.YTranslation, ResponseType.Strain],
        displacement_ctrl=PierSettlement(displacement=c.pd_unit_disp, pier=pier_i),
    )
    pier = c.bridge.supports[pier_i]
    if nesw_location == 0:
        nesw_point = Point(
            x=pier.x - (pier.length / 2), y=0, z=pier.z + (pier.width_top / 2)
        )
    else:
        raise ValueError("Invalid NESW plot location")
    if max_shell_len is None:
        max_shell_len = c.bridge.length / 10
    # Construct a function to ignore fem, this is around pier lines.
    without = without.pier_lines(c=c, radius=strain_ignore_radius)

    def update_bridge():
        c.bridge.name = "Bridge 705"
        c.bridge.accuracy = f"convergence-pier-{pier_i}-{max_shell_len}"
        c.bridge.base_mesh_deck_max_x = max_shell_len
        c.bridge.base_mesh_deck_max_z = max_shell_len
        c.bridge.base_mesh_pier_max_long = max_shell_len
        return c.bridge

    # Write parameter information to the results file.
    filepath = c.get_image_path(
        "convergence-pier",
        safe_str(f"{c.bridge.name}-{process}-convergence-results-pier-{pier_i}")
        + ".csv",
        # We are storing results for all model sizes in the same file, so no
        # need for bridge accuracy in filepath.
        acc=False,
    )
    print_i(f"Expecting parameters at {filepath}")

    if not os.path.exists(filepath):
        print_i(filepath)
        # Parameters of simulations are written to a file.
        df = pd.DataFrame(
            columns=[
                "deck-nodes",
                "pier-nodes",
                "time",
                "shell-size",
                "deck-size",
                "pier-size",
            ]
        )
        df.index.name = "max-shell-len"
        df.to_csv(filepath)
    df = pd.read_csv(filepath, index_col="max-shell-len")

    max_shell_lens = list(np.arange(max_shell_len, 2 - 0.00001, -1))
    max_shell_lens += list(np.arange(1.9, 1 - 0.00001, -0.1))
    max_shell_lens += list(np.arange(0.9, 0.1 - 0.00001, -0.01))
    max_shell_lens = list(map(round_m, max_shell_lens))
    max_shell_lens = [msl for msl in max_shell_lens if msl <= max_shell_len]
    max_shell_lens = [msl for msl in max_shell_lens if msl >= min_shell_len]
    print_i(f"Max shell lens = {max_shell_lens}")

    # Load fem for each parameter setting. If the simulation has not run
    # yet then it will be run and the parameter settings saved.
    all_displacements = dict()
    all_strains = dict()
    for max_shell_len in max_shell_lens:
        print(f"max shell len = {max_shell_len}")
        update_bridge()
        try:
            # Start timing and load the results into memory.
            start = timer()
            displacements = load_fem_responses(
                c=c,
                sim_params=sim_params,
                response_type=ResponseType.YTranslation,
                sim_runner=OSRunner(c),
            )
            all_displacements[max_shell_len] = displacements
            strains = load_fem_responses(
                c=c,
                sim_params=sim_params,
                response_type=ResponseType.Strain,
                sim_runner=OSRunner(c),
            )
            all_strains[max_shell_len] = strains.resize()
            end = timer()
            # If the simulation was run, then nodes from the built FEM will be
            # attached. In that case save the paramameters.
            if hasattr(sim_params, "bridge_nodes"):
                nodes = det_nodes(sim_params.bridge_nodes)
                # Clear the parameter, so the test works next iteration.
                del sim_params.bridge_nodes
                deck_nodes = len([n for n in nodes if n.deck])
                pier_nodes = len([n for n in nodes if not n.deck])
                assert deck_nodes + pier_nodes == len(nodes)
                # Determine shell sizes for the deck, pier and whole bridge.
                shells = det_shells(sim_params.bridge_shells)
                avg_shell_size = np.mean([s.area() for s in shells])
                avg_deck_size = np.mean([s.area() for s in shells if not s.pier])
                avg_pier_size = np.mean([s.area() for s in shells if s.pier])
                # Add the new parameters to the DataFrame and write to disk.
                if max_shell_len in df.index:
                    df.drop(max_shell_len)
                df.append(pd.Series(name=max_shell_len))
                for param_name, param in [
                    ("deck-nodes", deck_nodes),
                    ("pier-nodes", pier_nodes),
                    ("time", end - start),
                    ("shell-size", avg_shell_size),
                    ("deck-size", avg_deck_size),
                    ("pier-size", avg_pier_size),
                ]:
                    df.at[max_shell_len, param_name] = param
                df.to_csv(filepath)
            row = df.loc[max_shell_len, :]
            # Stop the simulation if maximum amount of nodes are reached.
            if float(row["deck-nodes"]) + float(row["pier-nodes"]) > max_nodes:
                print_i("Maximum nodes reached")
                break
            # TODO: Remove to deck interpolation test.
            # for x in displacements.xs:
            #     if 0 in displacements.zs[x]:
            #         for z in displacements.zs[x][0]:
            #             og = displacements.fem[0][x][0][z]
            #             ip = displacements.at_deck(Point(x=x, y=0, z=z), interp=True)
            #             assert np.isclose(og, ip)
        except ValueError as e:
            if "No fem found" in str(e):
                print_i("Simulation failed. Time to plot results")
                break
            else:
                raise e

    plot_nesw_convergence(
        c=og_c,
        df=df,
        responses=all_strains,
        point=nesw_point,
        max_distance=nesw_max_dist,
        from_=f"the NW point of pier {pier_i}",
    )
    filepath = og_c.get_image_path(
        "convergence-pier",
        safe_str(f"{og_c.bridge.name}-{process}-convergence-nesw-pier-{pier_i}")
        + ".pdf",
        acc=False,
    )
    plt.savefig(filepath)
    plt.close()

    # For each set of fem remove the removed points.
    # for key, displacements in all_displacements.items():
    #     all_displacements[key] = displacements.without(without)
    #     print(f"Filtering displacements with max shell len {key}", end="\r")
    # print()

    # Plot convergence of strain, first with all sensors, then without some.
    title = f"Strain convergence as a function of model size\ndue to settlement of pier {pier_i}"
    plot_mmm_strain_convergence(
        c=og_c, pier=pier, df=df, all_strains=all_strains, title=title, append="0"
    )
    plot_mmm_strain_convergence(
        c=og_c,
        pier=pier,
        df=df,
        all_strains=all_strains,
        title=title,
        without=without,
        append=f"{strain_ignore_radius}",
    )


def make_convergence_data(c: Config, x: float = 34.955, z: float = 29.226 - 16.6):
    """Make convergence data file, increasing mesh density per simulation."""
    load_point = Point(x=x, y=0, z=z)
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
    # then there will be an increase in nodes where fem are large, thus
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
    # Header information for a second file, recording strain close to the load.
    strain_path = c.get_image_path("convergence", "strain-inf.txt", bridge=False)
    with open(strain_path, "w") as f:
        # Simulation parameters, direction recording, and recordings.
        f.write("max_mesh,decknodes,piernodes,dir,recs")

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
                        og = bridge_sim.sim.responses.responses[0][x][0][z].value
                        ip = displacements.at_deck(Point(x=x, y=0, z=z), interp=True)
                        assert np.isclose(og, ip)

            # Determine min, max and mean displacements.
            all_displacements = np.array(list(displacements.values()))
            grid_displacements = np.array(
                [displacements.at_deck(point, interp=True) for point in grid]
            )

            # Minimum displacement is under the load.
            min_d = scalar(np.min(all_displacements))
            max_d = scalar(np.max(grid_displacements))
            mean_d = scalar(np.mean(grid_displacements))

            strains = load_fem_responses(
                c=c,
                sim_params=fem_params,
                response_type=ResponseType.Strain,
                sim_runner=OSRunner(c),
            )
            all_strains = np.array(list(strains.values()))
            grid_strains = np.array(
                [strains.at_deck(point, interp=True) for point in grid]
            )
            min_s = scalar(np.min(grid_strains))
            # Maximum strain is under the load.
            max_s = scalar(np.max(all_strains))
            mean_s = scalar(np.mean(grid_strains))

            # Write results for this simulation to disk.
            with open(path + ".txt", "a") as f:
                f.write(
                    f", {deck_nodes}, {pier_nodes}, {end - start}"
                    f", {min_d}, {max_d}, {mean_d}"
                    f", {min_s}, {max_s}, {mean_s}"
                    f", {avg_shell_size}, {avg_deck_size}, {avg_pier_size}"
                )

            # Also write results of strain recordings, for each direction.
            for dir_name, x_mul, z_mul in [
                ("N", 0, 1),
                ("E", -1, 0),
                ("S", 0, -1),
                ("W", 1, 0),
            ]:
                recordings = []
                for delta in np.arange(0, 5, 0.05):
                    strain_point = Point(
                        x=load_point.x + (delta * x_mul),
                        y=load_point.y,
                        z=load_point.z + (delta * z_mul),
                    )
                    if (
                        strain_point.x < c.bridge.x_min
                        or strain_point.x > c.bridge.x_max
                        or strain_point.z < c.bridge.z_min
                        or strain_point.z > c.bridge.z_max
                    ):
                        break
                    print(strain_point.x, strain_point.z)
                    recordings.append(strains.at_deck(strain_point, interp=True))
                with open(strain_path, "a") as f:
                    f.write(
                        f"\n{max_shell_len}, {deck_nodes}, {pier_nodes}, {dir_name}, {recordings}"
                    )

        except ValueError as e:
            if "No fem found" in str(e):
                print_i("Simulation failed. Time to plot results")
            else:
                raise e


def plot_nesw_strain_convergence(c: Config, filepath: str, from_: str, label: str):
    """Plot convergence of strain at different points around a load."""
    headers = ["max_shell_len", "decknodes", "piernodes", "compass", "fem"]
    parsed_lines = []
    with open(filepath) as f:
        lines = list(map(lambda l: l.split(",", len(headers) - 1), f.readlines()[1:]))
    for max_mesh, deck_nodes, pier_nodes, compass, responses in lines:
        parsed_lines.append(
            [
                float(max_mesh),
                float(deck_nodes),
                float(pier_nodes),
                compass.strip(),
                np.array(
                    list(
                        map(
                            float,
                            responses.replace("[", "").replace("]", "").split(","),
                        )
                    )
                ),
            ]
        )
    df = pd.DataFrame(parsed_lines, columns=headers)
    # First find the maximum distance traversed.
    delta_distance = 0.05
    max_distance = 0
    for compass in ["N", "S", "E", "W"]:
        compass_df = df[df["compass"] == compass]
        responses = compass_df.iloc[0]["fem"]
        max_distance = max(len(responses) * delta_distance, max_distance)
    # Overriding maximum distance.
    # max_distance = 4
    # Create color mappable for distances.
    norm = matplotlib.colors.Normalize(vmin=0, vmax=max_distance)
    cmap = cm.get_cmap("jet")
    mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
    color = lambda d: mappable.to_rgba(d)
    # For each compass point.
    plt.square()
    fig, axes = plt.subplots(nrows=2, ncols=2)
    for ax, compass, compass_name, in zip(
        axes.flat, ["N", "S", "E", "W"], ["North", "South", "East", "West"]
    ):
        # Collect data into fem per max_shell_len.
        lines = {}
        compass_df = df[df["compass"] == compass]
        for df_i, row in compass_df.iterrows():
            lines[row["max_shell_len"]] = row["fem"]
        # Restructure data into lines for plotting.
        max_shell_lens = []
        sorted_lines = []
        for max_shell_len in sorted(lines.keys()):
            max_shell_lens.append(max_shell_len)
            sorted_lines.append(lines[max_shell_len])
        sorted_lines = np.array(sorted_lines).T
        # Finally plot every nth line.
        distance = 0
        skip = 3
        for responses in sorted_lines[::skip]:
            ax.plot(max_shell_lens, responses, color=color(distance))
            distance += skip * delta_distance
            if distance > max_distance:
                break
        ax.set_xlim(2, min(max_shell_lens))
        ax.set_title(
            f"Strain at increasing distance\nin direction {compass_name} from\n{from_}"
        )
        ax.set_xlabel("MSL (m)")
        ax.set_ylabel("Strain")
        ax.grid(axis="y")
    plt.tight_layout()
    clb = plt.colorbar(mappable, ax=axes.ravel())
    clb.ax.set_title("Distance (m)")
    plt.savefig(
        c.get_image_path("convergence", f"convergencestrain-{label}.pdf", bridge=False)
    )
    plt.close()


def plot_convergence(c: Config):
    """Plot convergence as model size is increased.

    Loads files named 'convergence-*', generated by 'make_convergence' and
    renamed manually by you. Note that the '*' indicates the plot label which
    will be put in the legend.

    """
    convergence_dir = os.path.dirname(
        c.get_image_path("convergence", "_", bridge=False)
    )

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

    CHOSEN_NUM_NODES = 24500

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
                num_nodes, maxes_d / final_max_d, color="orange", label="Max. response",
            )
            plt.plot(
                num_nodes, means_d / final_mean_d, color="green", label="Mean response",
            )
            plot_intersection(CHOSEN_NUM_NODES, num_nodes, mins_d / final_min_d, "min")
            plot_intersection(CHOSEN_NUM_NODES, num_nodes, maxes_d / final_max_d, "max")
            plot_intersection(
                CHOSEN_NUM_NODES, num_nodes, means_d / final_mean_d, "mean"
            )
        break

    # plt.xlim(plt.xlim()[1], plt.xlim()[0])
    plt.title("Normalized y translation as a function of number of nodes")
    plt.xlabel("Number of nodes")
    plt.ylabel("Normalized y translation")
    plt.legend()
    plt.savefig(c.get_image_path("convergence", "min-max-displa.pdf", bridge=False))
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
                num_nodes, maxes_s / final_max_s, color="orange", label="Max. response",
            )
            plt.plot(
                num_nodes, means_s / final_mean_s, color="green", label="Mean response",
            )
            plot_intersection(CHOSEN_NUM_NODES, num_nodes, mins_s / final_min_s, "min")
            plot_intersection(CHOSEN_NUM_NODES, num_nodes, maxes_s / final_max_s, "max")
            plot_intersection(
                CHOSEN_NUM_NODES, num_nodes, means_s / final_mean_s, "mean"
            )

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
            plot_intersection(
                CHOSEN_NUM_NODES, num_nodes, shell_size, units="Shell area (m²)"
            )
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
            plot_intersection(
                CHOSEN_NUM_NODES, num_nodes, max_mesh, units="Shell length (m)"
            )
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
            plt.title("Mean shell area")
            plt.xlabel("Mean shell area (m²)")
            plt.ylabel("Mean shell area (m²)")
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
            contour_responses(
                c=c, responses=fem_responses, ploads=loads, title=title,
            )
            plt.savefig(save(""))
            plt.close()


def temp_plots():
    sensors = ["TA", "TB", "TC", "U13", "U26", "U29"]
    data_path = "validation/sensors"
    times, temps, responses = [], [], [[] for _ in sensors]
    for i in range(1, 13 + 1):
        # Times.
        times_path = os.path.join(data_path, f"times{i}.csv")
        with open(times_path) as f:
            lines = f.read().split(",")
        parse_time = lambda l: datetime.strptime(l.split()[1], "%H:%M:%S")
        times.append(list(map(parse_time, lines)))
        # Temps.
        temps_path = os.path.join(data_path, f"temps{i}.csv")
        with open(temps_path) as f:
            lines = f.read().split(",")
        temps.append(list(map(float, lines)))
        assert len(times[-1]) == len(temps[-1])
        # Sensors.
        for s_i, sensor in enumerate(sensors):
            sensor_path = os.path.join(data_path, f"{sensor}{i}.csv")
            with open(sensor_path) as f:
                lines = f.read().split(",")
            sensor_responses = list(map(float, lines))
            responses[s_i].append(sensor_responses)
            assert len(responses[s_i][-1]) == len(temps[-1])
    # Plot times versus temperatures.
    all_times = np.concatenate(times)
    all_temps = np.concatenate(temps)
    assert len(all_times) == len(all_temps)
    plt.scatter(all_times, all_temps)
    plt.title("Time versus temperature")
    plt.show()
    for s_i, sensor in enumerate(sensors):
        # sensor_responses = np.concatenate(fem[s_i])
        sensor_responses = [responses[s_i][i][0] for i in range(13)]
        plot_temps = [temps[i][0] for i in range(13)]
        # assert len(sensor_responses) == len(all_times)
        plt.scatter(plot_temps, sensor_responses)
        plt.show()
