from enum import Enum

import numpy as np


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
        return f"fix {int(node)} {int(self.x)} {int(self.y)} {int(self.rot)}"


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
        return ( f"patch rect {self.material.value} 1 {self.num_sub_div_z} "
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
        return ( f"section Fiber {self.id} {{"
                 + "\n".join(p.to_opensees() for p in self.patches)
                 + "}}")
