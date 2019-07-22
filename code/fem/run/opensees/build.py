"""
Build an OpenSees model file from a configuration.
"""
import numpy as np

from config import Config
from fem.params import ExptParams, FEMParams
from fem.run import FEMRunner, fem_file_path
from model import *
from util import *


def opensees_nodes(c: Config):
    """OpenSees node commands for a .tcl file."""
    return "\n".join(
        f"node {i + 1} {c.os_node_step * i} 0"
        for i in np.arange(c.os_num_nodes()))


def opensees_fixed_nodes(c: Config):
    """OpenSees fixed node commands for a .tcl file."""
    def opensees_fixed_node(f: Fix):
        node = np.interp(f.x_frac, (0, 1), (1, c.os_num_nodes()))
        return f"fix {int(node)} {int(f.x)} {int(f.y)} {int(f.rot)}"
    return "\n".join(opensees_fixed_node(f) for f in c.bridge.fixed_nodes)


def opensees_elements(c: Config):
    """OpenSees element commands for a .tcl file."""
    def opensees_element(left_nid):
        return (f"element dispBeamColumn {left_nid} {left_nid} {left_nid + 1}"
                + " 5 1 1")
    return "\n".join(opensees_element(nid) for nid in c.os_node_ids()[:-1])


def opensees_loads(c: Config, fem_params: FEMParams):
    """OpenSees load commands for a .tcl file."""
    def opensees_load(l: Load):
        nid = int(np.interp(l.x_frac, (0, 1), (1, c.os_num_nodes())))
        return f"load {nid} 0 {l.kn} 0"
    if fem_params.displacement_ctrl is not None:
        fix = c.bridge.fixed_nodes[fem_params.displacement_ctrl.pier]
        return opensees_load(Load(x_frac=fix.x_frac, kn=10))
    return "\n".join(opensees_load(l) for l in fem_params.loads)


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


def opensees_recorders(c: Config, fem_runner: FEMRunner,
                       fem_params: FEMParams):
    """OpenSees recorder commands for a .tcl file."""
    response_types = fem_params.response_types
    recorders = ""

    node_recorders = []
    if ResponseType.XTranslation in response_types:
        node_recorders.append(
            (fem_runner.x_translation_path(fem_params), 1))
    if ResponseType.YTranslation in response_types:
        node_recorders.append(
            (fem_runner.y_translation_path(fem_params), 2))
    if len(node_recorders) > 0:
        for node_out_file, dof in node_recorders:
            recorders += f"\nrecorder Node -file {node_out_file}"
            recorders += " -node " + " ".join(map(str, c.os_node_ids()))
            recorders += f" -dof {dof} disp"
        recorders += f"\nrecorder Element -file"
        recorders += f" {fem_runner.element_path(fem_params)}"
        recorders += " -ele " + " ".join(map(str, c.os_elem_ids()))
        recorders += " globalForce"

    if (ResponseType.Stress in response_types or
            ResponseType.Strain in response_types):
        # Record stress and strain for each patch.
        for patch in c.bridge.sections[0].patches:
            point = patch.center()
            recorders += (f"\nrecorder Element -file"
                        + f" {fem_runner.patch_path(fem_params, patch)}"
                        + " -ele " + " ".join(map(str, c.os_elem_ids()))
                        + f" section 1 fiber {point.y} {point.z} stressStrain")
        # Record stress and strain for each fiber in a layer.
        for layer in c.bridge.sections[0].layers:
            for (point, point_path) in zip(
                    layer.points(), fem_runner.layer_paths(fem_params, layer)):
                recorders += (f"\nrecorder Element -file {point_path}"
                              + " -ele " + " ".join(map(str, c.os_elem_ids()))
                              + f" section 1 fiber {point.y} {point.z}"
                              + " stressStrain")
    return recorders


def opensees_test(c: Config, displacement_ctrl: DisplacementCtrl):
    """OpenSees test command."""
    if displacement_ctrl is None:
        return ""
    return "test NormDispIncr 1.0e-12 100"


def opensees_algorithm(c: Config, displacement_ctrl: DisplacementCtrl):
    """OpenSees algorithm command."""
    if displacement_ctrl is None:
        return "algorithm Linear"
    return "algorithm Newton"


def opensees_integrator(c: Config, displacement_ctrl: DisplacementCtrl):
    """OpenSees integrator command."""
    if displacement_ctrl is None:
        return "integrator LoadControl 1"
    fix = c.bridge.fixed_nodes[displacement_ctrl.pier]
    nid = int(np.interp(fix.x_frac, (0, 1), (1, c.os_num_nodes())))
    return (f"integrator DisplacementControl {nid} 2"
            + f" {displacement_ctrl.displacement}")


def build_model(c: Config, expt_params: ExptParams, fem_runner: FEMRunner):
    """Build OpenSees model files."""
    for fem_params in expt_params.fem_params:
        print_i(f"OpenSees: building model file with"
                + f" {c.os_num_elems()} elements,"
                + f" {c.os_node_step} element length")
        with open(c.os_model_template_path) as f:
            in_tcl = f.read()
        out_tcl = (in_tcl
            .replace("<<NODES>>", opensees_nodes(c))
            .replace("<<FIX>>", opensees_fixed_nodes(c))
            .replace("<<ELEMENTS>>", opensees_elements(c))
            .replace("<<LOAD>>", opensees_loads(c, fem_params))
            .replace("<<SECTIONS>>", opensees_sections(c))
            .replace("<<TEST>>", opensees_test(
                c, fem_params.displacement_ctrl))
            .replace("<<ALGORITHM>>", opensees_algorithm(
                c, fem_params.displacement_ctrl))
            .replace("<<INTEGRATOR>>", opensees_integrator(
                c, fem_params.displacement_ctrl))
            .replace("<<RECORDERS>>", opensees_recorders(
                c, fem_runner, fem_params)))
        model_path = fem_file_path(fem_params, fem_runner)
        print_i(f"OpenSees: saving model file to {model_path}")
        with open(model_path, "w") as f:
            f.write(out_tcl)
    return expt_params
