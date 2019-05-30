from enum import Enum

import numpy as np

from util import print_i

MODEL_TEMPLATE = "2018_OpenSees/model-template.tcl"


class Fix():
    def __init__(self, x_pos, x=False, y=False, rot=False):
        self.x_pos = x_pos
        self.x = x
        self.y = y
        self.rot = rot

    def to_opensees(self):
        fixed_nodes = np.interp(
            list(map(lambda f: f.x_pos, fix)),
            (0, 1),
            (1, num_elems + 1)
        )
        fixed = ""
        fixed += f"\nfix {int(fixed_nodes[i])} "
        fixed += f"{int(fix[i].x)} {int(fix[i].y)} {int(fix[i].rot)}"


class Load():
    def __init__(self, x_pos, weight):
        self.x_pos = x_pos
        self.weight = weight


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Material(Enum):
    Concrete = 1
    Steel = 2


class Patch():
    def __init__(self, x0, y0, x1, y1, sub_div_z=30,
                 material=Material.Concrete):
        self.p0 = Point(x0, y0)
        self.p1 = Point(x1, y1)
        self.sub_div_z = sub_div_z
        self.material = material


def build_model(num_elems=300, node_start=0, node_step=0.2, fix=[], load=[],
                patches=[], in_file=MODEL_TEMPLATE, out_file="built-model.tcl",
                elem_out_file="elem.out", node_x_out_file="node-x.out",
                node_y_out_file="node-y.out",
                node_stress_strain_out_file="stress-strain.out"):
    """Build a .tcl file based on the given parameters."""
    print_i(f"Generating model file with\n\t{num_elems} elements"
            + f"\n\t{node_step} element length")
    with open(in_file) as f:
        in_tcl = f.read()

    # Nodes ###################################################################
    out_tcl = in_tcl.replace(
        "<<NODES>>",
        "\n".join(
            f"node {i + 1} {node_step * i + node_start} 0"
            for i in np.arange(num_elems + 1)
        )
    )

    # Fix #####################################################################
    fixed_nodes = np.interp(
        list(map(lambda f: f.x_pos, fix)),
        (0, 1),
        (1, num_elems + 1)
    )
    fixed = ""
    for i in range(len(fix)):
        fixed += f"\nfix {int(fixed_nodes[i])} "
        fixed += f"{int(fix[i].x)} {int(fix[i].y)} {int(fix[i].rot)}"
    out_tcl = out_tcl.replace("<<FIX>>", fixed)

    # Elements ################################################################
    out_tcl = out_tcl.replace(
        "<<ELEMENTS>>",
        "\n".join(
            f"element dispBeamColumn {i + 1} {i + 1} {i + 2} 5 1 1"
            for i in np.arange(num_elems)
        )
    )

    # Loads ###################################################################
    load_nodes = np.interp(
        list(map(lambda l: l.x_pos, load)),
        (0, 1),
        (1, num_elems + 1)
    )
    loads = ""
    for i in range(len(load)):
        loads += f"\nload {int(load_nodes[i])} 0 {load[i].weight} 0"
    out_tcl = out_tcl.replace("<<LOAD>>", loads)

    # Recorders ###############################################################
    recorders = ""
    for node_out_file, dof in [(node_x_out_file, 1), (node_y_out_file, 2)]:
        recorders += f"\nrecorder Node -file {node_out_file} -node "
        recorders += " ".join(map(str, np.arange(1, num_elems + 2)))
        recorders += f" -dof {dof} disp"
    recorders += f"\nrecorder Element -file {elem_out_file}"
    recorders += " -ele" + " ".join(map(str, np.arange(1, num_elems + 1)))
    recorders += " globalForce"

    recorders += f"\nrecorder Element -file {node_stress_strain_out_file}"
    recorders += " -ele " + " ".join(map(str, np.arange(1, num_elems + 2)))
    recorders += " section 1 fiber 0 0.5 stressStrain"
    out_tcl = out_tcl.replace("<<RECORDERS>>", recorders)

    with open(out_file, "w") as f:
        f.write(out_tcl)
    print_i(f"Saved model file to {out_file}")
