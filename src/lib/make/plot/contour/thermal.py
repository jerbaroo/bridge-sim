from copy import deepcopy

import matplotlib as mpl
import numpy as np
import pandas as pd

from classify.scenario.bridge import thermal_damage
from config import Config
from fem.params import SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from model.response import ResponseType
from plot import axis_cmap_r, axis_colors, plt
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck
from util import safe_str


def unit_axial_thermal_deck_load(c: Config, run: bool):
    """Response to unit axial thermal deck loading."""
    damage_scenario = thermal_damage(axial_delta_temp=c.unit_axial_delta_temp_c)
    c, sim_params = damage_scenario.use(c)
    axis_values = pd.read_csv("validation/axis-screenshots/thermal-min-max.csv")
    for i, response_type in enumerate(
        [ResponseType.Stress, ResponseType.YTranslation, ResponseType.StressZZB]
    ):
        # Get min and max values for both Axis and OpenSees.
        rt_name = "stress" if response_type == ResponseType.Stress else "ytrans"
        if response_type == ResponseType.StressZZB:
            rt_name = "stress_zzb"
        # The rt_name is used to extract min and max values for 'levels'..
        try:
            row = axis_values[axis_values["name"] == f"{rt_name}-axial"]
            dmin, dmax = float(row["dmin"]), float(row["dmax"])
            omin, omax = float(row["omin"]), float(row["omax"])
            amin, amax = max(dmin, omin), min(dmax, omax)
            amin, amax = np.around(max(dmin, omin), 2), np.around(min(dmax, omax), 2)
            levels = np.linspace(amin, amax, 16)
        # .. but if these values are not available we don't use levels.
        except:
            levels = None
        levels = None
        # Load responses, strain in case of stress.
        sim_type = ResponseType.YTranslation
        if response_type == ResponseType.Stress:
            sim_type = ResponseType.Strain
        elif response_type == ResponseType.StressZZB:
            sim_type = ResponseType.StrainZZB
        sim_responses = load_fem_responses(
            c=c,
            sim_runner=OSRunner(c),
            response_type=sim_type,
            sim_params=sim_params,
            run=run and i == 0,
        )
        if response_type in [ResponseType.Stress, ResponseType.StressZZB]:
            # og_sim_responses = deepcopy(sim_responses)
            sim_responses = damage_scenario.to_stress(c=c, sim_responses=sim_responses)
            # for response, (x, y, z) in og_sim_responses.values(point=True):
            #     assert np.isclose(
            #         (response * 1E-6 - (c.cte * c.unit_axial_delta_temp_c)) * c.bridge.sections[0].youngs,
            #         sim_responses.responses[0][x][y][z]
            #     )
        sim_responses = sim_responses.resize()
        top_view_bridge(bridge=c.bridge, abutments=True, piers=True)
        plot_contour_deck(c=c, responses=sim_responses, cmap=axis_cmap_r, levels=14)
        plt.title(
            f"{sim_responses.response_type.name()} from {c.unit_axial_delta_temp_c}‎°C uniform temp. deck loading with OpenSees"
        )
        plt.tight_layout()
        plt.savefig(
            c.get_image_path(
                "validation/thermal",
                safe_str(f"thermal-deck-unit-axial_load-{rt_name})") + ".pdf",
            )
        )
        plt.close()

        if response_type == ResponseType.StressZZB:
            continue

        # Load the axis image.
        axis_img = mpl.image.imread(
            f"validation/axis-screenshots/thermal-{rt_name}-axial.png"
        )
        # First plot and clear, just to have the same colorbar.
        plot_contour_deck(c=c, responses=sim_responses, cmap=axis_cmap_r, levels=levels)
        plt.cla()
        # Then imshow the axis image.
        top_view_bridge(bridge=c.bridge, abutments=True)
        plt.imshow(
            axis_img,
            extent=(c.bridge.x_min, c.bridge.x_max, c.bridge.z_min, c.bridge.z_max,),
        )
        # Plot the min and max values.
        for leg_label, color in [
            (f"min = {dmin:.3f} {sim_responses.units}", "r"),
            (f"max = {dmax:.3f} {sim_responses.units}", "r"),
            (f"|min-max| = {abs(dmax - dmin):.3f} {sim_responses.units}", "r"),
        ]:
            plt.scatter(
                [0], [0], label=leg_label, marker="o", color=color, alpha=0,
            )
        plt.legend()
        # Title and save.
        plt.title(
            f"{response_type.name()} from 1‎°C uniform temp. deck"
            f" loading with AxisVM"
        )
        plt.xlabel("X position (m)")
        plt.ylabel("Z position (m)")
        plt.tight_layout()
        plt.savefig(
            c.get_image_path("validation/thermal", f"axis-{rt_name}-axial.pdf",)
        )
        plt.close()


def unit_moment_thermal_deck_load(c: Config, run: bool):
    """Response to unit moment thermal deck loading."""
    damage_scenario = thermal_damage(moment_delta_temp=c.unit_moment_delta_temp_c)
    c, sim_params = damage_scenario.use(c)
    axis_values = pd.read_csv("validation/axis-screenshots/thermal-min-max.csv")
    for i, response_type in enumerate(
        [ResponseType.Stress, ResponseType.StressZZB, ResponseType.YTranslation]
    ):
        # Get min and max values for both Axis and OpenSees.
        rt_name = "stress" if response_type == ResponseType.Stress else "ytrans"
        if response_type == ResponseType.StressZZB:
            rt_name = "stress_zzb"
        # The rt_name is used to extract min and max values for 'levels'..
        try:
            row = axis_values[axis_values["name"] == f"{rt_name}-moment"]
            dmin, dmax = float(row["dmin"]), float(row["dmax"])
            omin, omax = float(row["omin"]), float(row["omax"])
            amin, amax = np.around(max(dmin, omin), 2), np.around(min(dmax, omax), 2)
            levels = np.linspace(amin, amax, 16)
        # .. but if these values are not available we don't use levels.
        except:
            levels = None
        # Load responses, strain in case of stress.
        sim_type = ResponseType.YTranslation
        if response_type == ResponseType.Stress:
            sim_type = ResponseType.Strain
        elif response_type == ResponseType.StressZZB:
            sim_type = ResponseType.StrainZZB
        sim_responses = load_fem_responses(
            c=c,
            sim_runner=OSRunner(c),
            response_type=sim_type,
            sim_params=sim_params,
            run=run and i == 0,
        )
        if response_type in [ResponseType.Stress, ResponseType.StressZZB]:
            # og_sim_responses = deepcopy(sim_responses)
            sim_responses = damage_scenario.to_stress(c=c, sim_responses=sim_responses)
            # for response, (x, y, z) in og_sim_responses.values(point=True):
            #     assert np.isclose(
            #         (response * 1E-6 + (0.5 * c.cte * c.unit_axial_delta_temp_c)) * c.bridge.sections[0].youngs,
            #         sim_responses.responses[0][x][y][z]
            #     )
        sim_responses = sim_responses.resize()
        top_view_bridge(bridge=c.bridge, abutments=True, piers=True)
        plot_contour_deck(c=c, responses=sim_responses, cmap=axis_cmap_r, levels=levels)
        plt.title(
            f"{sim_responses.response_type.name()} from {c.unit_moment_delta_temp_c}‎°C linear temp. deck loading with OpenSees"
        )
        plt.tight_layout()
        plt.savefig(
            c.get_image_path(
                "validation/thermal",
                safe_str(f"thermal-deck-unit-moment_load-{rt_name})") + ".pdf",
            )
        )
        plt.close()

        if response_type == ResponseType.StressZZB:
            continue

        # Load the axis image.
        axis_img = mpl.image.imread(
            f"validation/axis-screenshots/thermal-{rt_name}-moment.png"
        )
        # First plot and clear, just to have the same colorbar.
        plot_contour_deck(c=c, responses=sim_responses, cmap=axis_cmap_r, levels=levels)
        plt.cla()
        # Then imshow the axis image.
        top_view_bridge(bridge=c.bridge, abutments=True)
        plt.imshow(
            axis_img,
            extent=(c.bridge.x_min, c.bridge.x_max, c.bridge.z_min, c.bridge.z_max,),
        )
        # Plot the min and max values.
        for leg_label, color in [
            (f"min = {dmin:.3f} {sim_responses.units}", "r"),
            (f"max = {dmax:.3f} {sim_responses.units}", "r"),
            (f"|min-max| = {abs(dmax - dmin):.3f} {sim_responses.units}", "r"),
        ]:
            plt.scatter(
                [0], [0], label=leg_label, marker="o", color=color, alpha=0,
            )
        plt.legend()
        # Title and save.
        plt.title(
            f"{response_type.name()} from 1‎°C linear temp. deck"
            f" loading with AxisVM"
        )
        plt.xlabel("X position (m)")
        plt.ylabel("Z position (m)")
        plt.tight_layout()
        plt.savefig(
            c.get_image_path("validation/thermal", f"axis-{rt_name}-moment.pdf",)
        )
        plt.close()
