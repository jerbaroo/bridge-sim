"""Build OpenSees 3D model files."""

import os
from collections import OrderedDict, defaultdict
from itertools import chain
from typing import List, Optional, Tuple

import numpy as np

from bridge_sim.model import PierSettlement, PointLoad, Config, Material
from bridge_sim.sim.model import (
    BuildContext,
    DeckNodes,
    DeckShells,
    Node,
    PierNodes,
    PierShells,
    SimParams,
)
from bridge_sim.sim.build import (
    det_nodes_id_str,
    det_shells_id_str,
    det_shells,
    get_bridge_shells_and_nodes,
    to_deck_nodes,
)
from bridge_sim.sim.run.opensees.build.d3.self_weight import opensees_self_weight_loads
from bridge_sim.sim.run.opensees.build.d3.thermal import (
    opensees_thermal_axial_deck_loads,
    opensees_thermal_moment_deck_loads,
)
from bridge_sim.sim.run.opensees.build.d3.util import comment
from bridge_sim.util import flatten, print_d, print_i, print_w, round_m


# Print debug information for this file.
# D: str = "fem.run.opensees.build.d3"
D: bool = False

##### Begin nodes #####


def opensees_support_nodes(
    c: Config, deck_nodes: DeckNodes, all_support_nodes: PierNodes,
) -> str:
    """Opensees node commands for the supports (ignoring deck).

    By 'ignoring deck' we mean that nodes that belong to both supports and the
    deck will not be returned by this function but instead by
    'opensees_deck_nodes'.

    Args:
        c: Config, global configuration object.
        deck_nodes: DeckNodes, to check for already added support nodes.
        all_support_nodes: AllSupportNodes, all support nodes to generate
            commands for.

    """
    # We want to avoid generating commands for support nodes that also belong to
    # the deck, thus we create a set for fast indexing to allow this check.
    deck_nodes = set(chain.from_iterable(deck_nodes))
    nodes = OrderedDict()
    # For each support.
    for s_nodes in all_support_nodes:
        # For each wall of the support (there are two).
        for w_nodes in s_nodes:
            # For each ~vertical line of nodes for a z position at top of wall.
            for y_nodes in w_nodes:
                # For each node in the ~vertical line.
                for y, node in enumerate(y_nodes):
                    # Insert the node, if not part of the deck nodes.
                    if node not in deck_nodes:
                        # A dictionary is used incase the node is already added,
                        # incase it is a bottom node shared by both walls.
                        nodes[node] = None
    return comment(
        "support nodes",
        "\n".join(map(lambda n: n.command_3d(), nodes.keys())),
        units="node nodeTag x y z",
    )


def opensees_deck_nodes(c: Config, deck_nodes: DeckNodes) -> str:
    """OpenSees node commands for a bridge deck.

    The nodes are created based on given positions of deck nodes.

    Args:
        c: Config, global configuratin object.

    """
    node_strings = []
    node_strings += list(
        map(lambda node: node.command_3d(), list(chain.from_iterable(deck_nodes)),)
    )
    return comment("deck nodes", "\n".join(node_strings), units="node nodeTag x y z")


##### End nodes #####
##### Begin fixed nodes #####


class FixNode:
    """A command to fix a node in some degrees of freedom (dof).

    Args:
        node: Node, the node with dof to fix specified.
        comment_: Optional[str], an optional comment for the command.

    """

    def __init__(
        self,
        node: Node,
        fix_x_translation: bool,
        fix_y_translation: bool,
        fix_z_translation: bool,
        fix_x_rotation: bool,
        fix_y_rotation: bool,
        fix_z_rotation: bool,
        comment: Optional[str] = None,
    ):
        self.node = node
        self.fix_x_translation = fix_x_translation
        self.fix_y_translation = fix_y_translation
        self.fix_z_translation = fix_z_translation
        self.fix_x_rotation = fix_x_rotation
        self.fix_y_rotation = fix_y_rotation
        self.fix_z_rotation = fix_z_rotation
        self.comment = comment

    def command_3d(self):
        """The command in string format for a TCL file."""
        # TODO: Update comment to include support ID.
        comment_ = "" if self.comment is None else f"; # {self.comment}"
        return (
            f"fix {self.node.n_id}"
            + f" {int(self.fix_x_translation)}"
            + f" {int(self.fix_y_translation)}"
            + f" {int(self.fix_z_translation)}"
            + f" {int(self.fix_x_rotation)}"
            + f" {int(self.fix_y_rotation)}"
            + f" {int(self.fix_z_rotation)}"
            + f"{comment_}"
        )


def opensees_fixed_abutment_nodes(
    c: Config, sim_params: SimParams, deck_nodes: DeckNodes
) -> str:
    """OpenSees fix commands for fixed nodes on the abument.

    Fixed for translation but not for rotation.

    """
    thermal = (sim_params.axial_delta_temp is not None) or (
        sim_params.moment_delta_temp is not None
    )
    fixed_nodes: List[FixNode] = []
    for i_x, x_nodes in enumerate(deck_nodes):
        assert len(x_nodes) >= 2
        for node in [x_nodes[0], x_nodes[-1]]:
            fixed_nodes.append(
                FixNode(
                    node=node,
                    fix_x_translation=False,
                    fix_y_translation=True,
                    fix_z_translation=True,
                    # fix_z_translation=(not thermal) or (i_x == (len(deck_nodes) // 2)),
                    fix_x_rotation=False,
                    fix_y_rotation=False,
                    fix_z_rotation=False,
                )
            )
    return comment(
        "fixed deck nodes",
        "\n".join(map(lambda f: f.command_3d(), fixed_nodes)),
        units="fix nodeTag x y z rx ry rz",
    )


def opensees_fixed_pier_nodes(
    c: Config,
    sim_params: SimParams,
    all_support_nodes: PierNodes,
    pier_disp: List[PierSettlement],
) -> str:
    """OpenSees fix commands for fixed support nodes."""
    # First, for thermal loading, we determine the piers at each longitudinal
    # (x) position, so for each x position we can then determine which piers
    # will be fixed in transverse (z) translation.
    pier_positions = defaultdict(set)
    for p_i, _ in enumerate(all_support_nodes):
        pier = c.bridge.supports[p_i]
        pier_positions[round_m(pier.x)].add(round_m(pier.z))
    pier_positions = {
        pier_x: sorted(pier_zs) for pier_x, pier_zs in pier_positions.items()
    }

    fixed_nodes: List[FixNode] = []
    # Iterate through each pier. Note that p_nodes is a tuple of nodes for each
    # pier wall. And each wall is a 2-d array of nodes.
    for p_i, p_nodes in enumerate(all_support_nodes):
        pier = c.bridge.supports[p_i]
        # If pier displacement for this pier then select the bottom central node
        # for the integrator command, and attach it to the pier.
        free_y_trans = False
        for ps in pier_disp:
            if p_i == ps.pier:
                free_y_trans = True
                pier = c.bridge.supports[ps.pier]
                pier.disp_node = p_nodes[0][len(p_nodes[0]) // 2][-1]
                if len(p_nodes[0]) % 2 == 0:
                    print_w("Pier settlement:")
                    print_w("  no central node (even number of nodes)")
        # For each ~vertical line of nodes for a z position at top of wall.
        for y_i, y_nodes in enumerate(p_nodes[0]):
            # We will fix the bottom node.
            node = y_nodes[-1]
            fixed_nodes.append(
                FixNode(
                    node=node,
                    fix_x_translation=pier.fix_x_translation,
                    fix_y_translation=False if free_y_trans else pier.fix_y_translation,
                    # fix_z_translation=fix_pier_z_translation(pier),
                    fix_z_translation=True,
                    fix_x_rotation=pier.fix_x_rotation,
                    fix_y_rotation=pier.fix_y_rotation,
                    fix_z_rotation=pier.fix_z_rotation,
                    comment=f"pier {p_i} y {y_i}",
                )
            )
    return comment(
        "fixed support nodes",
        "\n".join(map(lambda f: f.command_3d(), fixed_nodes)),
        units="fix nodeTag x y z rx ry rz",
    )


##### End fixed nodes #####
##### Begin sections #####


def opensees_section(section: Material):
    """OpenSees ElasticMembranePlateSection command for a Material."""
    # TODO: Implicit information, assumption that if young's modulus in x
    #     direction is modified that cracking is desired (poisson's set to 0).
    CRACK_Z = not np.isclose(section.youngs_x(), section.youngs)
    # New orthotropic method.
    return (
        f"nDMaterial ElasticOrthotropic {section.id}"
        f" {section.youngs_x() * 1E6} {section.youngs * 1E6} {section.youngs * 1E6}"
        f" {0 if CRACK_Z else section.poissons} {section.poissons} {section.poissons}"
        f" {(section.youngs * 1E6) / (2 * (1 + section.poissons))}"
        f" {(section.youngs * 1E6) / (2 * (1 + section.poissons))}"
        f" {(section.youngs * 1E6) / (2 * (1 + section.poissons))}"
        f" {section.density * 1E-3}"
        f"\nsection PlateFiber {section.id} {section.id} {section.thickness}"
    )
    # Old isotropic method.
    raise ValueError("Not using orthotropic method")
    return (
        f"section ElasticMembranePlateSection {section.id}"
        + f" {section.youngs * 1E6} {section.poissons} {section.thickness}"
        + f" {section.density * 1E-3}"
    )


def opensees_deck_sections(c: Config):
    """Sections used in the bridge deck."""
    return comment(
        "deck sections",
        "\n".join([opensees_section(section) for section in c.bridge.sections]),
        units=(
            "section ElasticMembranePlateSection secTag youngs_modulus"
            + " poisson_ratio depth mass_density"
        ),
    )


def opensees_pier_sections(c: Config, all_pier_elements: PierShells):
    """Sections used in the bridge's piers."""
    pier_shells = det_shells(all_pier_elements)
    # Some pier's may refer to the same section so we create a set to avoid
    # rendering duplicate section definitions into the .tcl file.
    pier_sections = set([pier_shell.section for pier_shell in pier_shells])
    return comment(
        "pier sections",
        "\n".join([opensees_section(section) for section in pier_sections]),
        units=(
            "section ElasticMembranePlateSection secTag youngs_modulus"
            + " poisson_ratio depth mass_density"
        ),
    )


##### End sections #####
##### Begin shell elements #####


def opensees_deck_elements(c: Config, deck_elements: DeckShells) -> str:
    """OpenSees element commands for a bridge deck."""
    deck_shells = det_shells(deck_elements)
    return comment(
        "deck shell elements",
        "\n".join(map(lambda e: e.command_3d(), deck_shells)),
        units="element ShellMITC4 eleTag iNode jNode kNode lNode secTag",
    )


def opensees_pier_elements(c: Config, all_pier_elements: PierShells) -> str:
    """OpenSees element commands for a bridge's piers."""
    pier_shells = det_shells(all_pier_elements)
    return comment(
        "pier shell elements",
        "\n".join(map(lambda e: e.command_3d(), pier_shells)),
        units="element ShellMITC4 eleTag iNode jNode kNode lNode secTag",
    )


# End shell elements #
# Begin loads #


def opensees_load(
    c: Config, pload: PointLoad, deck_nodes: DeckNodes,
):
    """An OpenSees load command."""
    assert deck_nodes[0][0].y == 0
    assert deck_nodes[-1][-1].y == 0
    best_node = sorted(
        chain.from_iterable(deck_nodes),
        key=lambda node: node.distance(x=pload.x, y=0, z=pload.z),
    )[0]

    assert np.isclose(best_node.y, 0)
    print(f"before assert load.x = {pload.x}")
    print(f"best_node_x = {best_node.x}")
    assert np.isclose(best_node.x, pload.x)
    assert np.isclose(best_node.z, pload.z)

    return f"load {best_node.n_id} 0 {pload.load} 0 0 0 0"


def opensees_loads(
    c: Config,
    ploads: List[PointLoad],
    deck_nodes: DeckNodes,
    pier_disp: List[PierSettlement],
):
    """OpenSees load commands for a .tcl file."""
    # In case of pier displacement apply load at the pier's central bottom node,
    # the load intensity doesn't matter though, only the position matters.
    if len(pier_disp) > 0:
        load_str = ""
        for ps in pier_disp:
            node = c.bridge.supports[ps.pier].disp_node
            load_str += f"\nload {node.n_id} 0 {ps.settlement * 1000} 0 0 0 0"
    # Otherwise find the deck nodes which best suit given point loads.
    else:
        load_str = "\n".join(
            opensees_load(c=c, pload=pload, deck_nodes=deck_nodes) for pload in ploads
        )

    return comment("loads", load_str, units="load nodeTag N_x N_y N_z N_rx N_ry N_rz")


##### End loads #####
##### Begin recorders #####


def opensees_translation_recorders(
    c: Config, fem_params: SimParams, os_runner: "OSRunner", ctx: BuildContext
) -> str:
    """OpenSees recorder commands for translation."""
    # A list of tuples of ResponseType and OpenSees direction index, for
    # translation response types, if requested in fem_params.response_types.
    translation_response_types = []
    # X translation.
    x_path = os_runner.x_translation_path(c, fem_params)
    translation_response_types.append((x_path, 1))
    print_i(f"OpenSees: saving x translation at {x_path}")
    # Y translation.
    y_path = os_runner.y_translation_path(c, fem_params)
    translation_response_types.append((y_path, 2))
    print_i(f"OpenSees: saving y translation at {y_path}")
    # Z translation.
    z_path = os_runner.z_translation_path(c, fem_params)
    translation_response_types.append((z_path, 3))
    print_i(f"OpenSees: saving z translation at {z_path}")

    # Append a recorder string for each response type (recording nodes).
    recorder_strs = []
    node_str = det_nodes_id_str(ctx)
    for response_path, direction in translation_response_types:
        print_d(D, f"Adding response path to build: {response_path}")
        recorder_strs.append(
            f"recorder Node -file {response_path} -node {node_str} -dof"
            + f" {direction} disp"
        )
    return comment(
        "translation recorders",
        "\n".join(recorder_strs),
        units="recorder Node -file path -node nodeTags -dof direction disp",
    )


def opensees_strain_recorders(
    c: Config, sim_params: SimParams, os_runner: "OSRunner", ctx: BuildContext
):
    """OpenSees recorder commands for translation."""
    return "\n".join(
        f"recorder Element"
        f" -file {os_runner.strain_path(config=c, sim_params=sim_params, point=point)}"
        f" -ele {det_shells_id_str(ctx)} material {str(point)} deformation"
        for point in [1, 2, 3, 4]
    )


def opensees_forces(
    config: Config, sim_params: SimParams, os_runner: "OSRunner", ctx: BuildContext
):
    return (
        f"recorder Element"
        f" -file {os_runner.forces_path(config=config, sim_params=sim_params)}"
        f" -ele {det_shells_id_str(ctx)} forces"
    )


def opensees_stress_variables(
    c: Config, sim_params: SimParams, os_runner: "OSRunner", ctx: BuildContext
) -> Tuple[str, str]:
    """OpenSees stress recorder variables.

    These replace <<ELEM_IDS>> and <<FORCES_OUT_FILE>> in the TCL file.

    """
    return (
        det_shells_id_str(ctx),
        os_runner.stress_path(config=c, sim_params=sim_params),
    )


def opensees_integrator(c: Config, pier_disp: List[PierSettlement]):
    """The integrator command to use based on FEMParams."""
    if len(pier_disp) > 0:
        node = c.bridge.supports[pier_disp[0].pier].disp_node
        if len(pier_disp) > 1:
            print_w(f"Using pier {pier_disp[0].pier} for DisplacementControl")
        return (
            f"integrator DisplacementControl {node.n_id} 2"
            + f" {pier_disp[0].settlement}"
        )
    return "integrator LoadControl 1"


def opensees_algorithm(pier_disp: List[PierSettlement]):
    """The algorithm command to use based on FEMParams."""
    if len(pier_disp) > 0:
        return "algorithm Linear"
    return "algorithm Newton"


def opensees_test(pier_disp: List[PierSettlement]):
    """The test command to use based on FEMParams."""
    if len(pier_disp) > 0:
        return ""
    return "test NormDispIncr 1.0e-12 1000"


##### End recorders #####


def build_model_3d(c: Config, expt_params: List[SimParams], os_runner: "OSRunner"):
    """Build OpenSees 3D model files.

    TODO: ExptParams -> SimParams.

    """
    # Read in the template model file.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.normpath(
        os.path.join(dir_path, "../../../../../../", c.os_3d_model_template_path)
    )
    with open(template_path) as f:
        in_tcl = f.read()

    # Build a model file for each simulation.
    for sim_params in expt_params:

        # Setup the 'BuildContext' for this simulation.
        sim_ctx = sim_params.build_ctx()
        # Determine nodes and shells.
        bridge_shells, bridge_nodes = get_bridge_shells_and_nodes(
            bridge=c.bridge, ctx=sim_ctx
        )
        deck_shells, pier_shells = bridge_shells
        deck_shell_nodes, pier_nodes = bridge_nodes
        deck_nodes = to_deck_nodes(deck_shell_nodes)
        # Attaching nodes and shells to the 'SimParams'. This allows the convert
        # process to build a deterministic list of nodes and shells. They should
        # be deleted again at that point.
        sim_params.bridge_shells = bridge_shells
        sim_params.bridge_nodes = bridge_nodes

        # Build the 3D model file by replacements in the template model file.
        out_tcl = (
            in_tcl.replace(
                "<<DECK_NODES>>", opensees_deck_nodes(c=c, deck_nodes=deck_nodes),
            )
            .replace(
                "<<SUPPORT_NODES>>",
                opensees_support_nodes(
                    c=c, deck_nodes=deck_nodes, all_support_nodes=pier_nodes,
                ),
            )
            .replace(
                "<<FIX_DECK>>",
                opensees_fixed_abutment_nodes(
                    c=c, sim_params=sim_params, deck_nodes=deck_nodes
                ),
            )
            .replace(
                "<<FIX_SUPPORTS>>",
                opensees_fixed_pier_nodes(
                    c=c,
                    sim_params=sim_params,
                    all_support_nodes=pier_nodes,
                    pier_disp=sim_params.pier_settlement,
                ),
            )
            .replace(
                "<<LOAD>>",
                opensees_loads(
                    c=c,
                    ploads=sim_params.ploads,
                    deck_nodes=deck_nodes,
                    pier_disp=sim_params.pier_settlement,
                ),
            )
            .replace(
                "<<THERMAL_AXIAL_LOAD_DECK>>",
                opensees_thermal_axial_deck_loads(
                    c=c, sim_params=sim_params, deck_elements=deck_shells, ctx=sim_ctx,
                ),
            )
            .replace(
                "<<THERMAL_MOMENT_LOAD_DECK>>",
                opensees_thermal_moment_deck_loads(
                    c=c, sim_params=sim_params, deck_elements=deck_shells, ctx=sim_ctx,
                ),
            )
            .replace(
                "<<SELF_WEIGHT>>",
                opensees_self_weight_loads(c, sim_params, deck_shells),
            )
            .replace("<<SUPPORTS>>", "")
            .replace("<<DECK_SECTIONS>>", opensees_deck_sections(c=c))
            .replace(
                "<<TRANS_RECORDERS>>",
                opensees_translation_recorders(
                    c=c, fem_params=sim_params, os_runner=os_runner, ctx=sim_ctx
                ),
            )
            .replace(
                "<<FORCES>>",
                opensees_forces(
                    config=c, sim_params=sim_params, os_runner=os_runner, ctx=sim_ctx
                ),
            )
            .replace(
                "<<DECK_ELEMENTS>>",
                opensees_deck_elements(c=c, deck_elements=deck_shells),
            )
            .replace(
                "<<PIER_ELEMENTS>>",
                opensees_pier_elements(c=c, all_pier_elements=pier_shells),
            )
            .replace(
                "<<PIER_SECTIONS>>",
                opensees_pier_sections(c=c, all_pier_elements=pier_shells),
            )
            .replace(
                "<<INTEGRATOR>>",
                opensees_integrator(c=c, pier_disp=sim_params.pier_settlement),
            )
            .replace("<<ALGORITHM>>", opensees_algorithm(sim_params.pier_settlement))
            .replace("<<TEST>>", opensees_test(sim_params.pier_settlement))
        )

        elem_ids, forces_out_file = opensees_stress_variables(
            c=c, sim_params=sim_params, os_runner=os_runner, ctx=sim_ctx
        )
        out_tcl = out_tcl.replace("<<ELEM_IDS>>", elem_ids).replace(
            "<<FORCES_OUT_FILE>>", forces_out_file
        )
        out_tcl = out_tcl.replace(
            "<<STRAIN_RECORDERS>>",
            opensees_strain_recorders(
                c=c, sim_params=sim_params, os_runner=os_runner, ctx=sim_ctx
            ),
        )

        # Write the generated model file.
        model_path = os_runner.sim_model_path(
            config=c, sim_params=sim_params, ext="tcl"
        )
        with open(model_path, "w") as f:
            f.write(out_tcl)
        num_nodes = len(set(flatten(bridge_nodes, Node)))
        print_i(f"OpenSees: saved 3D model ({num_nodes} nodes) file to {model_path}")

    return expt_params
