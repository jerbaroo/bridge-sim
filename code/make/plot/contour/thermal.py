import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from matplotlib.cm import get_cmap

from classify.scenario.bridge import ThermalDamage
from config import Config
from make.plot.contour.common import damage_scenario_plot
from model.response import ResponseType
from plot import plt
from plot.geometry import top_view_bridge
from util import safe_str


def unit_axial_thermal_deck_load(c: Config, run: bool):
    """Response to unit axial thermal deck loading."""
    response_types = [
        ResponseType.XTranslation,
        ResponseType.YTranslation,
        ResponseType.ZTranslation,
    ]
    damage_scenario_plot(
        c=c,
        response_types=response_types,
        damage_scenario=ThermalDamage(axial_delta_temp=c.unit_axial_delta_temp_c),
        titles=[
            f"{rt.name()} to {c.unit_axial_delta_temp_c}C axial thermal loading of the deck"
            for rt in response_types
        ],
        saves=[
            c.get_image_path(
                "validation/thermal",
                safe_str(f"thermal-deck-unit-axial_load-{rt.name()})") + ".pdf",
            )
            for rt in response_types
        ],
        run=run,
        levels=14,
    )


def unit_moment_thermal_deck_load(c: Config):
    """Response to unit moment thermal deck loading."""
    response_types = [
        ResponseType.XTranslation,
        ResponseType.YTranslation,
        ResponseType.ZTranslation,
    ]
    damage_scenario_plot(
        c=c,
        response_types=response_types,
        damage_scenario=ThermalDamage(moment_delta_temp=c.unit_moment_delta_temp_c),
        titles=[
            f"{rt.name()} to {c.unit_moment_delta_temp_c}C moment thermal loading of the deck"
            for rt in response_types
        ],
        saves=[
            c.get_image_path(
                "validation/thermal",
                safe_str(f"thermal-deck-unit-moment_load-{rt.name()})") + ".pdf",
            )
            for rt in response_types
        ],
    )


def unit_thermal_deck_load(c: Config):
    """Response to unit thermal deck loading."""
    response_types = [
        ResponseType.XTranslation,
        ResponseType.YTranslation,
        ResponseType.ZTranslation,
    ]
    damage_scenario_plot(
        c=c,
        response_types=response_types,
        damage_scenario=ThermalDamage(
            axial_delta_temp=c.unit_axial_delta_temp_c,
            moment_delta_temp=c.unit_moment_delta_temp_c,
        ),
        titles=[
            f"{rt.name()} to {c.unit_axial_delta_temp_c}C axial and \n {c.unit_moment_delta_temp_c}C moment thermal loading of the deck"
            for rt in response_types
        ],
        saves=[
            c.get_image_path(
                "validation/thermal",
                safe_str(f"thermal-unit-load-{rt.name()})") + ".pdf",
            )
            for rt in response_types
        ],
    )


def make_axis_plots(c: Config):
    """Create AxisVM plots for thermal loading."""
    axis_values = pd.read_csv("validation/axis-screenshots/thermal-min-max.csv")
    for response_type, rt_name, rt_units in [
        (ResponseType.YTranslation, "displa", "mm")
    ]:
        for thermal_type in ["axial"]:
            for direction in ["x", "y", "z"]:
                axis_img = mpimg.imread(
                    f"validation/axis-screenshots/thermal-{direction}-{thermal_type}-{rt_name}.png"
                )
                top_view_bridge(c.bridge, piers=True, abutments=True)
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
                row = axis_values[
                    axis_values["name"] == f"{direction}-{thermal_type}-{rt_name}"
                ]
                amin, amax = float(row["min"]), float(row["max"])
                if response_type == ResponseType.Strain:
                    amax, amin = -amin * 1e6, -amax * 1e6
                for point, leg_label, color in [
                    ((0, 0), f"min = {amin:.2f} {rt_units}", "r"),
                    ((0, 0), f"max = {amax:.2f} {rt_units}", "r"),
                    ((0, 0), f"|min-max| = {abs(amax - amin):.2f} {rt_units}", "r"),
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
                plt.title(f"Pier displacement of 1 m")
                plt.xlabel("X position (mm)")
                plt.ylabel("Z position (mm)")
                plt.savefig(
                    c.get_image_path(
                        "validation/thermal",
                        f"axis-{direction}-{thermal_type}-{rt_name}.pdf",
                    )
                )
                plt.close()
