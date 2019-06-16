"""
Classes for describing bridges and loads.
"""
from enum import Enum

import numpy as np


class Bridge():
    """Description of a bridge.

    Args:
        length: length of the beam.
        fixed_nodes: nodes fixed in some degrees of freedom.
        sections: specification of the cross section.
    """
    def __init__(self, length, fixed_nodes, sections):
        self.length = length
        self.fixed_nodes = fixed_nodes
        self.sections = sections
        assert len(sections) == 1

    def x_axis(self, n):
        """n equidistant points along the bridge's length."""
        return np.interp(range(n), [0, n - 1], [0, self.length])


class Fix():
    """A node fixed in some degrees of freedom."""
    def __init__(self, x_pos, x=False, y=False, rot=False):
        assert x_pos >= 0 and x_pos <= 1
        self.x_pos = x_pos
        self.x = x
        self.y = y
        self.rot = rot


class Load():
    """A load to apply to the bridge."""
    def __init__(self, x_pos, weight):
        assert x_pos >= 0 and x_pos <= 1
        self.x_pos = x_pos
        self.weight = weight


class Material(Enum):
    Concrete = 1
    Steel = 2


class Patch():
    """A rectangular patch, used to describe a Section."""
    next_id = 1
    def __init__(self, y_i, z_i, y_j, z_j, num_sub_div_z=30,
                 material=Material.Concrete):
        self.id = Patch.next_id
        Patch.next_id += 1
        self.p0 = Point(y=y_i, z=z_i)
        self.p1 = Point(y=y_j, z=z_j)
        self.num_sub_div_z = num_sub_div_z
        self.material = material


class Layer():
    """A straight line of fibers, used to describe a Section.

    Args:
        y_i, z_i: float, y and z-coordinates of first fiber in line.
        y_j, z_j: float, y and z-coordinates of last fiber in line.
        num_fibers: int, number of fibers along line.
        area_fiber: float, area of each fiber.
        material: Material, material of the fibers.
    """
    def __init__(self, y_i, z_i, y_j, z_j, num_fibers, area_fiber,
                 material=Material.Steel):
        self.p0 = Point(y=y_i, z=z_i)
        self.p1 = Point(y=y_j, z=z_j)
        self.num_fibers = num_fibers
        self.area_fiber = area_fiber
        self.material = material


class Point():
    """A point described as (x, y, z)."""
    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z


class Section():
    """A section composed of fibers."""
    next_id = 1
    def __init__(self, patches=[], layers=[]):
        self.id = Section.next_id
        Section.next_id += 1
        self.patches = patches
        self.layers = layers
