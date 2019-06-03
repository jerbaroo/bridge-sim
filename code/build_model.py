from enum import Enum

import numpy as np

from util import print_i

MODEL_TEMPLATE = "2018_OpenSees/model-template.tcl"


class Fix():
    """An OpenSees fix command e.g. fix 43 0 1 0."""
    def __init__(self, x_pos, x=False, y=False, rot=False):
        self.x_pos = x_pos
        self.x = x
        self.y = y
        self.rot = rot

    def to_opensees(self, num_elems):
        node = np.interp(
            [self.x_pos],
            (0, 1),
            (1, num_elems + 1)
        )[0]
        fix = f"\nfix {int(node)}"
        fix += f" {int(self.x)} {int(self.y)} {int(self.rot)}"
        return fix


class Load():
    def __init__(self, x_pos, weight):
        self.x_pos = x_pos
        self.weight = weight


class Point():
    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z


class Material(Enum):
    Concrete = 1
    Steel = 2


class Patch():
    """A rectangular patch."""
    def __init__(self, y_i, z_i, y_j, z_j, num_sub_div_z=30,
                 material=Material.Concrete):
        self.p0 = Point(y=y_i, z=z_j)
        self.p1 = Point(y=y_i, z=z_j)
        self.num_sub_div_z = num_sub_div_z
        self.material = material

    def to_opensees(self):
        return ( f"patch rect {self.material.value} 1 {self.num_sub_div_z} "
                 + f"{self.p0.y} {self.p0.z} {self.p1.y} {self.p1.z}")


class Section():
    """A fiber section consisting of multiple patches."""
    next_id = 1
    def __init__(self, patches):
        self.id = Section.next_id
        Section.next_id += 1
        self.patches = patches

    def to_opensees(self):
        return ( f"section Fiber {self.id} {{"
                 + "\n".join(p.to_opensees() for p in self.patches)
                 + "}}")


def build_model(num_elems=300, node_start=0, node_step=0.2, fix=[], load=[],
                sections=[], in_file=MODEL_TEMPLATE,
                out_file="built-model.tcl", elem_out_file="elem.out",
                node_x_out_file="node-x.out", node_y_out_file="node-y.out",
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
    out_tcl = out_tcl.replace(
        "<<FIX>>",
        "\n".join(x.to_opensees(num_elems) for x in fix)
    )

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
        [l.x_pos for l in load],
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
