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
    # Raw responses being collected.
    response_types = [
        ResponseType.XTranslation,
        ResponseType.YTranslation,
        ResponseType.ZTranslation,
        ResponseType.Strain,
        ResponseType.Strain,
    ]
    # Response types being plotted.
    final_response_types = response_types[:]
    final_response_types[-1] = ResponseType.Stress
    # Map from raw responses to responses and units for plotting. The
    # displacements are converted from meter to millimeter, and the strains are
    # converted to real strains and then converted to stresses.
    map_responses = [(lambda x: x, rt.units()) for rt in response_types]
    for i in [0, 1, 2]:
        map_responses[i] = ((lambda r: r.map(lambda v: v * 1000)), "mm")
    def to_stress(s):
        s = s.strain_to_real_strain(c.cte * 1E+6)
        s = s.deck_strain_to_stress(bridge=c.bridge, times=1E-6)
        return s
    map_responses[-1] = (to_stress, ResponseType.Stress.units())
    # Put it all together for plotting purposes.
    damage_scenario_plot(
        c=c,
        response_types=response_types,
        damage_scenario=ThermalDamage(axial_delta_temp=c.unit_axial_delta_temp_c),
        titles = [
            f"{rt.name()} from {c.unit_axial_delta_temp_c}‎°C axial thermal deck loading in OpenSees"
            for rt in final_response_types
        ],
        saves=[
            c.get_image_path(
                "validation/thermal",
                safe_str(f"thermal-deck-unit-axial_load-{rt.name()})") + ".pdf",
            )
            for rt in final_response_types
        ],
        run=run,
        levels=14,
        map_responses=map_responses,
    )


def unit_moment_thermal_deck_load(c: Config, run: bool):
    """Response to unit moment thermal deck loading."""
    response_types = [
        ResponseType.XTranslation,
        ResponseType.YTranslation,
        ResponseType.ZTranslation,
        ResponseType.Strain,
    ]
    damage_scenario_plot(
        c=c,
        response_types=response_types,
        damage_scenario=ThermalDamage(moment_delta_temp=c.unit_moment_delta_temp_c),
        titles=[
            f"{rt.name()} from {c.unit_moment_delta_temp_c}‎°C moment thermal deck loading in OpenSees"
            for rt in response_types
        ],
        saves=[
            c.get_image_path(
                "validation/thermal",
                safe_str(f"thermal-deck-unit-moment_load-{rt.name()})") + ".pdf",
            )
            for rt in response_types
        ],
        run=run,
        levels=14,
    )


def unit_thermal_deck_load(c: Config, run: bool):
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
            f"{rt.name()} from {c.unit_axial_delta_temp_c}‎°C axial and \n {c.unit_moment_delta_temp_c}C moment thermal loading of the deck"
            for rt in response_types
        ],
        saves=[
            c.get_image_path(
                "validation/thermal",
                safe_str(f"thermal-unit-load-{rt.name()})") + ".pdf",
            )
            for rt in response_types
        ],
        run=run,
        levels=14,
    )


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
                    "validation/thermal",
                    f"axis-{rt_name}-{thermal_type}.pdf",
                )
            )
            plt.close()
