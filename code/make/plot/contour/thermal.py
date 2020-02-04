from copy import deepcopy

import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from matplotlib.cm import get_cmap

from classify.scenario.bridge import thermal_damage
from config import Config
from fem.params import SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from model.response import ResponseType
from plot import plt
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck
from util import safe_str


def unit_axial_thermal_deck_load(c: Config, run: bool):
    """Response to unit axial thermal deck loading."""
    damage_scenario = thermal_damage(axial_delta_temp=c.unit_axial_delta_temp_c)
    c, sim_params = damage_scenario.use(c)
    for i, response_type in enumerate(ResponseType.all()):
        is_stress = response_type == ResponseType.Stress
        sim_responses = load_fem_responses(
            c=c,
            sim_runner=OSRunner(c),
            response_type=ResponseType.Strain if is_stress else response_type,
            sim_params=sim_params,
            run=run and i == 0,
        )
        if is_stress:
            og_sim_responses = deepcopy(sim_responses)
            sim_responses = damage_scenario.to_stress(c=c, sim_responses=sim_responses)
            for response, (x, y, z) in og_sim_responses.values(point=True):
                assert np.isclose(
                    (response * 1E-6 - (c.cte * c.unit_axial_delta_temp_c)) * c.bridge.sections[0].youngs,
                    sim_responses.responses[0][x][y][z]
                )
        sim_responses = sim_responses.resize()
        top_view_bridge(bridge=c.bridge, abutments=True, piers=True)
        plot_contour_deck(c=c, responses=sim_responses, levels=25)
        plt.title(f"{sim_responses.response_type.name()} from {c.unit_axial_delta_temp_c}‎°C axial thermal deck loading in OpenSees")
        plt.tight_layout()
        plt.savefig(c.get_image_path(
            "validation/thermal",
            safe_str(f"thermal-deck-unit-axial_load-{sim_responses.response_type.name()})") + ".pdf",
        ))
        plt.close()


def unit_moment_thermal_deck_load(c: Config, run: bool):
    """Response to unit moment thermal deck loading."""
    damage_scenario = thermal_damage(moment_delta_temp=c.unit_moment_delta_temp_c)
    c, sim_params = damage_scenario.use(c)
    for i, response_type in enumerate(ResponseType.all()):
        is_stress = response_type == ResponseType.Stress
        sim_responses = load_fem_responses(
            c=c,
            sim_runner=OSRunner(c),
            response_type=ResponseType.Strain if is_stress else response_type,
            sim_params=sim_params,
            run=run and i == 0,
        )
        if is_stress:
            og_sim_responses = deepcopy(sim_responses)
            sim_responses = damage_scenario.to_stress(c=c, sim_responses=sim_responses)
            for response, (x, y, z) in og_sim_responses.values(point=True):
                assert np.isclose(
                    (response * 1E-6 + (0.5 * c.cte * c.unit_axial_delta_temp_c)) * c.bridge.sections[0].youngs,
                    sim_responses.responses[0][x][y][z]
                )
        sim_responses = sim_responses.resize()
        top_view_bridge(bridge=c.bridge, abutments=True, piers=True)
        plot_contour_deck(c=c, responses=sim_responses, levels=25)
        plt.title(f"{sim_responses.response_type.name()} from {c.unit_moment_delta_temp_c}‎°C moment thermal deck loading in OpenSees")
        plt.tight_layout()
        plt.savefig(c.get_image_path(
            "validation/thermal",
            safe_str(f"thermal-deck-unit-moment_load-{sim_responses.response_type.name()})") + ".pdf",
        ))
        plt.close()


def make_axis_plots(c: Config):
    """Create AxisVM plots for thermal loading."""
    axis_values = pd.read_csv("validation/axis-screenshots/thermal-min-max.csv")
    for response_type, rt_name, rt_units in [
        (ResponseType.XTranslation, "xtrans", "mm"),
        (ResponseType.YTranslation, "ytrans", "mm"),
        (ResponseType.ZTranslation, "ztrans", "mm"),
        (ResponseType.Stress, "stress", "m/m"),
    ]:
        for thermal_type in ["axial"]:
            axis_img = mpimg.imread(
                f"validation/axis-screenshots/thermal-{rt_name}-{thermal_type}.png"
            )
            top_view_bridge(c.bridge, abutments=True)
            plt.imshow(
                axis_img,
                extent=(
                    c.bridge.x_min,
                    c.bridge.x_max,
                    c.bridge.z_min,
                    c.bridge.z_max,
                ),
            )
            # Plot the load and min, max values.
            row = axis_values[axis_values["name"] == f"{rt_name}-{thermal_type}"]
            amin, amax = float(row["min"]), float(row["max"])
            if response_type == ResponseType.Strain:
                amax, amin = -amin * 1e6, -amax * 1e6
            for point, leg_label, color in [
                ((0, 0), f"min = {amin:.3f} {rt_units}", "r"),
                ((0, 0), f"max = {amax:.3f} {rt_units}", "r"),
                ((0, 0), f"|min-max| = {abs(amax - amin):.3f} {rt_units}", "r"),
            ]:
                plt.scatter(
                    [point[0]],
                    [point[1]],
                    label=leg_label,
                    marker="o",
                    color=color,
                    alpha=0,
                )
            plt.legend()
            # Add the Axis colorbar.
            plt.imshow(
                np.array([[amin, amax]]), cmap=get_cmap("jet"), extent=(0, 0, 0, 0)
            )
            clb = plt.colorbar()
            clb.ax.set_title(rt_units)
            # Title and save.
            plt.title(
                f"{response_type.name()} from 1‎°C {thermal_type} thermal deck"
                f" loading in AxisVM"
            )
            plt.xlabel("X position (m)")
            plt.ylabel("Z position (m)")
            plt.tight_layout()
            plt.savefig(
                c.get_image_path(
                    "validation/thermal", f"axis-{rt_name}-{thermal_type}.pdf",
                )
            )
            plt.close()
