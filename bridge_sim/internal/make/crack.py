from typing import Tuple, List

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import crack, temperature, plot, sim, traffic
from bridge_sim.model import Config, ResponseType, Point
from bridge_sim.sim.model import Responses, Shell
from bridge_sim.sim.responses import without
from bridge_sim.util import safe_str, print_i
from bridge_sim.vehicles import truck1


def plot_crack_E(config: Config):
    """Verification plot of Young's modulus before and after cracking"""
    plt.portrait()
    plt.subplot(3, 1, 2)
    transverse_crack = crack.transverse_crack(length=2, at_x=config.bridge.x_center)
    crack_config = transverse_crack.crack(config)
    cmap, norm = plot.shells(
        crack_config, color_f=lambda shell: shell.section.youngs_x(), ret_cmap_norm=True
    )
    plot.top_view_bridge(config.bridge, piers=True)
    plt.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=plt.gca(), cmap=cmap, norm=norm
    )
    plt.title("Cracked bridge")
    plt.subplot(3, 1, 1)
    plot.shells(
        config, color_f=lambda shell: shell.section.youngs_x(), cmap=cmap, norm=norm
    )
    plot.top_view_bridge(config.bridge, piers=True)
    plt.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=plt.gca(), cmap=cmap, norm=norm
    )
    plt.title("Uncracked bridge")
    plt.subplot(3, 1, 3)

    def difference(shell: Shell) -> float:
        center = shell.center()
        uncracked_shell = config.bridge.deck_section_at(x=center.x, z=center.z)
        return uncracked_shell.youngs_x() - shell.section.youngs_x()

    cmap, norm = plot.shells(crack_config, color_f=difference, ret_cmap_norm=True)
    plot.top_view_bridge(config.bridge, piers=True)
    plt.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=plt.gca(), cmap=cmap, norm=norm
    )
    plt.title("Difference of cracked and uncracked")
    plt.tight_layout()
    plt.savefig(config.get_image_path("verification/cracking", "crack.pdf"))
    plt.close()


def crack_zone_plot(
    config: Config,
    crack_x_min: float,
    crack_length: float,
    response_type: ResponseType,
    run: bool = False,
    scatter: bool = False,
    temps: Tuple[float, float] = [17, 23],
):
    """Plot bridge responses to temperature with and without cracking.

    Args:
        config: simulation configuration object.
        crack_x_min: lower X position of crack zone.
        crack_length: length of crack zone in X direction.
        response_type: type of sensor response to plot.
        run: force the simulation data to be regenerated.
        scatter: scatter plot instead of contour plot.
        temps: temperature profile of the deck.

    """
    NUM_X, NUM_Z = 2000, 120
    # NUM_X, NUM_Z = 100, 100
    points = [
        Point(x=x, z=z)
        for x in np.linspace(config.bridge.x_min, config.bridge.x_max, NUM_X)
        for z in np.linspace(config.bridge.z_min, config.bridge.z_max, NUM_Z)
    ]
    crack_deck = crack.transverse_crack(length=crack_length, at_x=crack_x_min)
    crack_config = crack_deck.crack(config)
    time = truck1.time_at(x=56, bridge=config.bridge)
    thresh = 0.35
    _w1 = crack_deck.without(config.bridge, thresh)
    _w2 = without.edges(config, 2)
    without_crack_zone_and_thresh = lambda p, _r: not _w1(p) or _w2(p, None)
    print_i(f"{thresh} m outside crack zone not considered")

    def filter_responses(_responses):
        return (
            _responses.without_nan_inf()
            .map(lambda r: r * (1e6 if response_type.is_strain() else 1))
            .without(without_crack_zone_and_thresh)
        )

    # Find closes point to middle of lane.
    pi = 0
    point = points[pi]
    dist_to = Point(x=55, z=-8.4)
    for i in range(len(points)):
        if points[i].distance(dist_to) < point.distance(dist_to):
            pi = i
            point = points[pi]

    def get_responses(_config):
        _temp_responses = temperature.effect(
            config=_config,
            response_type=response_type,
            points=points,
            temps_bt=([temps[0]], [temps[1]]),
        ).T[0]
        _truck_responses = sim.responses.load(
            config=_config,
            response_type=response_type,
            point_loads=truck1.wheel_track_loads(_config, times=[time])[0],
        ).at_decks(points) * (1e-6 if response_type.is_strain() else 1)
        print_i(f"Temperature shape = {_temp_responses.shape}")
        print_i(f"Truck shape = {_truck_responses.shape}")
        _responses = _temp_responses + _truck_responses
        print_i(
            f"At index {pi}: (temp, truck, +) = {_temp_responses[pi]}, {_truck_responses[pi]}, {_responses[pi]}"
        )
        assert _responses.shape == _truck_responses.shape
        assert np.isclose(_responses[pi], _temp_responses[pi] + _truck_responses[pi])
        if not response_type.is_strain():
            _responses *= 1e3
        return (
            _responses,
            (
                filter_responses(
                    Responses(
                        response_type=response_type,
                        responses=list(zip(_responses, points)),
                        units="" if response_type.is_strain() else "mm",
                    )
                )
            ),
        )

    def plot_outline(label):
        cz = crack_deck.crack_zone(config.bridge)
        c_x_start, c_z_start, c_x_end, c_z_end = [
            cz.x_min,
            cz.z_min,
            cz.x_max,
            cz.z_max,
        ]
        plt.gca().add_patch(
            mpl.patches.Rectangle(
                (c_x_start, c_z_start),
                c_x_end - c_x_start,
                c_z_end - c_z_start,
                fill=not scatter,
                edgecolor="black",
                facecolor="white",
                alpha=1,
                label=label,
            )
        )

    def legend():
        plt.legend(
            loc="upper right",
            borderpad=0.2,
            labelspacing=0.2,
            borderaxespad=0,
            handletextpad=0.2,
            columnspacing=0.2,
        )

    center = config.bridge.x_center
    min_x, max_x = center - 20, center + 20
    min_z, max_z = config.bridge.z_min, config.bridge.z_max

    def zoom_in():
        plt.ylim(min_z, max_z)
        plt.xlim(min_x, max_x)

    # Collect responses.
    _r, responses = get_responses(config)
    _cr, crack_responses = get_responses(crack_config)
    diff_responses = filter_responses(
        Responses(
            response_type=response_type,
            responses=list(zip(map(lambda x: x[1] - x[0], zip(_r, _cr)), points)),
            units="" if response_type.is_strain() else "mm",
        )
    )

    count_min, count_max = 0, 0
    diff_min, diff_max = min(diff_responses.values()), max(diff_responses.values())
    print(f"Diff min, max = {diff_min}, {diff_max}")
    diff_min08, diff_max08 = diff_min * 0.8, diff_max * 0.8
    for diff_r in diff_responses.values():
        if diff_r < diff_min08:
            count_min += 1
        if diff_r > diff_max08:
            count_max += 1
    print(f"Count = {count_min}, {count_max}")
    txt_path = config.get_image_path(
        "classify/crack_zones",
        safe_str(f"x-{crack_x_min}-len-{crack_length}-{response_type.value}") + ".txt",
    )
    point_area = (config.bridge.length / NUM_X) * (config.bridge.width / NUM_Z)
    with open(txt_path, "w") as f:
        f.write(
            f"Count 0.8 min/max = {count_min}, {count_max}, area = {point_area}, min/max area = {count_min * point_area}, {count_max * point_area}"
        )

    # Norm calculation.
    r_min, r_max = min(responses.values()), max(responses.values())
    c_min, c_max = min(crack_responses.values()), max(crack_responses.values())
    vmin, vmax = min(r_min, c_min), max(r_max, c_max)
    # vmin, vmax = min(vmin, -vmax), max(vmax, -vmin)
    print_i(f"Min, max = {vmin}, {vmax}")
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

    # Healthy bridge.
    plt.portrait()
    plt.subplot(3, 1, 1)
    plot.contour_responses(config, responses, decimals=1, interp=(200, 60), norm=norm)
    plot.top_view_bridge(config.bridge, piers=True, units="m")
    plot_outline("Not considered")
    plot.top_view_vehicles(
        config, [truck1], time, wheels=True, body=False, label_wheels=True
    )
    legend()
    plt.xlabel(None)
    plt.tick_params(axis="x", bottom=False, labelbottom=False)
    plt.title("Healthy bridge")
    zoom_in()

    # Cracked bridge.
    plt.subplot(3, 1, 2)
    plot.contour_responses(
        config, crack_responses, decimals=1, interp=(200, 60), norm=norm
    )
    plot.top_view_bridge(config.bridge, piers=True, units="m")
    plot_outline("Crack zone")
    plot.top_view_vehicles(
        config, [truck1], time, wheels=True, body=False, label_wheels=True
    )
    legend()
    plt.xlabel(None)
    plt.tick_params(axis="x", bottom=False, labelbottom=False)
    plt.title("Cracked bridge")
    zoom_in()

    # Difference of cracked and uncracked.
    plt.subplot(3, 1, 3)
    vmin, vmax = min(diff_responses.values()), max(diff_responses.values())
    vmin, vmax = min(vmin, -vmax), max(vmax, -vmin)
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    plot.contour_responses(
        config,
        diff_responses,
        decimals=1,
        interp=(200, 60),
        cmap=mpl.cm.get_cmap("RdBu_r"),
        norm=norm,
    )
    plot.top_view_bridge(config.bridge, piers=True, units="m")
    plot_outline("Crack zone")
    plot.top_view_vehicles(
        config, [truck1], time, wheels=True, body=False, label_wheels=True
    )
    legend()
    plt.title("Difference of healthy & cracked bridge")
    zoom_in()

    rt_str = (
        "Microstrain XXB"
        if response_type == ResponseType.StrainXXB
        else response_type.name()
    )
    plt.suptitle(
        f"{rt_str}: Truck 1 on healthy & cracked bridge\nT_REF = {config.bridge.ref_temp_c} °C, T_bot = {temps[0]} °C, T_top = {temps[1]} °C"
    )
    plt.tight_layout(rect=[0, 0.03, 1, 0.93])
    plt.savefig(
        config.get_image_path(
            "classify/crack_zones",
            safe_str(f"x-{crack_x_min}-len-{crack_length}-{response_type.value}")
            + ".png",
        )
    )
    plt.close()


def crack_zone_plots(
    config: Config,
    response_types: List[ResponseType],
    temps: Tuple[float, float] = [17, 25],
):
    for x, length in [(50, 0.5), (50, 1), (50, 3), (50, 5), (41.25, 20), (48, 14)]:
        for response_type in response_types:
            crack_zone_plot(
                config=config,
                crack_x_min=x,
                crack_length=length,
                response_type=response_type,
                temps=temps,
            )


def plot_crack_time_series(config: Config):
    time = 10
    _0, _1, ta = traffic.load_traffic(config, traffic.normal_traffic(config), time=time)
    response_type = ResponseType.YTrans
    crack_f = crack.transverse_crack(at_x=80, length=2)
    point = Point(x=80, z=-8.4)
    crack_time = 5
    crack_index = int((crack_time / time) * len(ta))
    responses = sim.responses.to(
        config=config,
        points=[point],
        traffic_array=ta,
        response_type=response_type,
        crack=(crack_f, crack_index),
    )[0]
    plt.landscape()
    plt.plot(np.linspace(0, time, len(responses)), responses)
    plt.axvline(x=crack_time, c="black", label="Crack occurs")
    plt.ylabel(response_type.name())
    plt.xlabel("Time (s)")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(config.get_image_path("crack", "time-series.png"))
