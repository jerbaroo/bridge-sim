"""Plot vehicles distributions."""
import bridge_sim.util
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from bridge_sim.model import Config
from bridge_sim.vehicles.sample import (
    sample_vehicle,
    axle_array_and_count,
    load_vehicle_data,
)
from bridge_sim.util import print_i

# Print debug information for this file.
D: bool = False


def plot_dist(c: Config):
    """Original A16 data, showing outliers, and downsampled final data."""
    # Print information on original data.
    a16 = load_vehicle_data("data/a16-data/original-a16.csv")
    print_i(f"A16 columns = {a16.columns}")
    print_i(f"Original A16 data has {len(a16)} rows")
    min_length = np.min(a16["length"])
    print_i(f"Minimum length = {min_length / 100} m")
    min_weight = np.min(a16["total_weight"])
    print_i(f"Minimum weight = {min_weight} kN")

    # Get and remove outliers.
    outliers = a16[(np.abs(stats.zscore(a16[["total_weight", "length"]])) >= 2)]
    num_outliers = len(a16) - len(outliers)
    print_i(
        f"Removed {len(outliers)} ({len(outliers) / len(a16):.4f}) outliers (by weight & length) from A16 data"
    )
    a16 = a16.drop(outliers.index)

    # Sample to 10% of original size.
    a16 = a16.sample(n=int(len(a16) * 0.1))
    print_i(f"Downsampled A16 data has {len(a16)} rows")

    # Construct passenger vehicles.
    n, min_kn = len(a16), 5
    weights = np.random.gumbel(loc=12.53, scale=10, size=n)
    weights = [w for w in weights if w >= min_kn]
    axles = list(
        map(int, np.around(np.interp(weights, [min(weights), max(weights)], [2, 4]), 0))
    )
    add_min_length = 2.4 * 100
    add_max_length = min_length * 1.2
    lengths = np.interp(
        weights, [min(weights), max(weights)], [add_min_length, add_max_length]
    )
    rand = np.random.gumbel(loc=1.5, scale=4, size=len(lengths))
    lengths = np.multiply(lengths, rand)

    weights = np.multiply(weights, np.random.gumbel(1, 1, len(weights)))
    add_weight = np.interp(
        lengths, [add_min_length, add_max_length], [1, min_weight * 1.5]
    )
    weights += add_weight

    # Add passenger vehicles to DataFrame.
    records = []
    for length, weight, axle in zip(lengths, weights, axles):
        # A little filter function, to make results look a bit better.
        if (
            add_min_length <= length <= 9.7 * 100
            and weight >= 7
            and (length > 5 * 100 or weight < 100)
        ):
            records.append(
                {
                    "length": length,
                    "total_weight": weight,
                    "weight_per_axle": str([weight / axle] * axle),
                    "axle_distance": str([length / (axle - 1)] * (axle - 1)),
                }
            )
    a16 = a16.append(records, ignore_index=True)
    a16.index.name = "number"

    a16.to_csv("data/a16-data/a16.csv")
    print_i("Wrote updated A16 data to disk")

    ws, ls = a16["total_weight"], a16["length"]
    print_i(f"Weight: min = {min(ws)}, max = {max(ws)}")
    print_i(f"Length: min = {min(ls)}, max = {max(ls)}")

    # Plot.
    def plot_pdf():
        xs = list(map(lambda x: x[0], c.vehicle_pdf))
        xs[-1] = min(xs[-1], plt.xlim()[1])
        ps = list(map(lambda x: x[1], c.vehicle_pdf))
        total_x = xs[-1] - xs[0]
        rel_heights = []
        for x0, x1, p in zip(xs[:-1], xs[1:], ps):
            l = (x1 - x0) / total_x
            h = p / l
            rel_heights.append(h)
        for x0, x1, h in zip(xs[:-1], xs[1:], rel_heights):
            h = (h / max(rel_heights)) * plt.ylim()[1]
            plt.gca().add_patch(
                patches.Rectangle(
                    (x0, 0),
                    x1 - x0,
                    h,
                    facecolor="none",
                    edgecolor="red",
                    lw=1,
                    label=f"Area ∝ probability" if x1 == xs[-1] else None,
                )
            )
        plt.legend()

    n = 10000
    c.vehicle_data = load_vehicle_data(c.vehicle_data_path)
    vehicles = [sample_vehicle(c) for _ in range(n)]
    kns = list(map(lambda v: v.total_kn(), vehicles))

    num_axles = bridge_sim.util.apply(lambda s: len(axle_array_and_count(s)))
    plt.landscape()
    plt.subplot(3, 1, 1)
    plt.scatter(a16["length"] / 100, a16["total_weight"], s=1)
    plot_pdf()
    plt.ylabel("Load intensity (kN)")
    plt.xlabel("Length (m)")
    plt.title("Load intensity per vehicles")
    plt.xlim(0, plt.xlim()[1])
    plt.subplot(3, 1, 2)
    plt.scatter(a16["length"] / 100, num_axles, s=1)
    plt.xlim(0, plt.xlim()[1])
    plt.ylabel("Number of axles")
    plt.xlabel("Length (m)")
    plt.title("Number of axles per vehicles")
    plt.subplot(3, 1, 3)
    plt.hist(kns)
    plt.ylabel("Number of vehicles")
    plt.xlabel("Load intensity")
    plt.title(f"Load intensity distribution of {n} sampled vehicles")
    plt.tight_layout()
    plt.savefig(c.get_image_path("vehicles", "vehicles-db.png"))
    plt.savefig(c.get_image_path("vehicles", "vehicles-db.pdf"))
    plt.close()
