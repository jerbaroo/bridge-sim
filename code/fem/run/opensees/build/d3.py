"""Build OpenSees 3D model files."""
from config import Config
from fem.params import ExptParams
from util import print_d

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


# End node IDs #


def opensees_deck_nodes(c: Config):
    """OpenSees node commands for the bridge deck for a .tcl file."""
    nodes = []  # A list of tuples (node_id, x_coord, y_coord, z_coord).
    num_nodes_x = c.bridge.length / c.os_node_step
    num_nodes_y = c.bridge.width / c.os_node_step
    y_pos = 0
    for num_y in range(num_nodes_y):
        ff_node_ids() # Fast forward node IDs on each transverse (y) increment.
        x_pos = 0
        for num_x in range(num_nodes_x):
            nodes.append((next_node_id(), x_pos, y_pos, 0))
            x_pos += c.os_node_step
        y_pos += c.os_node_step
    return "\n".join(map(
        lambda (n_id, x, y, z): f"node {n_id} {x} {y} {z}",
        nodes))


def opensees_nodes(c: Config):
    reset_node_ids()
    return opensees_deck_nodes(c)


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
