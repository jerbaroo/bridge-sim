"""
Build an OpenSees model file from a configuration.
"""
import numpy as np

from config import Config
from model import *
from util import print_i


def opensees_nodes(c: Config):
    """OpenSees node commands for a .tcl file."""
    return "\n".join(
        f"node {i + 1} {c.os_node_step * i} 0"
        for i in np.arange(c.os_num_nodes()))


def opensees_fixed_nodes(c: Config):
    """OpenSees fixed node commands for a .tcl file."""
    def opensees_fixed_node(f: Fix):
        node = np.interp(f.x_pos, (0, 1), (1, c.os_num_nodes()))
        return f"fix {int(node)} {int(f.x)} {int(f.y)} {int(f.rot)}"
    return "\n".join(opensees_fixed_node(f) for f in c.bridge.fixed_nodes)


def opensees_elements(c: Config):
    """OpenSees element commands for a .tcl file."""
    def opensees_element(left_nid):
        return (f"element dispBeamColumn {left_nid} {left_nid} {left_nid + 1}"
                + " 5 1 1")
    return "\n".join(opensees_element(nid) for nid in c.os_node_ids()[:-1])


def opensees_loads(c: Config, loads: [Load]):
    """OpenSees load commands for a .tcl file."""
    def opensees_load(l: Load):
        nid = int(np.interp(l.x_pos, (0, 1), (1, c.os_num_nodes())))
        return f"load {nid} 0 {l.weight} 0"
    return "\n".join(opensees_load(l) for l in loads)


def opensees_sections(c: Config):
    """OpenSees section commands for a .tcl file."""
    def opensees_patch(p: Patch):
        return (f"patch rect {p.material.value} 1 {p.num_sub_div_z}"
                + f" {p.p0.y} {p.p0.z} {p.p1.y} {p.p1.z}")
    def opensees_layer(l: Layer):
        return (f"layer straight {l.material.value} {l.num_fibers}"
                + f" {l.area_fiber} {l.p0.y} {l.p0.z} {l.p1.y} {l.p1.z}")
    def opensees_section(s: Section):
        return (f"section Fiber {s.id} {{"
                + "\n\t" + "\n\t".join(opensees_patch(p) for p in s.patches)
                + "\n\t" + "\n\t".join(opensees_layer(l) for l in s.layers)
                + "\n}")
    return "\n".join(opensees_section(s) for s in c.bridge.sections)


def opensees_recorders(c: Config):
    """OpenSees recorder commands for a .tcl file."""
    recorders = ""
    for node_out_file, dof in [(c.os_x_path, 1), (c.os_y_path, 2)]:
        recorders += f"\nrecorder Node -file {node_out_file}"
        recorders += " -node " + " ".join(map(str, c.os_node_ids()))
        recorders += f" -dof {dof} disp"
    recorders += f"\nrecorder Element -file {c.os_element_path}"
    recorders += " -ele " + " ".join(map(str, c.os_elem_ids()))
    recorders += " globalForce"
    # Record stress and strain for each patch.
    for p in c.bridge.sections[0].patches:
        point = p.center()
        recorders += (f"\nrecorder Element -file"
                      + f" {c.os_stress_strain_path(p)}"
                      + " -ele " + " ".join(map(str, c.os_elem_ids()))
                      + f" section 1 fiber {point.y} {point.z} stressStrain")
    # Record stress and strain for each fiber in a layer.
    return recorders


def build_opensees_model(c: Config, loads=[]):
    """Build a .tcl file based on the given configuration."""
    print_i(f"Generating model file with"
            + f"\n\t{c.os_num_elems()} elements"
            + f"\n\t{c.os_node_step} element length")
    with open(c.os_model_template_path) as f:
        in_tcl = f.read()
    out_tcl = (in_tcl
        .replace("<<NODES>>", opensees_nodes(c))
        .replace("<<FIX>>", opensees_fixed_nodes(c))
        .replace("<<ELEMENTS>>", opensees_elements(c))
        .replace("<<LOAD>>", opensees_loads(c, loads))
        .replace("<<SECTIONS>>", opensees_sections(c))
        .replace("<<RECORDERS>>", opensees_recorders(c)))
    with open(c.os_built_model_path, "w") as f:
        f.write(out_tcl)
    print_i(f"Saved model file to {c.os_built_model_path}")
