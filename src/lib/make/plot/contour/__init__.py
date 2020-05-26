"""Make contour plots."""
import itertools
from itertools import chain

import matplotlib.colors as colors
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from matplotlib.cm import get_cmap

from bridge_sim.model import Config, PierSettlement, Point, PointLoad, ResponseType
from bridge_sim.sim.responses import responses_to_traffic_array
from bridge_sim.scenarios import (
    HealthyScenario,
    transverse_crack,
    PierSettlementScenario,
)
from bridge_sim.vehicles import truck1
from bridge_sim.sim.model import SimParams
from bridge_sim.sim.responses import Responses, load_fem_responses
from bridge_sim.sim.run.opensees import OSRunner
from lib.make.plot.distribution import load_normal_traffic_array
from lib.plot import diana_cmap_r, parula_cmap, plt
from lib.plot.contour import contour_responses_3d
from lib.plot.geometry import top_view_bridge
from lib.plot.responses import plot_contour_deck
from bridge_sim.util import safe_str

# Print debug information for this file.
D: str = "make.plots.contour"
# D: bool = False


def cover_photo(c: Config, x: float, deformation_amp: float):
    """

    TODO: SimParams takes any loads iterable, to be flattened.
    TODO: Wrap SimRunner into Config.
    TODO: Ignore response type in SimParams (fill in by load_sim_responses).

    """
    response_type = ResponseType.YTranslation
    sim_responses = load_fem_responses(
        c=c,
        sim_runner=OSRunner(c),
        response_type=response_type,
        sim_params=SimParams(
            response_types=[response_type],
            ploads=list(
                chain.from_iterable(
                    truck1.to_point_loads(
                        bridge=c.bridge, time=truck1.time_at(x=x, bridge=c.bridge),
                    )
                )
            ),
        ),
    )
    shells = contour_responses_3d(c=c, sim_responses=sim_responses)
    for cmap in [
        parula_cmap,
        get_cmap("jet"),
        get_cmap("coolwarm"),
        get_cmap("viridis"),
    ]:
        contour_responses_3d(
            c=c,
            sim_responses=sim_responses,
            deformation_amp=deformation_amp,
            shells=shells,
            cmap=cmap,
        )
        plt.axis("off")
        plt.grid(False)
        plt.savefig(
            c.get_image_path(
                "cover-photo",
                f"cover-photo-deform-{deformation_amp}" f"-cmap-{cmap.name}.pdf",
            )
        )
        plt.close()


def traffic_response_plots(c: Config, times: int = 3):
    """Response to normal traffic per scenarios scenario at multiple time steps."""
    response_type = ResponseType.YTranslation
    # 10 x 10 grid of points on the bridge deck where to record fem.
    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, 10),
            np.linspace(c.bridge.z_min, c.bridge.z_max, 10),
        )
    ]
    # for damage_scenario in all_scenarios(c):
    for damage_scenario in [unit_temp_scenario]:
        response_array = responses_to_traffic_array(
            c=c,
            traffic_array=load_normal_traffic_array(c, mins=1)[0],
            response_type=response_type,
            bridge_scenario=damage_scenario,
            points=points,
            sim_runner=OSRunner,
        )
        print(response_array.shape)
        mean_response_array = np.mean(response_array, axis=0).T
        print(mean_response_array.shape)
        print(mean_response_array.shape)

        for t in range(times):
            time_index = -1 + abs(t)
            top_view_bridge(c.bridge, abutments=True, piers=True)
            responses = Responses.from_responses(
                response_type=response_type,
                responses=[
                    (response_array[time_index][p], point)
                    for p, point in enumerate(points)
                ],
            )
            plot_contour_deck(c=c, responses=responses, center_norm=True, levels=100)
            plt.title(damage_scenario.name)
            plt.savefig(
                c.get_image_path(
                    "contour-traffic-response",
                    f"{damage_scenario.name}-time={time_index}",
                )
            )
            plt.close()


def point_load_response_plots(
    c: Config, x: float, z: float, kn: int = 1000, run: bool = False
):
    """Response to a point load per scenarios scenario."""
    response_types = [ResponseType.YTranslation, ResponseType.Strain]
    # scenarios = all_scenarios(c)
    damage_scenarios = [HealthyScenario(), transverse_crack()]

    # 10 x 10 grid of points on the bridge deck where to record fem.
    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, 30),
            np.linspace(c.bridge.z_min, c.bridge.z_max, 100),
        )
    ]

    for response_type in response_types:
        all_responses = []
        for damage_scenario in damage_scenarios:
            sim_params = SimParams(
                response_types=[response_type],
                ploads=[
                    PointLoad(
                        x_frac=c.bridge.x_frac(x), z_frac=c.bridge.z_frac(z), kn=kn
                    )
                ],
            )
            use_c, sim_params = damage_scenario.use(c=c, sim_params=sim_params)
            all_responses.append(
                load_fem_responses(
                    c=use_c,
                    sim_params=sim_params,
                    response_type=response_type,
                    sim_runner=OSRunner(use_c),
                    run=run,
                ).resize()
            )
        amin, amax = np.inf, -np.inf
        for sim_responses in all_responses:
            responses = np.array(list(sim_responses.values()))
            amin = min(amin, min(responses))
            amax = max(amax, max(responses))
        for d, damage_scenario in enumerate(damage_scenarios):
            top_view_bridge(c.bridge, abutments=True, piers=True)
            plot_contour_deck(
                c=c,
                responses=all_responses[d],
                levels=100,
                norm=colors.Normalize(vmin=amin, vmax=amax),
                decimals=10,
            )
            plt.title(damage_scenario.name)
            plt.tight_layout()
            plt.savefig(
                c.get_image_path(
                    "contour/point-load",
                    safe_str(
                        f"x-{x:.2f}-z-{z:.2f}-kn-{kn}-{response_type.name()}-{damage_scenario.name}"
                    )
                    + ".pdf",
                )
            )
            plt.close()


def cracked_concrete_plots(c: Config):
    """Contour plots of cracked concrete scenarios."""
    response_type = ResponseType.YTranslation
    # 10 x 10 grid of points on the bridge deck where to record fem.
    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, 10),
            np.linspace(c.bridge.z_min, c.bridge.z_max, 10),
        )
    ]

    # Create empty traffic array and collect fem.
    response_array = responses_to_traffic_array(
        c=c,
        traffic_array=load_normal_traffic_array(c)[0],
        response_type=response_type,
        bridge_scenario=cracked_scenario,
        points=points,
        sim_runner=OSRunner,
    )

    for t in range(len(response_array)):
        top_view_bridge(c.bridge, abutments=True, piers=True)
        responses = Responses.from_responses(
            response_type=response_type,
            responses=[(response_array[t][p], point) for p, point in enumerate(points)],
        )
        plot_contour_deck(c=c, responses=responses, center_norm=True)
        plt.title("Cracked Concrete")
        plt.savefig(c.get_image_path("cracked-scenario", f"cracked-time-{t}"))
        plt.close()


def piers_displaced(c: Config):
    """Contour plots of pier displacement for the given pier indices."""
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
            # norm = None
            from plot import axis_cmap_r

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


def gradient_pier_displacement_plots(c: Config):
    """Contour plot of piers displaced in an increasing gradient."""
    for response_type in [ResponseType.YTranslation]:

        # Equal pier displacement scenario.
        for displacement in np.array([0.1, 0.01]) / 1000:
            gradient_pier_displacement_plot(
                c=c,
                pier_disp=equal_pier_disp(bridge=c.bridge, displacement=displacement),
                response_type=response_type,
                title=f"{response_type.name()} when each pier is displaced by {displacement} m",
            )

        # Gradient pier displacement scenario.
        for start, step in itertools.product([0.01, 0.02, 0.05], [0.01, 0.02, 0.05]):
            start, step = np.array([start, step]) / 1000
            gradient_pier_displacement_plot(
                c=c,
                pier_disp=longitudinal_pier_disp(
                    bridge=c.bridge, start=start, step=step
                ),
                response_type=response_type,
                title=f"{response_type.name()} when piers are incrementally displaced by {step} m starting at {start} m",
            )


def gradient_pier_displacement_plot(
    c: Config,
    pier_disp: PierSettlementScenario,
    response_type: ResponseType,
    title: str,
):
    """Contour plot of piers displaced in an increasing gradient."""

    # 10 x 10 grid of points on the bridge deck where to record fem.
    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, 10),
            np.linspace(c.bridge.z_min, c.bridge.z_max, 10),
        )
    ]

    # Create empty traffic array and collect fem.
    response_array = responses_to_traffic_array(
        c=c,
        traffic_array=np.zeros((1, len(c.bridge.wheel_tracks(c)) * c.il_num_loads)),
        response_type=response_type,
        bridge_scenario=pier_disp,
        points=points,
        fem_runner=OSRunner(c),
    )

    top_view_bridge(c.bridge, abutments=True, piers=True)
    responses = Responses.from_responses(
        response_type=response_type,
        responses=[(response_array[0][p], point) for p, point in enumerate(points)],
    )
    plot_contour_deck(c=c, responses=responses, center_norm=True)
    plt.title(title)
    plt.savefig(
        c.get_image_path("pier-scenarios", f"pier-displacement-{safe_str(title)}")
    )
    plt.close()


def comparison_plots_705(c: Config, run_only: bool, scatter: bool):
    """Make contour plots for all verification points on bridge 705."""
    # from classify.scenario.bridge import transverse_crack
    # c = transverse_crack().use(c)[0]
    positions = [
        # (52, -8.4, "a"),
        (34.95459, 26.24579 - 16.6, "a"),
        (51.25051, 16.6 - 16.6, "b"),
        (89.98269, 9.445789 - 16.6, "c"),
        (102.5037, 6.954211 - 16.6, "d"),
        # (34.95459, 29.22606 - 16.6, "a"),
        # (51.25051, 16.6 - 16.6, "b"),
        # (92.40638, 12.405 - 16.6, "c"),
        # (101.7649, 3.973938 - 16.6, "d"),
    ]
    diana_values = pd.read_csv("validation/diana-screenshots/min-max.csv")
    response_types = [ResponseType.YTranslation, ResponseType.Strain]
    # For each response type and loading position first create contour plots for
    # OpenSees. Then finally create subplots comparing to Diana.
    cmap = diana_cmap_r
    for load_x, load_z, label in positions:
        for response_type in response_types:
            # Setup the metadata.
            if response_type == ResponseType.YTranslation:
                rt_str = "displa"
                unit_str = "mm"
            elif response_type == ResponseType.Strain:
                rt_str = "strain"
                unit_str = "E-6"
            else:
                raise ValueError("Unsupported response type")
            row = diana_values[diana_values["name"] == f"{label}-{rt_str}"]
            dmin, dmax = float(row["dmin"]), float(row["dmax"])
            omin, omax = float(row["omin"]), float(row["omax"])
            amin, amax = max(dmin, omin), min(dmax, omax)
            levels = np.linspace(amin, amax, 16)

            # Create the OpenSees plot.
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
            if run_only:
                continue
            title = (
                f"{response_type.name()} from a {loads[0].kn} kN point load at"
                + f"\nx = {load_x:.3f}m, z = {load_z:.3f}m, with "
            )
            save = lambda prefix: c.get_image_path(
                "validation/diana-comp",
                safe_str(f"{prefix}{response_type.name()}") + ".pdf",
            )
            top_view_bridge(c.bridge, piers=True, abutments=True)
            fem_responses = fem_responses.resize()
            sci_format = response_type == ResponseType.Strain
            plot_contour_deck(
                c=c,
                responses=fem_responses,
                ploads=loads,
                cmap=cmap,
                levels=levels,
                sci_format=sci_format,
                decimals=4,
                scatter=scatter,
            )
            plt.title(title + "OpenSees")
            plt.tight_layout()
            plt.savefig(save(f"{label}-"))
            plt.close()

            # Finally create label/title the Diana plot.
            if label is not None:
                # First plot and clear, just to have the same colorbar.
                plot_contour_deck(
                    c=c, responses=fem_responses, ploads=loads, cmap=cmap, levels=levels
                )
                plt.cla()
                # Then plot the bridge and
                top_view_bridge(c.bridge, piers=True, abutments=True)
                plt.imshow(
                    mpimg.imread(f"validation/diana-screenshots/{label}-{rt_str}.png"),
                    extent=(
                        c.bridge.x_min,
                        c.bridge.x_max,
                        c.bridge.z_min,
                        c.bridge.z_max,
                    ),
                )
                dmin_s = f"{dmin:.4e}" if sci_format else f"{dmin:.4f}"
                dmax_s = f"{dmax:.4e}" if sci_format else f"{dmax:.4f}"
                dabs_s = (
                    f"{abs(dmin - dmax):.4e}"
                    if sci_format
                    else f"{abs(dmin - dmax):.4f}"
                )
                for point, leg_label, color, alpha in [
                    ((load_x, load_z), f"{loads[0].kn} kN load", "r", 1),
                    ((0, 0), f"min = {dmin_s} {fem_responses.units}", "r", 0),
                    ((0, 0), f"max = {dmax_s} {fem_responses.units}", "r", 0),
                    ((0, 0), f"|min-max| = {dabs_s} {fem_responses.units}", "r", 0),
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
                plt.title(title + "Diana")
                plt.xlabel("X position (m)")
                plt.ylabel("Z position (m)")
                plt.tight_layout()
                plt.savefig(save(f"{label}-diana-"))
                plt.close()


def plot_of_unit_loads(c: Config):
    """Make a contour plot of response at unit load position."""
    fem_runner = OSRunner(c)
    response_type = ResponseType.YTranslation
    X, Z, R = [], [], []
    for x in np.linspace(c.bridge.x_min, c.bridge.x_max, int(c.bridge.length)):
        X.append([])
        Z.append([])
        R.append([])
        for z in np.linspace(c.bridge.z_min, c.bridge.z_max, int(c.bridge.width)):
            pload = PointLoad(
                x_frac=c.bridge.x_frac(x), z_frac=c.bridge.z_frac(z), kn=100
            )
            fem_params = SimParams(ploads=[pload], response_types=[response_type])
            fem_responses = load_fem_responses(
                c=c,
                fem_params=fem_params,
                response_type=response_type,
                fem_runner=fem_runner,
            )
            X[-1].append(x)
            Z[-1].append(z)
            R[-1].append(fem_responses._at(x=x, y=0, z=z))

    cmap = get_cmap("bwr")
    plt.contourf(X, Z, R, levels=50, cmap=cmap)
    plt.show()
