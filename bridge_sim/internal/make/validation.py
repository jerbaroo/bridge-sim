import os

import bridge_sim.plot
import matplotlib as mpl
import numpy as np
import pandas as pd
from matplotlib import image as mpimg

from bridge_sim import sim, plot
from bridge_sim.model import Config, ResponseType, PointLoad, PierSettlement
from bridge_sim.util import safe_str, project_dir, print_w, print_i
from bridge_sim.internal.plot import axis_cmap_r, plt
from bridge_sim.plot import contour_responses, top_view_bridge


def unit_loads(c: Config, scatter: bool):
    """Contour plots of unit loads, OpenSees and AxisVM."""
    positions = [
        (35, 9.65, "a"),
        (51.375, 0, "b"),
        (92.4, -7.15, "c"),
        (101.75, -9.65, "d"),
    ]
    min_max_values = pd.read_csv(
        os.path.join(project_dir(), "data/validation/axis/min-max.csv")
    )
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
            point_loads = [PointLoad(x=load_x, z=load_z, load=100 * 1e3)]  # 100 kN.
            os_responses = sim.responses.load(
                config=c, response_type=response_type, point_loads=point_loads,
            )
            if response_type.is_strain():
                os_responses = os_responses.to_stress(c.bridge)
                os_responses.units = "N/mm²"
            else:
                os_responses.units = "mm"
                os_responses = os_responses.map(lambda x: x * 1e3)
            title = (
                f"{os_responses.response_type.name()} from a {int(point_loads[0].load / 1E3)} kN point load at"
                + f"\nx = {np.round(load_x, 3)} m, z = {np.round(load_z, 3)} m, with "
            )
            save = lambda prefix: c.get_image_path(
                "verification/point-load",
                safe_str(f"{prefix}{response_type.name()}") + ".pdf",
            )
            top_view_bridge(
                c.bridge, piers=True, abutments=True, units="m", compass=True
            )
            contour_responses(
                config=c,
                responses=os_responses,
                point_loads=[
                    PointLoad(x=p.x, z=p.z, load=int(p.load / 1e3), units="kN")
                    for p in point_loads
                ],
                cmap=axis_cmap_r,
                levels=levels,
                scatter=scatter,
                interp=(200, 60),
            )
            plt.legend()
            plt.title(title + "OpenSees")
            plt.tight_layout()
            plt.savefig(save(f"{label}-"))
            plt.close()

            # Finally create label/title the Axis plot.
            if label is not None:
                # First plot and clear, just to have the same colorbar.
                contour_responses(
                    config=c, responses=os_responses, cmap=axis_cmap_r, levels=levels
                )
                plt.cla()
                # Then plot the bridge and Axis image.
                top_view_bridge(
                    c.bridge, piers=True, abutments=True, units="m", compass=True
                )
                plt.imshow(
                    mpimg.imread(
                        os.path.join(
                            project_dir(), f"data/validation/axis/{label}-{rt_str}.PNG"
                        )
                    ),
                    extent=(
                        c.bridge.x_min,
                        c.bridge.x_max,
                        c.bridge.z_min,
                        c.bridge.z_max,
                    ),
                )
                tmin_s = f"{tmin:.3f}"
                tmax_s = f"{tmax:.3f}"
                tabs_s = f"{abs(tmin - tmax):.3f}"
                for point, leg_label, color, alpha in [
                    (
                        (load_x, load_z),
                        f"{int(point_loads[0].load / 1e3)} kN load",
                        "black",
                        1,
                    ),
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
                plt.savefig(save(f"{label}-axis-"))
                plt.close()


def pier_settlement(c: Config):
    """Contour plots of pier settlement, OpenSees and AxisVM."""
    pier_indices = [4, 5]
    response_types = [ResponseType.YTrans, ResponseType.StrainXXB]
    axis_values = pd.read_csv(
        os.path.join(project_dir(), "data/validation/axis/piers-min-max.csv")
    )
    for r_i, response_type in enumerate(response_types):
        for p in pier_indices:
            # Run the simulation and collect fem.
            sim_responses = sim.responses.load(
                config=c,
                response_type=response_type,
                pier_settlement=[PierSettlement(pier=p, settlement=1 / 1e3)],
            )
            if response_type.is_strain():
                sim_responses.to_stress(c.bridge)
                sim_responses.units = "N/mm²"
            else:
                sim_responses = sim_responses.map(lambda r: r * 1e3)
                sim_responses.units = "mm"
            # Get min and max values for both Axis and OpenSees.
            rt_str = "displa" if response_type == ResponseType.YTrans else "stress"
            row = axis_values[axis_values["name"] == f"{p}-{rt_str}"]
            dmin, dmax = float(row["dmin"]), float(row["dmax"])
            omin, omax = float(row["omin"]), float(row["omax"])
            amin, amax = max(dmin, omin), min(dmax, omax)
            levels = np.linspace(amin, amax, 16)
            # Plot and save the image. If plotting stresses use Axis values for
            # colour normalization.
            top_view_bridge(
                c.bridge, abutments=True, piers=True, units="m", compass=True
            )
            contour_responses(
                config=c,
                cmap=axis_cmap_r,
                responses=sim_responses,
                levels=levels,
                interp=(200, 60),
            )
            plt.legend()
            plt.tight_layout()
            plt.title(
                f"{sim_responses.response_type.name()} from 1mm pier settlement with OpenSees"
            )
            filename = safe_str(f"pier-{p}-{sim_responses.response_type.name()}")
            plt.savefig(
                c.get_image_path("verification/pier-settlement", filename + ".pdf")
            )
            plt.close()
            # First plot and clear, just to have the same colorbar.
            contour_responses(
                config=c, responses=sim_responses, cmap=axis_cmap_r, levels=levels
            )
            plt.cla()
            # Save the axis plots.
            axis_img = mpimg.imread(
                os.path.join(project_dir(), f"data/validation/axis/{p}-{rt_str}.PNG")
            )
            top_view_bridge(c.bridge, abutments=True, units="m", compass=True)
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
            plt.legend()
            # Title and save.
            plt.title(
                f"{sim_responses.response_type.name()} from 1mm pier settlement with AxisVM"
            )
            plt.tight_layout()
            plt.savefig(
                c.get_image_path(
                    "verification/pier-settlement", filename + "-axis" + ".pdf"
                )
            )
            plt.close()


def temperature_load(c: Config):
    """Response to unit temperature deck loading."""
    axis_values = pd.read_csv(
        os.path.join(project_dir(), "data/validation/axis/thermal-min-max.csv")
    )
    for temp_deltas, temp_id, temp_name in [
        ((1, None), "axial", "uniform"),
        ((None, 1), "moment", "linear"),
    ]:
        for i, response_type in enumerate(
            [ResponseType.StressXXB, ResponseType.YTrans, ResponseType.StressZZB]
        ):
            # Get min and max values for both Axis and OpenSees.
            rt_name = "ytrans"
            if response_type == ResponseType.StressXXB:
                rt_name = "stress"
            if response_type == ResponseType.StressZZB:
                rt_name = "stress_zzb"
            # The rt_name is used to extract min and max values for 'levels'..
            try:
                row = axis_values[axis_values["name"] == f"{rt_name}-{temp_id}"]
                dmin, dmax = float(row["dmin"]), float(row["dmax"])
                omin, omax = float(row["omin"]), float(row["omax"])
                amin, amax = (
                    np.around(max(dmin, omin), 2),
                    np.around(min(dmax, omax), 2),
                )
                print(f"{response_type.name()}: amin, amax = {amin}, {amax}")
                levels = np.linspace(amin, amax, 16)
            # .. but if these values are not available we don't use levels.
            except:
                print_w(f"Levels is None for response type {response_type.name()}")
                levels = None
            if levels is not None:
                print_i(
                    f"Min/max for {response_type.name()} = ({levels[0]}, {levels[-1]})"
                )
            # Load fem, strain in case of stress.
            sim_type = ResponseType.YTrans
            if response_type == ResponseType.StressXXB:
                sim_type = ResponseType.StrainXXB
            elif response_type == ResponseType.StressZZB:
                sim_type = ResponseType.StrainZZB
            sim_responses = sim.responses.load(
                config=c, response_type=sim_type, temp_deltas=temp_deltas
            )
            if response_type.is_stress():
                sim_responses = sim_responses.add_temp_strain(c, temp_deltas).to_stress(
                    c.bridge
                )
                sim_responses.units = "N/mm²"
            else:
                sim_responses = sim_responses.map(lambda r: r * 1e3)
                sim_responses.units = "mm"
            bridge_sim.plot.top_view_bridge(
                bridge=c.bridge, abutments=True, piers=True, units="m", compass=True,
            )
            plot.contour_responses(
                config=c,
                responses=sim_responses,
                cmap=axis_cmap_r,
                levels=levels,
                interp=(200, 60),
            )
            plt.legend()
            plt.title(
                f"{sim_responses.response_type.name()} from 1 ‎°C {temp_name} temp. deck loading with OpenSees"
            )
            plt.tight_layout()
            plt.savefig(
                c.get_image_path(
                    "verification/temperature",
                    safe_str(f"thermal-deck-unit-{temp_name}-{rt_name})") + ".pdf",
                )
            )
            plt.close()
            ##################
            # Now for AxisVM #
            ##################
            if response_type == ResponseType.StressZZB:
                continue  # We didn't save Axis StressZZB.
            # First plot and clear, just to have the same colorbar.
            plot.contour_responses(
                config=c, responses=sim_responses, cmap=axis_cmap_r, levels=levels
            )
            plt.cla()
            # Then imshow the axis image.
            bridge_sim.plot.top_view_bridge(
                bridge=c.bridge, abutments=True, units="m", compass=True
            )
            plt.imshow(
                mpl.image.imread(
                    os.path.join(
                        project_dir(),
                        f"data/validation/axis/thermal-{rt_name}-{temp_id}.PNG",
                    )
                ),
                extent=(
                    c.bridge.x_min,
                    c.bridge.x_max,
                    c.bridge.z_min,
                    c.bridge.z_max,
                ),
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
                f"{sim_type.name()} from 1‎°C {temp_name} temp. deck"
                f" loading with AxisVM"
            )
            plt.xlabel("X position (m)")
            plt.ylabel("Z position (m)")
            plt.tight_layout()
            plt.savefig(
                c.get_image_path(
                    "verification/temperature", f"axis-{rt_name}-{temp_name}.pdf",
                )
            )
            plt.close()


def self_weight(c: Config):
    """Contour plots of self-weight, OpenSees and AxisVM."""
    min_max_values = pd.read_csv(
        os.path.join(project_dir(), "data/validation/axis/self-weight.csv")
    )
    sim_types = [ResponseType.YTrans, ResponseType.StrainXXB]
    for sim_type in sim_types:
        response_type = sim_type
        if sim_type.is_strain():
            response_type = sim_type.to_stress()
            rt_str = "stressxxb"
            unit_str = "N/mm²"
        else:
            rt_str = "ytrans"
            unit_str = "mm"
        # Read the min max values.
        row = min_max_values[min_max_values["name"] == rt_str]
        amin, amax = float(row["amin"]), float(row["amax"])
        omin, omax = float(row["omin"]), float(row["omax"])
        rmin, rmax = max(amin, omin), min(amax, omax)
        print(f"{response_type.name()}: rmin, rmax = {rmin}, {rmax}")
        levels = np.linspace(rmin, rmax, 16)
        title = lambda prog: f"{response_type.name()} to self-weight with {prog}"
        save = lambda prog: c.get_image_path("verification/self-weight", prog + ".pdf")
        # Create the OpenSees plot.
        os_responses = sim.responses.load(
            config=c, response_type=sim_type, self_weight=True
        )
        if response_type.is_stress():
            os_responses = os_responses.to_stress(c.bridge)
        else:
            os_responses = os_responses.map(lambda r: r * 1e3)
        os_responses.units = unit_str
        top_view_bridge(c.bridge, piers=True, abutments=True, units="m", compass=True)
        contour_responses(
            config=c,
            responses=os_responses,
            cmap=axis_cmap_r,
            levels=levels,
            interp=(200, 60),
        )
        plt.legend()
        plt.title(title("OpenSees"))
        plt.tight_layout()
        plt.savefig(save(rt_str + "-OpenSees"))
        plt.close()

        # First plot and clear, just to have the same colorbar.
        contour_responses(
            config=c, responses=os_responses, cmap=axis_cmap_r, levels=levels
        )
        plt.cla()
        # Then plot the bridge and Axis image.
        top_view_bridge(c.bridge, piers=True, abutments=True, units="m", compass=True)
        plt.imshow(
            mpimg.imread(
                os.path.join(
                    project_dir(), f"data/validation/axis/self-weight-{rt_str}.PNG"
                )
            ),
            extent=(c.bridge.x_min, c.bridge.x_max, c.bridge.z_min, c.bridge.z_max,),
        )
        amin_s = f"{amin:.3f}"
        amax_s = f"{amax:.3f}"
        aabs_s = f"{abs(amin - amax):.3f}"
        for point, leg_label, color, alpha in [
            ((0, 0), f"min = {amin_s} {os_responses.units}", "r", 0),
            ((0, 0), f"max = {amax_s} {os_responses.units}", "r", 0),
            ((0, 0), f"|min-max| = {aabs_s} {os_responses.units}", "r", 0),
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
        plt.title(title("AxisVM"))
        plt.tight_layout()
        plt.savefig(save(rt_str + "-AxisVM"))
        plt.close()
