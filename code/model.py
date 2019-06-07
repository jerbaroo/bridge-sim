from enum import Enum

import numpy as np


class Bridge():
    """Specification of a model of a bridge.

    Args:
        length: length of the beam.
        fixed_nodes: nodes fixed in some degrees of freedom.
        sections: specification of the cross section.
    """
    def __init__(self, length, fixed_nodes, sections=[]):
        self.length = length
        self.fixed_nodes = fixed_nodes
        self.sections = sections

    def __repr__(self):
        return f"Bridge\n\tLength = {self.length}\n\tFixed = {[]}"

    def x_axis(self, n):
        """N equidistant points along the bridge's length."""
        return np.interp(range(n), [0, n - 1], [0, self.length])


class Config():
    """Simulation parameters including a bridge model specification.

    Args:
        bridge: specification of a model of a bridge.
        node_start: position on the x-axis of the first node.
        node_step: distance between two nodes, or length of an element.

        # Parameters used for the influence line.
        il_mat_path_prefix: prefix of path where to save an IL matrix.
        il_num_loads: amount of positions at which to apply load.
        il_unit_load: the value of load to place on the bridge.
        il_save_time: time index to read the response after loading.

        # Parameters used for OpenSees.
        os_model_template_path: path of the model template file.
        os_built_model_path: path to save/load the built model.
        os_element_path: path to save element recorder data.
        os_x_path: path to save node x translation recorder data.
        os_y_path: path to save node y translation recorder data.
        os_stress_strain_path: path to save stress/strain recorder data.
    """
    def __init__(self, bridge, node_start=0, node_step=0.2,
                 il_mat_path_prefix="generated/il/il-matrix", il_num_loads=10,
                 il_unit_load=-5e4, il_save_time=1,
                 os_model_template_path="model-template.tcl",
                 os_built_model_path="generated/built-model.tcl",
                 os_element_path="generated/elem.out",
                 os_x_path="generated/node-x.out",
                 os_y_path="generated/node-y.out",
                 os_stress_strain_path="generated/stress-strain.out"):
        self.bridge = bridge
        self.node_start = node_start
        self.node_step = node_step
        def get_num_elems():
            result = int(self.bridge.length / self.node_step)
            assert result * self.node_step == self.bridge.length
            return result
        get_num_elems()
        self.num_elems = get_num_elems
        self.num_nodes = lambda: self.num_elems() + 1
        self.node_ids = lambda: np.arange(1, self.num_nodes() + 1)
        assert len(list(self.node_ids())) == self.num_nodes()
        self.elem_ids = lambda: np.arange(1, self.num_elems() + 1)
        assert len(list(self.elem_ids())) == self.num_elems()

        # Influence line parameters.
        self.il_mat_path_prefix = il_mat_path_prefix
        self.il_num_loads = il_num_loads
        self.il_unit_load = il_unit_load
        self.il_save_time = il_save_time
        def get_il_mat_path():
            return (f"{self.il_mat_path_prefix}-nl-{self.il_num_loads}"
                    + f"-ns-{self.num_elems()}-l-{self.il_unit_load}"
                    + f"-t-{il_save_time}.npy")
        self.il_mat_path = get_il_mat_path

        # OpenSees parameters.
        self.os_model_template_path = os_model_template_path
        self.os_built_model_path = os_built_model_path
        self.os_element_path = os_element_path
        self.os_x_path = os_x_path
        self.os_y_path = os_y_path
        self.os_stress_strain_path = os_stress_strain_path


class Fix():
    """An indexed node which is fixed in some degrees of freedom."""
    def __init__(self, x_pos, x=False, y=False, rot=False):
        self.x_pos = x_pos
        self.x = x
        self.y = y
        self.rot = rot


class Load():
    def __init__(self, x_pos, weight):
        self.x_pos = x_pos
        self.weight = weight


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
        return (f"patch rect {self.material.value} 1 {self.num_sub_div_z} "
                + f"{self.p0.y} {self.p0.z} {self.p1.y} {self.p1.z}")


class Point():
    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z


class Section():
    """A fiber section consisting of multiple patches."""
    next_id = 1
    def __init__(self, patches):
        self.id = Section.next_id
        Section.next_id += 1
        self.patches = patches

    def to_opensees(self):
        return (f"section Fiber {self.id} {{"
                + "\n".join(p.to_opensees() for p in self.patches)
                + "}}")
