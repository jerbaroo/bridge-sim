import bridge_sim.plot
import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import plot, sim
from bridge_sim.model import Config, Point, ResponseType
from bridge_sim.plot.util import equal_lims
from bridge_sim.sim.run import ulm_point_loads
from bridge_sim.util import print_i, safe_str


def plot_uls(config: Config, indices=[0, 1, 10, 100, 1100, 1110, 1119]):
    point_loads = ulm_point_loads(config)
    for index in indices:
        responses = list(
            sim.run.point_load(
                config, indices=[index], response_type=ResponseType.YTrans
            )
        )[0].map(lambda r: r * 1e3)
        bridge_sim.plot.top_view_bridge(
            config.bridge, edges=True, piers=True, units="m"
        )
        responses.units = "mm"
        plot.contour_responses(config, responses)
        for point_load in point_loads[index]:
            plt.scatter([point_load.x], [point_load.z], c="r", s=10)
        plt.tight_layout()
        plt.title(f"Index = {index}")
        plt.savefig(config.get_image_path("verification/uls", f"uls-{index}.pdf"))
        plt.close()


def plot_ulm(config: Config, response_type: ResponseType, indices=[100, 1100]):
    xs = config.bridge.wheel_track_xs(config)
    zs = config.bridge.axle_track_zs()
    points = [
        Point(x=xs[index % len(xs)], z=zs[index // len(xs)]) for index in indices
    ] + [Point(x=49.125, z=-8.4), Point(x=53.625, z=-8.4), Point(x=64.425, z=-8.4)]
    ulms = sim.run.load_ulm(config, response_type=response_type, points=points).T
    print_i(f"ULMs have shape {ulms.shape}")
    for i, point in enumerate(points):
        ulm = ulms[i].reshape(len(zs), len(xs))
        x, z = point.x, point.z
        plt.portrait()
        title = f"{response_type.name()} at X = {np.around(x, 2)} m, Z = {np.around(z, 2)} m"
        plt.suptitle(title)
        xaxis = np.interp(
            list(range(len(xs))),
            [0, len(xs) - 1],
            [config.bridge.x_min, config.bridge.x_max],
        )
        for il in range(len(zs)):
            plt.subplot(len(zs), 1, il + 1)
            y = ulm[-(il + 1)]
            plt.plot(xaxis, y, c="r", lw=2)
            for s, support in enumerate(config.bridge.supports):
                plt.axvline(
                    x=support.x - support.width_top / 2,
                    c="black",
                    label="piers" if s == 0 else None,
                )
                plt.axvline(x=support.x + support.width_top / 2, c="black")
            plt.axvline(x=x, c="b", label="X position of response")
            plt.legend()
        equal_lims("y", len(zs), 1)
        plt.savefig(
            config.get_image_path(
                "verification/uls",
                safe_str(f"ulm{point}-{response_type.value}") + ".pdf",
            )
        )
        plt.close()
        plt.imshow(ulm.T, interpolation="nearest", aspect="auto")
        plt.title(title)
        plt.savefig(
            config.get_image_path(
                "verification/uls",
                safe_str(f"ulm{point}-{response_type.value}-imshow") + ".pdf",
            )
        )
        plt.close()
