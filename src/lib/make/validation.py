import os

import numpy as np
import pandas as pd
from matplotlib import image as mpimg

from bridge_sim import sim
from bridge_sim.model import Config, ResponseType, PointLoad, PierSettlement
from bridge_sim.sim.model import SimParams
from bridge_sim.sim.run import load_fem_responses
from bridge_sim.sim.run.opensees import OSRunner
from bridge_sim.util import safe_str, project_dir
from lib.plot import axis_cmap_r, plt
from lib.plot.geometry import top_view_bridge
from lib.plot.responses import plot_contour_deck


def unit_loads(c: Config, run_only: bool, scatter: bool):
    """Contour plots of unit loads, OpenSees and AxisVM."""
    positions = [
        (35, 9.65, "a"),
        (51.375, 0, "b"),
        (92.4, -7.15, "c"),
        (101.75, -9.65, "d"),
    ]
    min_max_values = pd.read_csv(os.path.join(project_dir(), "data/validation/axis/min-max.csv"))
    response_types = [ResponseType.YTrans, ResponseType.StrainXXB]
    # For each combination of response type and loading position.
    for load_x, load_z, label in positions:
        for response_type in response_types:
            # Setup the metadata.
            if response_type == ResponseType.YTrans:
                rt_str = "displa"
                unit_str = "mm"
            elif response_type == ResponseType.StrainXXB:
                rt_str = "strain"
                unit_str = ""
            else:
                raise ValueError("Unsupported response type")
            # Read the min max values.
            row = min_max_values[min_max_values["name"] == f"{label}-{rt_str}"]
            tmin, tmax = float(row["dmin"]), float(row["dmax"])
            omin, omax = float(row["omin"]), float(row["omax"])
            amin, amax = max(tmin, omin), min(tmax, omax)
            levels = np.linspace(amin, amax, 16)
            # Create the OpenSees plot.
            point_loads = [PointLoad(x=load_x, z=load_z, load=100)]
            os_responses = sim.responses.load(
                config=c,
                response_type=response_type,
                point_loads=point_loads,
            )
            if response_type.is_strain():
                os_responses = os_responses.to_stress(c.bridge).map(lambda x: x * 1E-6)
                os_responses.units = "N/mm²"
            else:
                os_responses.units = "mm"
                os_responses = os_responses.map(lambda x: x * 1E3)
            if run_only:
                continue
            title = (
                f"{os_responses.response_type.name()} from a {point_loads[0].load} kN point load at"
                + f"\nx = {np.round(load_x, 3)} m, z = {np.round(load_z, 3)} m, with "
            )
            save = lambda prefix: c.get_image_path(
                "validation/unit-load",
                safe_str(f"{prefix}{response_type.name()}") + ".pdf",
            )
            top_view_bridge(c.bridge, piers=True, abutments=True, units="M")
            sci_format = False
            plot_contour_deck(
                c=c,
                responses=os_responses,
                point_loads=point_loads,
                cmap=axis_cmap_r,
                levels=levels,
                sci_format=sci_format,
                decimals=3,
                scatter=scatter,
            )
            plt.legend()
            plt.title(title + "OpenSees")
            plt.tight_layout()
            plt.savefig(save(f"{label}-"))
            plt.close()

            # Finally create label/title the Axis plot.
            if label is not None:
                # First plot and clear, just to have the same colorbar.
                plot_contour_deck(
                    c=c, responses=os_responses, cmap=axis_cmap_r, levels=levels
                )
                plt.cla()
                # Then plot the bridge and Axis image.
                top_view_bridge(c.bridge, piers=True, abutments=True, units="M")
                plt.imshow(
                    mpimg.imread(os.path.join(project_dir(), f"data/validation/axis/{label}-{rt_str}.png")),
                    extent=(
                        c.bridge.x_min,
                        c.bridge.x_max,
                        c.bridge.z_min,
                        c.bridge.z_max,
                    ),
                )
                tmin_s = f"{tmin:.3e}" if sci_format else f"{tmin:.3f}"
                tmax_s = f"{tmax:.3e}" if sci_format else f"{tmax:.3f}"
                tabs_s = (
                    f"{abs(tmin - tmax):.3e}"
                    if sci_format
                    else f"{abs(tmin - tmax):.3f}"
                )
                for point, leg_label, color, alpha in [
                    ((load_x, load_z), f"{point_loads[0].load} kN load", "black", 1),
                    ((0, 0), f"min = {tmin_s} {os_responses.units}", "r", 0),
                    ((0, 0), f"max = {tmax_s} {os_responses.units}", "r", 0),
                    ((0, 0), f"|min-max| = {tabs_s} {os_responses.units}", "r", 0),
                ]:
                    plt.scatter(
                        [point[0]],
                        [point[1]],
                        label=leg_label,
                        marker="o",
                        color=color,
                        alpha=alpha,
                    )
                plt.legend()
                plt.title(title + "AxisVM")
                plt.xlabel("X position (m)")
                plt.ylabel("Z position (m)")
                plt.tight_layout()
                plt.savefig(save(f"{label}-diana-"))
                plt.close()


def pier_settlement(c: Config):
    """Contour plots of pier settlement, OpenSees and AxisVM."""
    pier_indices = [4, 5]
    response_types = [ResponseType.YTranslation, ResponseType.Strain]
    axis_values = pd.read_csv("validation/axis-screenshots/piers-min-max.csv")
    for r_i, response_type in enumerate(response_types):
        for p in pier_indices:
            # Run the simulation and collect fem.
            sim_responses = load_fem_responses(
                c=c,
                response_type=response_type,
                sim_runner=OSRunner(c),
                sim_params=SimParams(
                    displacement_ctrl=PierSettlement(
                        displacement=c.pd_unit_disp, pier=p
                    ),
                ),
            )

            # In the case of stress we map from kn/m2 to kn/mm2 (E-6) and then
            # divide by 1000, so (E-9).
            assert c.pd_unit_disp == 1
            if response_type == ResponseType.Strain:
                sim_responses.to_stress(c.bridge).map(lambda r: r * 1e-9)

            # Get min and max values for both Axis and OpenSees.
            rt_str = (
                "displa" if response_type == ResponseType.YTranslation else "stress"
            )
            row = axis_values[axis_values["name"] == f"{p}-{rt_str}"]
            dmin, dmax = float(row["dmin"]), float(row["dmax"])
            omin, omax = float(row["omin"]), float(row["omax"])
            amin, amax = max(dmin, omin), min(dmax, omax)
            levels = np.linspace(amin, amax, 16)

            # Plot and save the image. If plotting strains use Axis values for
            # colour normalization.

            cmap = axis_cmap_r
            top_view_bridge(c.bridge, abutments=True, piers=True)
            plot_contour_deck(c=c, cmap=cmap, responses=sim_responses, levels=levels)
            plt.tight_layout()
            plt.title(
                f"{sim_responses.response_type.name()} from 1mm pier settlement with OpenSees"
            )
            plt.savefig(
                c.get_image_path(
                    "validation/pier-displacement",
                    safe_str(f"pier-{p}-{sim_responses.response_type.name()}") + ".pdf",
                )
            )
            plt.close()

            # First plot and clear, just to have the same colorbar.
            plot_contour_deck(c=c, responses=sim_responses, cmap=cmap, levels=levels)
            plt.cla()
            # Save the axis plots.
            axis_img = mpimg.imread(f"validation/axis-screenshots/{p}-{rt_str}.png")
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
            for point, leg_label, color in [
                ((0, 0), f"min = {np.around(dmin, 3)} {sim_responses.units}", "r"),
                ((0, 0), f"max = {np.around(dmax, 3)} {sim_responses.units}", "r"),
                (
                    (0, 0),
                    f"|min-max| = {np.around(abs(dmax - dmin), 3)} {sim_responses.units}",
                    "r",
                ),
            ]:
                plt.scatter(
                    [point[0]],
                    [point[1]],
                    label=leg_label,
                    marker="o",
                    color=color,
                    alpha=0,
                )
            if response_type == ResponseType.YTranslation:
                plt.legend()
            # Title and save.
            plt.title(f"{response_type.name()} from 1mm pier settlement with AxisVM")
            plt.xlabel("X position (m)")
            plt.ylabel("Z position (m)")
            plt.tight_layout()
            plt.savefig(
                c.get_image_path(
                    "validation/pier-displacement", f"{p}-axis-{rt_str}.pdf",
                )
            )
            plt.close()