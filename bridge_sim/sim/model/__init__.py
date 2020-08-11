"""Classes for simulation parameters, mesh and simulation responses."""

import itertools
from collections import defaultdict
from typing import Optional, NewType, Dict, List, Tuple, Callable


import dill
import numpy as np
from scipy.interpolate import griddata, interp1d, interp2d
from scipy.spatial import distance

from bridge_sim.model import (
    Support,
    Material,
    Point,
    PointLoad,
    PierSettlement,
    ResponseType,
    Bridge,
    Config,
)
from bridge_sim.util import round_m, safe_str, nearest_index, print_i, print_w, print_d
from bridge_sim.sim.util import _responses_path, poly_area

D = False


class Node:
    """A node in a FE model.

    Args:
        n_id: the ID of this node.
        x: x position of this node on the bridge.
        y: y position of this node on the bridge.
        z: z position of this node on the bridge.
        deck: whether this node belongs to the bridge deck.
        pier: a pier that this node may belong to.
        comment: an optional comment for the .tcl file.
        support: a support that this node may belong to.

    Attrs:
        section: Material, a section that may be attached, or not.

    """

    def __init__(
        self,
        n_id: int,
        x: float,
        y: float,
        z: float,
        deck: bool,
        pier: Optional[Support] = None,
        comment: Optional[str] = None,
        support: Optional[Support] = None,
    ):
        self.n_id = n_id
        self.x = round_m(x)
        self.y = round_m(y)
        self.z = round_m(z)
        self.pier = pier
        self.deck = deck
        self.comment = comment
        self.support = support

    def command_3d(self):
        """OpenSees node command."""
        comment = "" if self.comment is None else f"; # {self.comment}"
        return (
            f"node {self.n_id} {round_m(self.x)} {round_m(self.y)}"
            + f" {round_m(self.z)}{comment}"
        )

    def distance(self, x: float, y: float, z: float):
        """Distance (with direction) from this node to coordinates."""
        return distance.euclidean((self.x, self.y, self.z), (x, y, z))

    def distance_n(self, node):
        """Distance (with direction) from this node to another node."""
        return self.distance(x=node.x, y=node.y, z=node.z)


NodesById = NewType("NodesById", Dict[int, Node])
# Nodes for a bridge deck.
DeckNodes = NewType("DeckNodes", List[List[Node]])
# A list of nodes for each shell.
DeckShellNodes = NewType("DeckShellNodes", List[Tuple[Node, Node, Node, Node]])
# Nodes for one wall of a pier. Indexed first by z then by x index.
WallNodes = NewType("WallNodes", List[List[Node]])
# Nodes for both walls of a single pier.
APierNodes = NewType("APierNodes", Tuple[WallNodes, WallNodes])
# Nodes for every pier.
PierNodes = NewType("PierNodes", List[APierNodes])
# Deck and pier nodes.
BridgeNodes = NewType("BridgeNodes", Tuple[DeckShellNodes, PierNodes])


class Shell:
    """A shell element in a FE model.

    NOTE: When this constructor is called additional work is done in setting a
    reference to the given section to all given nodes. Thus associating to each
    given node a section, this information that is attached to nodes is useful
    for creating colored plots of properties of the 3D model.

    Args:
        e_id: index for this shell element.
        ni_id: index of the node at corner i of this shell element.
        nj_id: index of the node at corner j of this shell element.
        nk_id: index of the node at corner k of this shell element.
        nl_id: index of the node at corner l of this shell element.
        section: section that this shell element belongs to.
        pier: whether this shell is on a pier.
        nodes_by_id: nodes in this build context.
        support_position_index: a 4-tuple of the support index, support wall
            index, and z and y indices

    """

    def __init__(
        self,
        e_id: int,
        ni_id: int,
        nj_id: int,
        nk_id: int,
        nl_id: int,
        section: Material,
        pier: bool,
        nodes_by_id: NodesById,
        support_position_index: Optional[Tuple[int, int, int, int]] = None,
    ):
        self.e_id = e_id
        self.ni_id = ni_id
        self.nj_id = nj_id
        self.nk_id = nk_id
        self.nl_id = nl_id
        self.pier = pier
        self.section = section
        self.support_position_index = support_position_index
        self.nodes_by_id = nodes_by_id
        self.deck = all(n.y == 0 for n in self.nodes())

        # Attach a reference to the section to each 'Node' and note if the node
        # belongs to a pier or to the bridge deck.
        for n_id in [self.ni_id, self.nj_id, self.nk_id, self.nl_id]:
            node = self.nodes_by_id[n_id]
            if pier:
                node.pier_section = self.section
            else:
                node.deck_section = self.section

    def node_ids(self):
        """IDs of this element's nodes."""
        return [self.ni_id, self.nj_id, self.nk_id, self.nl_id]

    def nodes(self):
        """This element's nodes."""
        return list(map(lambda n_id: self.nodes_by_id[n_id], self.node_ids()))

    def mass(self, config: Config):
        """Mass of this shell element: volume x density."""
        concrete_mass = self.section.thickness * self.area() * self.section.density
        # Asphalt only considered if Config flag set and is a deck shell.
        if not self.deck or not config.self_weight_asphalt:
            return concrete_mass
        z_min, z_max = self.width(min_max=True)
        assert z_min < z_max
        asphalt_mass = 0
        for lane in config.bridge.lanes:
            if lane.asphalt is None:
                continue
            assert lane.z_min < lane.z_max
            # Shell completely in the lane.
            if z_min >= lane.z_min and z_max <= lane.z_max:
                z_dist = z_max - z_min
            # Shell halfway in the lane.
            elif z_min < lane.z_min <= z_max <= lane.z_max:
                z_dist = z_max - lane.z_min
            # Shell halfway in the lane.
            elif lane.z_min <= z_min <= lane.z_max < z_max:
                z_dist = lane.z_max - z_min
            # Shell spanning the lane.
            elif z_min < lane.z_min and z_max > lane.z_max:
                z_dist = lane.z_max - lane.z_min
            else:
                continue
            z_frac = z_dist / self.width()
            assert 0 <= z_frac <= 1
            asphalt_mass += (
                lane.asphalt.thickness * self.area() * z_frac * lane.asphalt.density
            )
            print_d(
                D,
                f"Concrete density & asphalt density = {self.section.density}, {lane.asphalt.density}",
            )
        print_d(D, f"Concrete mass & asphalt mass = {concrete_mass}, {asphalt_mass}")
        return concrete_mass + asphalt_mass

    def area(self):
        """Assumes a tetrahedron shape."""
        ni = self.nodes_by_id[self.ni_id]
        nj = self.nodes_by_id[self.nj_id]
        nk = self.nodes_by_id[self.nk_id]
        nl = self.nodes_by_id[self.nl_id]

        return poly_area(
            [
                (ni.x, ni.y, ni.z),
                (nj.x, nj.y, nj.z),
                (nk.x, nk.y, nk.z),
                (nl.x, nl.y, nl.z),
            ]
        )

    def center(self) -> Point:
        """Point at the center of the element."""
        if not hasattr(self, "_center"):
            node_0 = self.nodes_by_id[self.ni_id]
            node_1 = self.nodes_by_id[self.nk_id]
            delta_x = abs(node_0.x - node_1.x)
            delta_y = abs(node_0.y - node_1.y)
            delta_z = abs(node_0.z - node_1.z)
            min_x = min(node_0.x, node_1.x)
            min_y = min(node_0.y, node_1.y)
            min_z = min(node_0.z, node_1.z)
            self._center = Point(
                x=min_x + delta_x / 2, y=min_y + delta_y / 2, z=min_z + delta_z / 2
            )
        return self._center

    def length(self) -> float:
        """The length of this element (longitudinal direction)."""
        if not hasattr(self, "_length"):
            min_x, max_x = np.inf, -np.inf
            for n_id in [self.ni_id, self.nj_id, self.nk_id, self.nl_id]:
                node_x = self.nodes_by_id[n_id].x
                if node_x < min_x:
                    min_x = node_x
                if node_x > max_x:
                    max_x = node_x
            self._length = max_x - min_x
        return self._length

    def width(self, min_max: bool = False) -> float:
        """The width of this element (transverse direction).

        Args:
            min_max: instead return a tuple of min and max Z position.

        """
        if min_max or not hasattr(self, "_width"):
            min_z, max_z = np.inf, -np.inf
            for n_id in [self.ni_id, self.nj_id, self.nk_id, self.nl_id]:
                node_z = self.nodes_by_id[n_id].z
                if node_z < min_z:
                    min_z = node_z
                if node_z > max_z:
                    max_z = node_z
            if min_max:
                return min_z, max_z
            self._width = max_z - min_z
        return self._width

    def command_3d(self):
        """OpenSees element command."""
        repr_section = repr(self.section).replace("\n", " ")
        return (
            f"element ShellMITC4 {self.e_id} {self.ni_id} {self.nj_id}"
            + f" {self.nk_id} {self.nl_id} {self.section.id}; # {repr_section}"
        )


ShellsById = NewType("ShellsById", Dict[int, Shell])
# Shells for a bridge deck.
DeckShells = NewType("DeckShells", List[List[Shell]])
# Shells for one wall of a pier. Indexed first by z then by x index.
WallShells = NewType("WallShells", List[List[Shell]])
# Shells for both walls of a pier.
APierShells = NewType("APierShells", Tuple[WallShells, WallShells])
# Shells for every pier.
PierShells = NewType("PierShells", List[APierShells])
# Deck and pier shells.
BridgeShells = NewType("BridgeShells", Tuple[DeckShells, PierShells])


class BuildContext:
    """Stores nodes and shells for a FEM being built.

    Args:
        add_loads: List[Point], additional grid lines where to add nodes.
        refinement_radii: List[float], radii for sweeps to refine around loads.

    """

    def __init__(
        self,
        add_loads: List[Point],
        refinement_radii: List[float] = [],
        # refinement_radii: List[float] = [2, 1, 0.5],
    ):
        self.next_n_id = 1
        self.nodes_by_id: NodesById = dict()
        self.nodes_by_pos = dict()
        # A dict of x to dict of y to dict of z to Node.
        self.nodes_by_pos_dict = defaultdict(lambda: defaultdict(dict))

        self.next_s_id = 1
        self.shells_by_id: ShellsById = dict()
        self.shells_by_n_ids = dict()

        self.add_loads = add_loads
        for point in self.add_loads:
            assert point.y == 0
        self.refinement_radii = refinement_radii

    def new_n_id(self):
        self.next_n_id += 1
        return self.next_n_id - 1

    def new_s_id(self):
        self.next_s_id += 1
        return self.next_s_id - 1

    def get_node(
        self, x: float, y: float, z: float, deck: bool, comment: Optional[str] = None
    ) -> Node:
        x, y, z = round_m(x), round_m(y), round_m(z)
        pos = (x, y, z)
        if pos not in self.nodes_by_pos:
            n_id = self.new_n_id()
            node = Node(n_id=n_id, x=x, y=y, z=z, deck=deck, comment=comment)
            self.nodes_by_id[n_id] = node
            self.nodes_by_pos[pos] = node
            self.nodes_by_pos_dict[x][y][z] = node
        return self.nodes_by_pos[pos]

    def get_shell(
        self,
        ni_id: int,
        nj_id: int,
        nk_id: int,
        nl_id: int,
        pier: bool,
        section: Material,
    ) -> Shell:
        n_ids = (ni_id, nj_id, nk_id, nl_id)
        if n_ids not in self.shells_by_n_ids:
            s_id = self.new_s_id()
            shell = Shell(
                e_id=s_id,
                ni_id=ni_id,
                nj_id=nj_id,
                nk_id=nk_id,
                nl_id=nl_id,
                pier=pier,
                section=section,
                nodes_by_id=self.nodes_by_id,
            )
            self.shells_by_n_ids[n_ids] = shell
            self.shells_by_id[s_id] = shell
        return self.shells_by_n_ids[n_ids]

    def get_nodes_at_xy(self, x: float, y: float):
        x, y = round_m(x), round_m(y)
        return self.nodes_by_pos_dict[x][y].values()


class SimParams:
    """Parameters for one FE simulation.

    Args:
        ploads: point loads to apply in the simulation.
        displacement_ctrl:  apply a load until a displacement is reached.
        axial_delta_temp: uniform thermal loading in Celcius.
        moment_delta_temp: linear thermal loading in Celcius.
        self_weight: apply loads corresponding to self-weight in simulation.

    """

    def __init__(
        self,
        ploads: List[PointLoad] = [],
        pier_settlement: List[PierSettlement] = [],
        axial_delta_temp: Optional[float] = None,
        moment_delta_temp: Optional[float] = None,
        self_weight: bool = False,
    ):
        self.ploads = ploads
        self.pier_settlement = pier_settlement
        self.axial_delta_temp = axial_delta_temp
        self.moment_delta_temp = moment_delta_temp
        self.self_weight = self_weight

    def build_ctx(self) -> BuildContext:
        """Build context from these simulation parameters.

        The build context only requires information on geometry.

        """
        return BuildContext(add_loads=[pload.point() for pload in self.ploads])

    def id_str(self, config: Config):
        """String representing the simulation parameters.

        NOTE: Response types are not included in the ID string because it is
        currently assumed that a simulation saves all output files.

        """
        load_str = ""
        if self.self_weight:
            load_str += "s"
            if config.self_weight_asphalt:
                load_str += "a"
        if self.axial_delta_temp is not None:
            load_str += f"temp-axial-{self.axial_delta_temp}"
        if self.moment_delta_temp is not None:
            load_str += f"temp-moment-{self.moment_delta_temp}"
        if len(self.ploads) > 0:
            pl_str = ",".join(pl.id_str() for pl in self.ploads)
            load_str += f"[{pl_str}]"
        if len(self.pier_settlement) > 0:
            load_str += ",".join(ps.id_str() for ps in self.pier_settlement)
        return safe_str(load_str)


class Responses:
    """Responses of one sensor type for one FE simulation."""

    def __init__(
        self,
        response_type: ResponseType,
        responses: List["Response"],
        build: bool = True,
        units: Optional[str] = None,
    ):
        assert isinstance(responses, list)
        if len(responses) == 0:
            raise ValueError("No fem found")
        assert isinstance(responses[0][1], Point)
        self.response_type = response_type
        self.units = units
        self.raw_responses = responses
        self.num_sensors = len(responses)
        # Nested dictionaries for indexing responses by position.
        self.responses = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        if build:
            for response, p in responses:
                self.responses[0][p.x][p.y][p.z] = response
            self.index()

    def index(self):
        """Create attributes for fast indexing of times and positions."""
        self.times = sorted(self.responses.keys())
        points = self.responses[self.times[0]]
        self.xs = sorted(points.keys())
        self.ys = {x: sorted(points[x].keys()) for x in self.xs}
        self.deck_xs = [x for x in self.xs if 0 in points[x].keys()]
        self.zs = {
            x: {y: sorted(points[x][y].keys()) for y in self.ys[x]} for x in self.xs
        }

    def deck_points(self) -> List[Point]:
        """All the points on the deck where fem are collected."""
        return [
            Point(x=x, y=0, z=z)
            for _, (x, y, z) in self.values(point=True)
            if np.isclose(y, 0)
        ]

    def add(self, values: List[float], points: List[Point]):
        """Add the values corresponding to given points.

        The points must already be in the fem.

        """
        assert len(values) == len(points)
        for v, p in zip(values, points):
            before = self.responses[0][p.x][p.y][p.z]
            self.responses[0][p.x][p.y][p.z] += v
            after = self.responses[0][p.x][p.y][p.z]
            # print(before, after)
        try:
            del self.griddata
        except AttributeError:
            pass
        return self

    def map(self, f, xyz: bool = False):
        """Map a function over the response values."""
        time = self.times[0]
        for x, y_dict in self.responses[time].items():
            for y, z_dict in y_dict.items():
                for z, response in z_dict.items():
                    if xyz:
                        self.responses[time][x][y][z] = f(response, x, y, z)
                    else:
                        self.responses[time][x][y][z] = f(response)
        try:
            del self.griddata
        except AttributeError:
            pass
        return self

    def without(self, remove: Callable[[Point, float], bool]) -> "Responses":
        responses = []
        for x, y_dict in self.responses[self.times[0]].items():
            for y, z_dict in y_dict.items():
                for z, response in z_dict.items():
                    p = Point(x=x, y=y, z=z)
                    if not remove(p, response):
                        responses.append((response, p))
                    # if abs(p.distance(of)) > radius:
        return Responses(
            response_type=self.response_type, responses=responses, units=self.units
        )

    def without_nan_inf(self):
        """Copy of these Responses without NaN or INF values."""
        return self.without(lambda p, r: np.isnan(r) or np.isinf(r))

    def add_temp_strain(
        self, config: Config, temp_deltas: Tuple[Optional[float], Optional[float]]
    ):
        """Convert responses, adding free and restrained strain."""
        if not self.response_type.is_strain():
            raise ValueError(f"Can only convert Strain not {self.response_type}")
        uniform_delta, linear_delta = temp_deltas
        if uniform_delta is not None and linear_delta is not None:
            raise ValueError("Must be ONLY uniform or linear temperature delta")
        if uniform_delta is not None:
            subtract = 1 * config.cte * uniform_delta
            print_i(f"Temperature post-processing, subtract strain = {subtract}")
            return self.map(lambda r: r - subtract)
        if linear_delta is not None:
            add = 0.5 * config.cte * linear_delta
            print_i(f"Temperature post-processing, adding strain = {add}")
            return self.map(lambda r: r + add)

    def to_stress(self, bridge: Bridge):
        """Convert strain responses to stress responses."""
        self.response_type = self.response_type.to_stress()
        if len(bridge.sections) == 1:
            youngs = bridge.sections[0].youngs
            self.map(lambda r: r * youngs)
        else:

            def _map(response, x, y, z):
                return response * bridge.deck_section_at(x=x, z=z).youngs

            self.map(_map, xyz=True)
        self.units = None  # We don't know units since strain is unit-less.
        return self

    def values(self, point: bool = False):
        """Yield each response value."""
        time = self.times[0]
        for x, y_dict in self.responses[time].items():
            for y, z_dict in y_dict.items():
                for z, response in z_dict.items():
                    if point:
                        yield response, (x, y, z)
                    else:
                        yield response

    def at_shells(self, shells: List["Shell"]) -> "Responses":
        responses = []
        for shell in shells:
            shell_center = shell.center()
            if shell_center.y != 0:
                raise ValueError("Can only get response on deck")
            responses.append((self.at_deck(shell_center, interp=False), shell_center))
        return Responses(response_type=self.response_type, responses=responses,)

    def at_deck(self, point: Point, interp: bool, grid_interp: bool = True):
        """Response at the deck (y = 0) with optional interpolation.

        NOTE: Interpolation cannot extrapolate to points outside known data.

        """
        assert point.y == 0
        if not interp:
            return self._at_deck_snap(x=point.x, z=point.z)
        return self._at_deck_interp(x=point.x, z=point.z, grid_interp=grid_interp)

    def at_decks(self, points: List[Point]) -> List[float]:
        """Like 'at_deck' with grid interpolation, but more efficient for many points.

        NOTE: Interpolation cannot extrapolate to points outside known data.

        """
        self._at_deck_interp(0, 0)  # Ensure the grid of points is calculated.
        xzs = np.array([[point.x, point.z] for point in points])
        points, values = self.griddata
        return griddata(points, values, xzs)
        # result = self.grid_interp2d(xzs[0].flatten(), xzs[1].flatten())[0]
        # return result

    def _at_deck_interp(self, x: float, z: float, grid_interp=True):
        # Assign to new variables, so they are not overwritten in loop.
        _x, _z = x, z
        # Determine grid of point and values for interpolation.
        if not hasattr(self, "griddata"):
            points = []
            values = []
            # For each x on the deck..
            for x in self.deck_xs:
                # for each z, for that x, determine value.
                for z in self.zs[x][0]:
                    points.append([x, z])
                    values.append(self.responses[0][x][0][z])
            self.griddata = np.array(points), np.array(values)
            # points = self.griddata[0].T
            # self.grid_interp2d = interp2d(points[0], points[1], values)
        # If grid interpolation selected then perform it.
        if grid_interp:
            points, values = self.griddata
            result = griddata(points, values, [[_x, _z]])[0]
            # result = self.grid_interp2d([_x], [_z])[0]
            # print(f"x = {_x}, z = {_z}, result = {result}")
            return result

    def _at_deck_snap(self, x: float, z: float):
        """Deck response from nearest available sensor."""
        y = 0
        x_ind = nearest_index(self.deck_xs, x)
        x_near = self.deck_xs[x_ind]
        z_ind = nearest_index(self.zs[x_near][y], z)
        z_near = self.zs[x_near][y][z_ind]
        return self.responses[0][x_near][y][z_near]


class SimResponses(Responses):
    """Responses of one sensor type for one FE simulation."""

    def __init__(
        self,
        c: Config,
        sim_params: SimParams,
        sim_runner: "FEMRunner",
        response_type: ResponseType,
        responses: List["Response"],
        build: bool = True,
    ):
        self.c = c
        self.sim_params = sim_params
        self.sim_runner = sim_runner
        super().__init__(response_type=response_type, responses=responses, build=build)

    def save(self):
        """Save theses simulation fem to disk."""
        path = _responses_path(
            config=self.c,
            sim_runner=self.sim_runner,
            sim_params=self.sim_params,
            response_type=self.response_type,
        )
        try:
            with open(path, "wb") as f:
                dill.dump(self.raw_responses, f)
        except:
            print("Could not save raw responses", flush=True)


def bridge_3d_nodes(deck_nodes: DeckNodes, all_support_nodes: PierNodes) -> List[Node]:
    """All a bridge's nodes in a deterministic order."""
    all_nodes = list(itertools.chain.from_iterable(deck_nodes))
    for support_nodes in all_support_nodes:
        for wall_nodes in support_nodes:
            for y_nodes in wall_nodes:
                for node in y_nodes:
                    all_nodes.append(node)
    assert isinstance(all_nodes[0], Node)
    assert isinstance(all_nodes[-1], Node)
    print_i(f"Total bridge nodes: {len(all_nodes)}")
    return all_nodes


def bridge_3d_elements(
    deck_elements: DeckShells, all_pier_elements: PierShells
) -> List[Shell]:
    """All a bridge's shell elements in a deterministic order."""
    all_elements = list(itertools.chain.from_iterable(deck_elements))
    for pier_element in all_pier_elements:
        all_elements.append(pier_element)
    assert isinstance(all_elements[0], Shell)
    assert isinstance(all_elements[-1], Shell)
    return all_elements
