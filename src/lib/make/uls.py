import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import plot, sim
from bridge_sim.model import Config, Point, ResponseType
from bridge_sim.plot import equal_lims
from bridge_sim.util import print_i, safe_str


def plot_uls(config: Config, indices=[0, 1, 100, 2000, 2380, 2399]):
    xs = config.bridge.wheel_track_xs(config)
    zs = config.bridge.wheel_track_zs(config)
    for index in indices:
        x = xs[index % len(xs)]
        z = zs[index // len(xs)]
        print_i(f"Point at X = {x}, Z = {z}")
        responses = list(sim.run.point_load(config, indices=[index], response_type=ResponseType.YTrans))[0]
        plot.top_view_bridge(config.bridge, edges=True, piers=True, units="m")
        responses.units = "mm"
        plot.contour_responses(config, responses)
        plt.scatter([x], [z], c="r", s=10)
        plt.tight_layout()
        plt.title(f"Index = {index}, X = {x}, Z = {z}")
        plt.savefig(config.get_image_path("verification/uls", f"uls-{index}.pdf"))
        plt.close()


def plot_ulm(config: Config, response_type: ResponseType, indices=[100, 2000]):
    xs = config.bridge.wheel_track_xs(config)
    zs = config.bridge.wheel_track_zs(config)
    points = [
        Point(x=xs[index % len(xs)], z=zs[index // len(xs)])
        for index in indices
    ] + [Point(x=49.125, z=-8.4), Point(x=53.625, z=-8.4), Point(x=64.425, z=-8.4)]
    ulms = sim.run.load_ulm(config, response_type=response_type, points=points).T
    print_i(f"ULMs have shape {ulms.shape}")
    for i, point in enumerate(points):
        ulm = ulms[i].reshape(len(zs), len(xs))
        x, z = point.x, point.z
        plt.portrait()
        title = f"{response_type.name()} at X = {np.around(x, 2)} m, Z = {np.around(z, 2)} m"
        plt.suptitle(title)
        xaxis = np.interp(list(range(len(xs))), [0, len(xs) - 1], [config.bridge.x_min, config.bridge.x_max])
        for il in range(len(zs)):
            plt.subplot(len(zs), 1, il + 1)
            y = ulm[- (il + 1)]
            plt.plot(xaxis, y, c="r", lw=2)
            for s, support in enumerate(config.bridge.supports):
                plt.axvline(x=support.x - support.width_top / 2, c="black", label="piers" if s == 0 else None)
                plt.axvline(x=support.x + support.width_top / 2, c="black")
            plt.axvline(x=x, c="b", label="X position of response")
            plt.legend()
        equal_lims("y", len(zs), 1)
        plt.savefig(config.get_image_path("verification/uls", safe_str(f"ulm{point}-{response_type.value}") + ".pdf"))
        plt.close()
        plt.imshow(ulm.T, interpolation="nearest", aspect="auto")
        plt.title(title)
        plt.savefig(config.get_image_path("verification/uls", safe_str(f"ulm{point}-{response_type.value}-imshow") + ".pdf"))
        plt.close()
