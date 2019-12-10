"""Build OpenSees 3D model files."""
from collections import OrderedDict, defaultdict
from itertools import chain
from typing import Dict, List, Optional, Tuple

import numpy as np
from config import Config
from fem.params import ExptParams, SimParams
from fem.run.build import get_all_nodes, reset_nodes
from fem.run.build.elements import get_deck_elements, get_pier_elements
from fem.run.build.types import (
    AllPierElements,
    AllSupportNodes,
    DeckElements,
    DeckNodes,
    Node,
    ShellElement,
    bridge_3d_nodes,
)
from model.bridge import Section3D, Support3D
from model.load import DisplacementCtrl, PointLoad
from model.response import ResponseType
from util import print_d, print_i, print_w, round_m


# Print debug information for this file.
D: str = "fem.run.opensees.build.d3"
# D: bool = False

##### Begin some comment-related things #####

opensees_intro = """
# Programatically generated file.
#
# Units:
# - dimension: metre
# - force: newton
#
# Dimension order is
# - x: longitudinal
# - y: vertical
# - z: transverse"""


def comment(c: str, inner: str, units: Optional[str] = None):
    """Add 'Begin c' and 'End c' comments around an inner block.

    Optionally add another 'units' comment before the inner block.

    """
    units_str = "" if units is None else f"# {units}\n"
    return units_str + f"# Begin {c}\n" + inner + f"\n# End {c}"


##### End some comment-related things #####
##### Begin nodes #####


def opensees_support_nodes(
    c: Config,
    deck_nodes: DeckNodes,
    all_support_nodes: AllSupportNodes,
    simple_mesh: bool,
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
                    # Sanity check that all (and only these) of the pier's top
                    # nodes are part of the deck
                    if not simple_mesh:
                        assert (node in deck_nodes) == (y == 0)
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


def opensees_deck_nodes(c: Config, deck_nodes: List[List[Node]]) -> str:
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

    def __init__(self, node: Node, free_y: bool = False, comment: Optional[str] = None):
        self.node = node
        self.free_y = free_y
        self.comment = comment

    def command_3d(self):
        """The command in string format for a TCL file."""
        # TODO: Update comment to include support ID.
        comment_ = "" if self.comment is None else f"; # {self.comment}"
        if self.node.support is None:
            return f"fix {self.node.n_id} 1 1 1 0 0 0{comment_}"
        else:
            # print(f"******************")
            # print(f"Fixed support node")
            y_trans_fix = self.node.support.fix_y_translation
            if self.free_y:
                y_trans_fix = False
            return (
                f"fix {self.node.n_id}"
                + f" {int(self.node.support.fix_x_translation)}"
                + f" {int(y_trans_fix)}"
                + f" {int(self.node.support.fix_z_translation)}"
                + f" {int(self.node.support.fix_x_rotation)}"
                + f" {int(self.node.support.fix_y_rotation)}"
                + f" {int(self.node.support.fix_z_rotation)}"
                + f"{comment_}"
            )


def opensees_fixed_deck_nodes(c: Config, deck_nodes: DeckNodes) -> str:
    """OpenSees fix commands for fixed deck nodes."""
    fixed_nodes: List[FixNode] = []
    for x_nodes in deck_nodes:
        assert len(x_nodes) >= 2
        fixed_nodes.append(FixNode(x_nodes[0]))
        fixed_nodes.append(FixNode(x_nodes[-1]))
    return comment(
        "fixed deck nodes",
        "\n".join(map(lambda f: f.command_3d(), fixed_nodes)),
        units="fix nodeTag x y z rx ry rz",
    )


def opensees_fixed_pier_nodes(
    c: Config,
    all_support_nodes: AllSupportNodes,
    pier_disp: Optional[DisplacementCtrl] = None,
) -> str:
    """OpenSees fix commands for fixed support nodes."""
    fixed_nodes: List[FixNode] = []
    # Iterate through each pier. Note that p_nodes is a tuple of nodes for each
    # pier wall. And each wall is a 2-d array of nodes.
    for p, p_nodes in enumerate(all_support_nodes):
        # If pier displacement for this pier then select the bottom central node
        # for the integrator command, and attach it to the pier.
        free_y = False
        if (pier_disp is not None) and (p == pier_disp.pier):
            free_y = True
            pier = c.bridge.supports[pier_disp.pier]
            pier.disp_node = p_nodes[0][len(p_nodes[0]) // 2][-1]
            if len(p_nodes[0]) % 2 == 0:
                raise ValueError(
                    "Pier displacement requires odd number of nodes along pier"
                    " in the transverse direction"
                )
        # For each ~vertical line of nodes for a z position at top of wall.
        for y, y_nodes in enumerate(p_nodes[0]):
            # We will fix the bottom node.
            fixed_nodes.append(
                FixNode(
                    node=y_nodes[-1], free_y=free_y, comment=f"support {p+1} y {y+1}",
                )
            )
    return comment(
        "fixed support nodes",
        "\n".join(map(lambda f: f.command_3d(), fixed_nodes)),
        units="fix nodeTag x y z rx ry rz",
    )


##### End fixed nodes #####
##### Begin sections #####


def opensees_section(section: Section3D):
    """OpenSees ElasticMembranePlateSection command for a Section3D."""
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


def opensees_pier_sections(c: Config, all_pier_elements: AllPierElements):
    """Sections used in the bridge's piers."""
    # Some pier's may refer to the same section so we create a set to avoid
    # rendering duplicate section definitions into the .tcl file.
    pier_sections = set([pier_element.section for pier_element in all_pier_elements])
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


def opensees_deck_elements(c: Config, deck_elements: DeckElements) -> str:
    """OpenSees element commands for a bridge deck."""
    deck_elements = chain.from_iterable(deck_elements)
    return comment(
        "deck shell elements",
        "\n".join(map(lambda e: e.command_3d(), deck_elements)),
        units="element ShellMITC4 eleTag iNode jNode kNode lNode secTag",
    )


def opensees_pier_elements(c: Config, all_pier_elements: AllPierElements) -> str:
    """OpenSees element commands for a bridge's piers."""
    return comment(
        "pier shell elements",
        "\n".join(map(lambda e: e.command_3d(), all_pier_elements)),
        units="element ShellMITC4 eleTag iNode jNode kNode lNode secTag",
    )


##### End shell elements #####
##### Begin loads #####


def opensees_load(
    c: Config,
    pload: PointLoad,
    deck_nodes: DeckNodes,
    simple_mesh: bool,
    pier_disp: Optional[DisplacementCtrl] = None,
):
    """An OpenSees load command."""
    pload_z = c.bridge.z(z_frac=pload.z_frac)
    pload_x = c.bridge.x(x_frac=pload.x_frac)
    assert deck_nodes[0][0].y == 0
    assert deck_nodes[-1][-1].y == 0
    best_node = sorted(
        chain.from_iterable(deck_nodes),
        key=lambda node: node.distance(x=pload_x, y=0, z=pload_z),
    )[0]

    if pier_disp is not None:
        pier = c.bridge.supports[pier_disp.pier]
        print_w(
            f"Distance of pier (under displacement) center to deck node"
            + f" {best_node.distance(x=pier.x, y=0, z=pier.z):.4f}m"
        )

    assert np.isclose(best_node.y, 0)
    # If we have a proper mesh then this should be the exact node.
    if not simple_mesh:
        assert np.isclose(best_node.x, pload_x)
        assert np.isclose(best_node.z, pload_z)

    return f"load {best_node.n_id} 0 {pload.kn * 1000000} 0 0 0 0"


def opensees_loads(
    c: Config,
    ploads: List[PointLoad],
    deck_nodes: DeckNodes,
    simple_mesh: bool,
    pier_disp: Optional[DisplacementCtrl],
):
    """OpenSees load commands for a .tcl file."""
    # In case of pier displacement apply load at the pier's central bottom node,
    # the load intensity doesn't matter though, only the position matters.
    if pier_disp is not None:
        node = c.bridge.supports[pier_disp.pier].disp_node
        load_str = f"load {node.n_id} 0 {c.pd_unit_load_kn * 1000} 0 0 0 0"
    # Otherwise find the deck nodes which best suit given point loads.
    else:
        load_str = "\n".join(
            opensees_load(
                c=c,
                pload=pload,
                deck_nodes=deck_nodes,
                simple_mesh=simple_mesh,
                pier_disp=pier_disp,
            )
            for pload in ploads
        )

    return comment("loads", load_str, units="load nodeTag N_x N_y N_z N_rx N_ry N_rz")


##### End loads #####
##### Begin recorders #####


def opensees_translation_recorders(
    c: Config, fem_params: SimParams, os_runner: "OSRunner"
) -> str:
    """OpenSees recorder commands for translation."""
    deck_nodes = fem_params.deck_nodes
    all_support_nodes = fem_params.all_support_nodes

    # A list of tuples of ResponseType and OpenSees direction index, for
    # translation response types, if requested in fem_params.response_types.
    translation_response_types = []
    if ResponseType.XTranslation in fem_params.response_types:
        x_path = os_runner.x_translation_path(fem_params)
        translation_response_types.append((x_path, 1))
        print_i(f"OpenSees: saving x translation at {x_path}")
    if ResponseType.YTranslation in fem_params.response_types:
        y_path = os_runner.y_translation_path(fem_params)
        translation_response_types.append((y_path, 2))
        print_i(f"OpenSees: saving y translation at {y_path}")
    if ResponseType.ZTranslation in fem_params.response_types:
        z_path = os_runner.z_translation_path(fem_params)
        translation_response_types.append((z_path, 3))
        print_i(f"OpenSees: saving z translation at {z_path}")

    # Append a recorder string for each response type (recording nodes).
    recorder_strs = []
    node_str = " ".join(
        str(n.n_id)
        for n in bridge_3d_nodes(
            deck_nodes=deck_nodes, all_support_nodes=all_support_nodes
        )
    )
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


from fem.run.build import nodes_by_id

node_ids_str = lambda: (" ".join(map(lambda n: str(sh.n_id), nodes_by_id.values())))


from fem.run.build.elements import shells_by_id

elem_ids_str = lambda: (" ".join(map(lambda sh: str(sh.e_id), shells_by_id.values())))


def opensees_strain_recorders(c: Config, sim_params: SimParams, os_runner: "OSRunner"):
    """OpenSees recorder commands for translation."""
    if not ResponseType.Strain in sim_params.response_types:
        return ""
    return "\n".join(
        f"recorder Element"
        f" -file {os_runner.strain_path(sim_params=sim_params, point=point)}"
        f" -ele {elem_ids_str()} material {str(point)} deformation"
        for point in [1, 2, 3, 4]
    )


def opensees_forces(sim_params: SimParams, os_runner: "OSRunner"):
    return (
        f"recorder Element"
        f" -file {os_runner.forces_path(sim_params)}"
        f" -ele 1 400 forces"
    )


def opensees_stress_variables(
    c: Config, sim_params: SimParams, os_runner: "OSRunner"
) -> Tuple[str, str]:
    """OpenSees stress recorder variables.

    These replace <<ELEM_IDS>> and <<FORCES_OUT_FILE>> in the TCL file.

    """
    if not ResponseType.Stress in sim_params.response_types:
        return "", os_runner.stress_path(sim_params)
    return elem_ids_str(), os_runner.stress_path(sim_params)


def opensees_integrator(c: Config, pier_disp: Optional[DisplacementCtrl]):
    """The integrator command to use based on FEMParams."""
    if pier_disp is None:
        return "integrator LoadControl 1"
    node = c.bridge.supports[pier_disp.pier].disp_node
    return (
        f"integrator DisplacementControl {node.n_id} 2" + f" {pier_disp.displacement}"
    )


def opensees_algorithm(pier_disp: Optional[DisplacementCtrl]):
    """The algorithm command to use based on FEMParams."""
    if pier_disp is None:
        return "algorithm Linear"
    return "algorithm Newton"


def opensees_test(pier_disp: Optional[DisplacementCtrl]):
    """The test command to use based on FEMParams."""
    if pier_disp is None:
        return ""
    return "test NormDispIncr 1.0e-12 1000"


##### End recorders #####


def build_model_3d(
    c: Config,
    expt_params: ExptParams,
    os_runner: "OSRunner",
    simple_mesh: bool = False,
):
    """Build OpenSees 3D model files.

    Args:
        c: Config, global configuration object.
        simple_mesh: bool, whether meshes for deck and for piers are based on
            simple grids of nodes without any refinement, for testing.

    """
    # Read in the template model file.
    with open(c.os_3d_model_template_path) as f:
        in_tcl = f.read()

    # Build a model file for each simulation.
    for fem_params in expt_params.sim_params:

        # Reset before building.
        # TODO: Remove.
        from fem.run.build.elements import reset_elem_ids

        reset_nodes()
        reset_elem_ids()

        # Attach deck and pier nodes and elements to the FEMParams to be
        # available when converting raw responses to responses with positions
        # attached.
        #
        # NOTE: there is some overlap between deck nodes and pier nodes, and
        # some over lap between nodes of both walls of one pier (at the bottom
        # where they meet).
        (
            fem_params.deck_nodes,
            fem_params.all_support_nodes,
            nodes_by_id,
        ) = get_all_nodes(c=c, sim_params=fem_params, simple_mesh=simple_mesh)
        fem_params.deck_elements = get_deck_elements(
            c=c, deck_nodes=fem_params.deck_nodes, nodes_by_id=nodes_by_id
        )
        fem_params.all_pier_elements = get_pier_elements(
            c=c,
            all_support_nodes=fem_params.all_support_nodes,
            nodes_by_id=nodes_by_id,
        )

        # Build the 3D model file by replacing each placeholder in the model
        # template file with OpenSees commands.
        out_tcl = (
            in_tcl.replace("<<INTRO>>", opensees_intro)
            .replace(
                "<<DECK_NODES>>",
                opensees_deck_nodes(c=c, deck_nodes=fem_params.deck_nodes),
            )
            .replace(
                "<<SUPPORT_NODES>>",
                opensees_support_nodes(
                    c=c,
                    deck_nodes=fem_params.deck_nodes,
                    all_support_nodes=fem_params.all_support_nodes,
                    simple_mesh=simple_mesh,
                ),
            )
            .replace(
                "<<FIX_DECK>>",
                opensees_fixed_deck_nodes(c=c, deck_nodes=fem_params.deck_nodes),
            )
            .replace(
                "<<FIX_SUPPORTS>>",
                opensees_fixed_pier_nodes(
                    c=c,
                    all_support_nodes=fem_params.all_support_nodes,
                    pier_disp=fem_params.displacement_ctrl,
                ),
            )
            .replace(
                "<<LOAD>>",
                opensees_loads(
                    c=c,
                    ploads=fem_params.ploads,
                    deck_nodes=fem_params.deck_nodes,
                    simple_mesh=simple_mesh,
                    pier_disp=fem_params.displacement_ctrl,
                ),
            )
            .replace("<<SUPPORTS>>", "")
            .replace("<<DECK_SECTIONS>>", opensees_deck_sections(c=c))
            .replace(
                "<<TRANS_RECORDERS>>",
                opensees_translation_recorders(
                    c=c, fem_params=fem_params, os_runner=os_runner
                ),
            )
            .replace(
                "<<FORCES>>",
                opensees_forces(sim_params=fem_params, os_runner=os_runner),
            )
            .replace(
                "<<DECK_ELEMENTS>>",
                opensees_deck_elements(c=c, deck_elements=fem_params.deck_elements),
            )
            .replace(
                "<<PIER_ELEMENTS>>",
                opensees_pier_elements(
                    c=c, all_pier_elements=fem_params.all_pier_elements
                ),
            )
            .replace(
                "<<PIER_SECTIONS>>",
                opensees_pier_sections(
                    c=c, all_pier_elements=fem_params.all_pier_elements
                ),
            )
            .replace(
                "<<INTEGRATOR>>",
                opensees_integrator(c=c, pier_disp=fem_params.displacement_ctrl),
            )
            .replace("<<ALGORITHM>>", opensees_algorithm(fem_params.displacement_ctrl),)
            .replace("<<TEST>>", opensees_test(fem_params.displacement_ctrl))
        )

        elem_ids, forces_out_file = opensees_stress_variables(
            c=c, sim_params=fem_params, os_runner=os_runner
        )
        out_tcl = out_tcl.replace("<<ELEM_IDS>>", elem_ids).replace(
            "<<FORCES_OUT_FILE>>", forces_out_file
        )
        out_tcl = out_tcl.replace(
            "<<STRAIN_RECORDERS>>",
            opensees_strain_recorders(c=c, sim_params=fem_params, os_runner=os_runner),
        )

        # Write the generated model file.
        model_path = os_runner.sim_raw_path(sim_params=fem_params, ext="tcl")
        with open(model_path, "w") as f:
            f.write(out_tcl)
        num_nodes = len(list(nodes_by_id.values()))
        print_i(f"OpenSees: saved 3D model ({num_nodes} nodes) file to {model_path}")

    return expt_params
