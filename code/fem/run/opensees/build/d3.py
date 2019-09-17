"""Build OpenSees 3D model files."""
import itertools
from typing import List, Tuple

from config import Config
from fem.params import ExptParams
from util import print_d, print_i, round_m

# Print debug information for this file.
D: bool = False

# Begin node IDs #

_node_id = None


def next_node_id() -> int:
    """Return the next node ID and increment the counter."""
    global _node_id
    result = _node_id
    _node_id = result + 1
    return result


def reset_node_ids():
    """Reset node IDs to 0, e.g. when building a new model file."""
    global _node_id
    _node_id = 0


def ff_node_ids(mod: int):
    """Fast forward node IDs until divisible by "mod"."""
    global _node_id
    while _node_id % mod != 0:
        _node_id += 1


def next_pow_10(n: int):
    """Power of 10 greater than n."""
    pow_10 = 1
    while pow_10 <= n:
        pow_10 = pow_10 * 10
    return pow_10


##### End node IDs #####
##### Begin nodes #####


class Node:
    def __init__(self, n_id: int, x: float, y: float, z: float):
        self.n_id = n_id
        self.x = x
        self.y = y
        self.z = z
    def tcl(self):
        return (f"node {self.n_id} {round_m(self.x)} {round_m(self.y)}"
                + f" {round_m(self.z)}")


def opensees_deck_nodes(c: Config) -> Tuple[str, List[List[Node]]]:
    """OpenSees node commands for the bridge deck for a .tcl file."""
    num_nodes_x = c.bridge.length / c.os_node_step + 1
    num_nodes_z = c.bridge.width / c.os_node_step_z + 1
    if num_nodes_x != int(num_nodes_x):
        raise ValueError(
            f"Bridge length {c.bridge.length} not evenly divisible by"
            + f" c.os_node_step {c.os_node_step}")
    if num_nodes_z != int(num_nodes_z):
        raise ValueError(
            f"Bridge width {c.bridge.width} not evenly divisible by"
            + f" c.os_node_step_z {c.os_node_step_z}")
    num_nodes_x = int(num_nodes_x)
    num_nodes_z = int(num_nodes_z)
    ff_mod = next_pow_10(num_nodes_x)
    print_i(ff_mod)
    z_pos = 0
    nodes = []
    for num_z in range(num_nodes_z):
        # Fast forward node IDs on each transverse (y) increment.
        ff_node_ids(ff_mod) 
        x_pos = 0
        nodes.append([])
        for num_x in range(num_nodes_x):
            nodes[-1].append(Node(next_node_id(), x=x_pos, y=0, z=z_pos))
            x_pos += c.os_node_step
        z_pos += c.os_node_step_z
    return (
        "\n".join(map(
            lambda n: n.tcl(),
            itertools.chain.from_iterable(nodes))),
        nodes)


def opensees_nodes(c: Config):
    reset_node_ids()
    deck_node_str, deck_nodes = opensees_deck_nodes(c)
    return deck_node_str


##### End nodes #####
##### Begin elements #####





##### End elements #####


def build_model(c: Config, expt_params: ExptParams, fem_runner: "OSRunner"):
    """Build OpenSees 3D model files."""
    # Read in the template model file.
    with open(c.os_3d_model_template_path) as f:
        in_tcl = f.read()
    # Build a model file for each simulation.
    for fem_params in expt_params.fem_params:
        num_nodes_x = c.bridge.length / c.os_node_step
        num_nodes_y = c.bridge.width / c.os_node_step
        print_i(f"OpenSees: building 3D model, {num_nodes_x} * {num_nodes_y}"
                + f" nodes, {c.os_node_step} node step")
        # Displacement control is not supported.
        if fem_params.displacement_ctrl is not None:
            raise ValueError("OpenSees: Displacement not supported in 3D")
        # Replace template with generated TCL code.
        out_tcl = (
            in_tcl
            .replace("<<NODES>>", opensees_nodes(c)))
        # Write the generated model file.
        model_path = fem_runner.fem_file_path(fem_params=fem_params, ext="tcl")
        with open(model_path, "w") as f:
            f.write(out_tcl)
        print_i(f"OpenSees: saved 3D model file to {model_path}")
    return expt_params
