"""Build OpenSees 2D model files."""
from __future__ import annotations

import numpy as np

from lib.config import Config
from lib.fem.params import ExptParams, SimParams
from lib.model.bridge import Dimensions, Fix, Layer, Patch, Section
from lib.model.load import PierSettlement, PointLoad
from lib.model.response import ResponseType
from util import print_d, print_i

# Print debug information for this file.
D: bool = False


def opensees_nodes(c: Config):
    """OpenSees node commands for a .tcl file."""
    return "\n".join(
        f"node {i + 1} {c.os_node_step * i} 0" for i in np.arange(c.os_num_nodes())
    )


def opensees_supports(c: Config):
    """OpenSees support command for a .tcl file.

    When 2D modeling these are fixed node commands.

    """

    def opensees_fixed_node(f: Fix):
        node = np.interp(f.x_frac, (0, 1), (1, c.os_num_nodes()))
        return f"fix {int(node)} {int(f.x)} {int(f.y)} {int(f.rot)}"

    if c.bridge.dimensions == Dimensions.D2:
        return "\n".join(opensees_fixed_node(f) for f in c.bridge.supports)
    else:
        raise ValueError("We don't support 3D supports.")


def opensees_elements(c: Config):
    """OpenSees element commands for a .tcl file."""

    def opensees_element(left_nid):
        return f"element dispBeamColumn {left_nid} {left_nid} {left_nid + 1}" + " 5 1 1"

    return "\n".join(opensees_element(nid) for nid in c.os_node_ids()[:-1])


def opensees_loads(c: Config, fem_params: SimParams):
    """OpenSees load commands for a .tcl file."""

    def opensees_load(l: PointLoad):
        nid = int(np.interp(l.x_frac, (0, 1), (1, c.os_num_nodes())))
        return f"load {nid} 0 {l.kn * 1000} 0"

    if fem_params.displacement_ctrl is not None:
        fix = c.bridge.supports[fem_params.displacement_ctrl.pier]
        # NOTE: The z_frac argument is ignored by the 2D simulation.
        # NOTE: The applied load intensity (kn argument) is ignored by OpenSees
        # for displacement control, I think..
        return opensees_load(PointLoad(x_frac=fix.x_frac, z_frac=None, kn=10))

    return "\n".join(opensees_load(l) for l in fem_params.ploads)


def opensees_sections(c: Config):
    """OpenSees section commands for a .tcl file."""

    def opensees_patch(p: Patch):
        # NOTE: the y and x coordinates are opposite to OpenSees documentation.
        return (
            f"patch rect {p.material.value} 1 {p.num_sub_div_z}"
            + f" {p.p0.z} {p.p0.y} {p.p1.z} {p.p1.y}"
        )

    def opensees_layer(l: Layer):
        # NOTE: the y and x coordinates are opposite to OpenSees documentation.
        return (
            f"layer straight {l.material.value} {l.num_fibers}"
            + f" {l.area_fiber} {l.p0.z} {l.p0.y} {l.p1.z} {l.p1.y}"
        )

    def opensees_section(s: Section):
        return (
            f"section Fiber {s.id} {{"
            + "\n\t"
            + "\n\t".join(opensees_patch(p) for p in s.patches)
            + "\n\t"
            + "\n\t".join(opensees_layer(l) for l in s.layers)
            + "\n}"
        )

    return "\n".join(opensees_section(s) for s in c.bridge.sections)


def opensees_recorders(c: Config, os_runner: "OSRunner", fem_params: SimParams):
    """OpenSees recorder commands for a .tcl file."""
    response_types = fem_params.response_types
    recorders = ""

    node_recorders = []
    if ResponseType.XTranslation in response_types:
        node_recorders.append((os_runner.x_translation_path(fem_params), 1))

    if ResponseType.YTranslation in response_types:
        node_recorders.append((os_runner.y_translation_path(fem_params), 2))

    if len(node_recorders) > 0:
        for node_out_file, dof in node_recorders:
            recorders += f"\nrecorder Node -file {node_out_file}"
            recorders += " -node " + " ".join(map(str, c.os_node_ids()))
            recorders += f" -dof {dof} disp"
        recorders += f"\nrecorder Element -file"
        recorders += f" {os_runner.element_path(fem_params)}"
        recorders += " -ele " + " ".join(map(str, c.os_elem_ids()))
        recorders += " globalForce"

    if ResponseType.Stress in response_types or ResponseType.Strain in response_types:

        # Record stress and strain for each patch.
        for patch in c.bridge.sections[0].patches:
            for (point, point_path) in zip(
                patch.points(), os_runner.patch_paths(fem_params, patch)
            ):
                recorders += (
                    f"\nrecorder Element -file {point_path}"
                    + " -ele "
                    + " ".join(map(str, c.os_elem_ids()))
                    + f" section 1 fiber {point.z} {point.y}"
                    + " stressStrain"
                )

        # Record stress and strain for each fiber in a layer.
        for layer in c.bridge.sections[0].layers:
            for (point, point_path) in zip(
                layer.points(), os_runner.layer_paths(fem_params, layer)
            ):
                recorders += (
                    f"\nrecorder Element -file {point_path}"
                    + " -ele "
                    + " ".join(map(str, c.os_elem_ids()))
                    + f" section 1 fiber {point.z} {point.y}"
                    + " stressStrain"
                )
    return recorders


def opensees_test(c: Config, displacement_ctrl: PierSettlement):
    """OpenSees test command."""
    if displacement_ctrl is None:
        return ""
    return "test NormDispIncr 1.0e-12 100"


def opensees_algorithm(c: Config, displacement_ctrl: PierSettlement):
    """OpenSees algorithm command."""
    if displacement_ctrl is None:
        return "algorithm Linear"
    return "algorithm Newton"


def opensees_integrator(c: Config, displacement_ctrl: PierSettlement):
    """OpenSees integrator command."""
    if displacement_ctrl is None:
        return "integrator LoadControl 1"
    fix = c.bridge.supports[displacement_ctrl.pier]
    nid = int(np.interp(fix.x_frac, (0, 1), (1, c.os_num_nodes())))
    return (
        f"integrator DisplacementControl {nid} 2" + f" {displacement_ctrl.displacement}"
    )


def opensees_materials(c: Config, displacement_ctrl: PierSettlement):
    """OpenSees material commands."""
    if displacement_ctrl is None:
        # In standard case return:
        # - Concrete: nonlinear with linear tension softening.
        # - Steel: uniaxial bilinear with strain hardening.
        return """
uniaxialMaterial Concrete02 1 -2.8800000e+07 -1.6044568e-03 -2.8800000e+07 -3.5000000e-03 2.0000000e-01 2.8800000e+06 3.5900000e+10
uniaxialMaterial Steel01    2 3.4800000e+08  2.0000000e+11  0.0000000e+00
"""
    # In displacement control case use linear elastic.
    return """
uniaxialMaterial Elastic 1 3.59e+10
uniaxialMaterial Elastic 2 2.0000000e+11
"""


def build_model_2d(c: Config, expt_params: ExptParams, os_runner: "OSRunner"):
    """Build OpenSees 2D model files."""
    # Read in the template model file.
    with open(c.os_model_template_path) as f:
        in_tcl = f.read()
    # Build a model file for each simulation.
    for fem_params in expt_params.fem_params:
        print_i(
            f"OpenSees: building 2D model, {c.os_num_nodes()} nodes,"
            + f" {c.os_node_step} node step"
        )
        # For displacement control the support in question must not be fixed in
        # y translation.
        if fem_params.displacement_ctrl is not None:
            print_d(D, "Displacement control!")
            fix = c.bridge.supports[fem_params.displacement_ctrl.pier]
            if fix.y:
                nid = int(np.interp(fix.x_frac, (0, 1), (1, c.os_num_nodes())))
                raise ValueError(
                    f"Displacement control node ({nid}) not fixed in y" + " direction."
                )
        # Replace template with generated TCL code.
        out_tcl = (
            in_tcl.replace("<<NODES>>", opensees_nodes(c))
            .replace("<<SUPPORTS>>", opensees_supports(c))
            .replace(
                "<<MATERIALS>>", opensees_materials(c, fem_params.displacement_ctrl),
            )
            .replace("<<ELEMENTS>>", opensees_elements(c))
            .replace("<<LOAD>>", opensees_loads(c, fem_params))
            .replace("<<SECTIONS>>", opensees_sections(c))
            .replace("<<TEST>>", opensees_test(c, fem_params.displacement_ctrl))
            .replace(
                "<<ALGORITHM>>", opensees_algorithm(c, fem_params.displacement_ctrl),
            )
            .replace(
                "<<INTEGRATOR>>", opensees_integrator(c, fem_params.displacement_ctrl),
            )
            .replace("<<RECORDERS>>", opensees_recorders(c, os_runner, fem_params))
        )
        # Write the generated model file.
        model_path = os_runner.fem_file_path(fem_params=fem_params, ext="tcl")
        with open(model_path, "w") as f:
            f.write(out_tcl)
        print_i(f"OpenSees: saved 2D model file to {model_path}")
    return expt_params
