"""General plotting functions.

More specific plotting functions are found in other modules.

"""

import matplotlib
import matplotlib.colors as colors
import matplotlib.pyplot as _plt
from matplotlib.ticker import ScalarFormatter
import numpy as np

from bridge_sim.util import print_i

# Print debug information for this file.
D: bool = False

# Apply modifications to matplotlib.pyplot. #


def _portrait():
    matplotlib.rcParams["figure.figsize"] = (10, 16)


def _square():
    matplotlib.rcParams["figure.figsize"] = (16, 16)


def _landspace():
    matplotlib.rcParams["figure.figsize"] = (16, 10)


_og_savefig = _plt.savefig
_og_show = _plt.show


def _savefig(s):
    print_i(f"Saving image to {s}")
    _og_savefig(s)
    if s.endswith(".pdf"):
        _og_savefig(s.replace(".pdf", ".png"))


def _show(*args, **kwargs):
    _og_show(*args, **kwargs)


def _equal_ax_lims(plt):
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    amin, amax = min(xmin, ymin), max(xmax, ymax)
    plt.xlim((amin, amax))
    plt.ylim((amin, amax))


plt = _plt
plt.equal_ax_lims = lambda: _equal_ax_lims(plt)
plt.savefig = _savefig
plt.show = _show
plt.portrait = _portrait
plt.square = _square
plt.landscape = _landspace

SMALL_SIZE = 18
MEDIUM_SIZE = 22
BIGGER_SIZE = 26

plt.rc("font", size=SMALL_SIZE)  # Default text sizes.
plt.rc("axes", titlesize=BIGGER_SIZE)  # Axes titles.
plt.rc("axes", labelsize=MEDIUM_SIZE)  # Axes titles.
plt.rc("xtick", labelsize=SMALL_SIZE)  # X tick labels.
plt.rc("ytick", labelsize=SMALL_SIZE)  # Y tick labels.
plt.rc("legend", fontsize=SMALL_SIZE)  # Legend.
plt.rc("figure", titlesize=BIGGER_SIZE)  # Figure title


###############################################################################


parula_cmap = colors.LinearSegmentedColormap.from_list(
    "parula",
    [
        [0.2081, 0.1663, 0.5292],
        [0.2116238095, 0.1897809524, 0.5776761905],
        [0.212252381, 0.2137714286, 0.6269714286],
        [0.2081, 0.2386, 0.6770857143],
        [0.1959047619, 0.2644571429, 0.7279],
        [0.1707285714, 0.2919380952, 0.779247619],
        [0.1252714286, 0.3242428571, 0.8302714286],
        [0.0591333333, 0.3598333333, 0.8683333333],
        [0.0116952381, 0.3875095238, 0.8819571429],
        [0.0059571429, 0.4086142857, 0.8828428571],
        [0.0165142857, 0.4266, 0.8786333333],
        [0.032852381, 0.4430428571, 0.8719571429],
        [0.0498142857, 0.4585714286, 0.8640571429],
        [0.0629333333, 0.4736904762, 0.8554380952],
        [0.0722666667, 0.4886666667, 0.8467],
        [0.0779428571, 0.5039857143, 0.8383714286],
        [0.079347619, 0.5200238095, 0.8311809524],
        [0.0749428571, 0.5375428571, 0.8262714286],
        [0.0640571429, 0.5569857143, 0.8239571429],
        [0.0487714286, 0.5772238095, 0.8228285714],
        [0.0343428571, 0.5965809524, 0.819852381],
        [0.0265, 0.6137, 0.8135],
        [0.0238904762, 0.6286619048, 0.8037619048],
        [0.0230904762, 0.6417857143, 0.7912666667],
        [0.0227714286, 0.6534857143, 0.7767571429],
        [0.0266619048, 0.6641952381, 0.7607190476],
        [0.0383714286, 0.6742714286, 0.743552381],
        [0.0589714286, 0.6837571429, 0.7253857143],
        [0.0843, 0.6928333333, 0.7061666667],
        [0.1132952381, 0.7015, 0.6858571429],
        [0.1452714286, 0.7097571429, 0.6646285714],
        [0.1801333333, 0.7176571429, 0.6424333333],
        [0.2178285714, 0.7250428571, 0.6192619048],
        [0.2586428571, 0.7317142857, 0.5954285714],
        [0.3021714286, 0.7376047619, 0.5711857143],
        [0.3481666667, 0.7424333333, 0.5472666667],
        [0.3952571429, 0.7459, 0.5244428571],
        [0.4420095238, 0.7480809524, 0.5033142857],
        [0.4871238095, 0.7490619048, 0.4839761905],
        [0.5300285714, 0.7491142857, 0.4661142857],
        [0.5708571429, 0.7485190476, 0.4493904762],
        [0.609852381, 0.7473142857, 0.4336857143],
        [0.6473, 0.7456, 0.4188],
        [0.6834190476, 0.7434761905, 0.4044333333],
        [0.7184095238, 0.7411333333, 0.3904761905],
        [0.7524857143, 0.7384, 0.3768142857],
        [0.7858428571, 0.7355666667, 0.3632714286],
        [0.8185047619, 0.7327333333, 0.3497904762],
        [0.8506571429, 0.7299, 0.3360285714],
        [0.8824333333, 0.7274333333, 0.3217],
        [0.9139333333, 0.7257857143, 0.3062761905],
        [0.9449571429, 0.7261142857, 0.2886428571],
        [0.9738952381, 0.7313952381, 0.266647619],
        [0.9937714286, 0.7454571429, 0.240347619],
        [0.9990428571, 0.7653142857, 0.2164142857],
        [0.9955333333, 0.7860571429, 0.196652381],
        [0.988, 0.8066, 0.1793666667],
        [0.9788571429, 0.8271428571, 0.1633142857],
        [0.9697, 0.8481380952, 0.147452381],
        [0.9625857143, 0.8705142857, 0.1309],
        [0.9588714286, 0.8949, 0.1132428571],
        [0.9598238095, 0.9218333333, 0.0948380952],
        [0.9661, 0.9514428571, 0.0755333333],
        [0.9763, 0.9831, 0.0538],
    ],
)

default_cmap = matplotlib.cm.get_cmap("jet")


# Colourbar from Diana.
diana_colors = np.array(
    [
        [255, 0, 0],
        [255, 72, 0],
        [255, 145, 0],
        [255, 218, 0],
        [218, 255, 0],
        [145, 255, 0],
        [72, 255, 0],
        [0, 255, 0],
        [0, 255, 72],
        [0, 255, 145],
        [0, 255, 218],
        [0, 218, 255],
        [0, 145, 255],
        [0, 72, 255],
        [0, 0, 255],
    ]
)  # R -> G -> B
diana_colors = diana_colors / 255
diana_r = np.interp(
    np.linspace(0, 1, 256), np.linspace(0, 1, len(diana_colors)), diana_colors.T[0]
)
diana_g = np.interp(
    np.linspace(0, 1, 256), np.linspace(0, 1, len(diana_colors)), diana_colors.T[1]
)
diana_b = np.interp(
    np.linspace(0, 1, 256), np.linspace(0, 1, len(diana_colors)), diana_colors.T[2]
)
diana_colors = [(diana_r[i], diana_g[i], diana_b[i]) for i in range(len(diana_r))]
diana_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("diana", diana_colors)
diana_cmap_r = matplotlib.colors.LinearSegmentedColormap.from_list(
    "diana_r", diana_colors[::-1]
)

# Colourbar from Axis.
axis_colors = np.array(
    [
        [118, 2, 6],
        [185, 6, 17],
        [218, 10, 22],
        [253, 112, 34],
        [253, 186, 44],
        [255, 253, 56],
        [109, 253, 48],
        [58, 254, 188],
        [40, 230, 253],
        [31, 180, 252],
        [15, 85, 251],
        [10, 33, 236],
        [3, 17, 150],
        [1, 5, 183],
    ]
)  # R -> G -> B
axis_colors = axis_colors / 255
axis_r = np.interp(
    np.linspace(0, 1, 256), np.linspace(0, 1, len(axis_colors)), axis_colors.T[0]
)
axis_g = np.interp(
    np.linspace(0, 1, 256), np.linspace(0, 1, len(axis_colors)), axis_colors.T[1]
)
axis_b = np.interp(
    np.linspace(0, 1, 256), np.linspace(0, 1, len(axis_colors)), axis_colors.T[2]
)
axis_colors = [(axis_r[i], axis_g[i], axis_b[i]) for i in range(len(axis_r))]
axis_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("axis", axis_colors)
axis_cmap_r = matplotlib.colors.LinearSegmentedColormap.from_list(
    "axis_r", axis_colors[::-1]
)


class Color:
    bridge = "limegreen"
    lane = "gold"
    load = "crimson"
    pier = "limegreen"
    rebar = "crimson"
    response = "mediumorchid"
    response_axle = "cornflowerblue"


def sci_format_y_axis(points: int = 1):
    """Format y-axis ticks in scientific style."""

    class ScalarFormatterForceFormat(ScalarFormatter):
        def _set_format(self):
            self.format = f"%1.{points}f"

    plt.gca().yaxis.set_major_formatter(ScalarFormatterForceFormat())
    plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
