import matplotlib.pyplot as plt

from bridge_sim import plot, sim
from bridge_sim.model import Config, ResponseType
from bridge_sim.util import print_i


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
        plt.savefig(config.get_image_path("verification/uls", f"uls{index}.pdf"))
        plt.close()

