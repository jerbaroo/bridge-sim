"""Specification and Config for bridge 705 in Amsterdam."""
from copy import deepcopy
from typing import Callable, List, Optional, Tuple

import numpy as np

from config import Config
from model.bridge import Bridge, Dimensions, Fix, Lane, Layer, Patch, Section,\
    Section2D, Section3D, Section3DPier, Support, Support3D


#################################
##### Length, width & lanes #####
#################################


bridge_705_length = 102.75
bridge_705_width = 33.2
half_width = bridge_705_width / 2
bridge_705_lanes = [
    Lane(z0=4 - half_width, z1=12.4 - half_width, ltr=True),
    Lane(z0=20.8 - half_width, z1=29.2 - half_width, ltr=False)]


#######################
##### 2D supports #####
#######################


# Pier locations in meters (includes bridge beginning and end).
bridge_705_piers = [0]
bridge_705_spans = [13.125, 15.3, 15.3, 15.3, 15.3, 15.3, 13.125]
for _span_distance in bridge_705_spans:
    bridge_705_piers.append(bridge_705_piers[-1] + _span_distance)
# for _i in range(len(bridge_705_spans)):
#     print(sum(bridge_705_spans[:_i + 1]))
bridge_705_supports_2d = [
    Fix(x / bridge_705_length, y=True) for x in bridge_705_piers]
bridge_705_supports_2d[0].x = True


############################
##### Patches & Layers #####
############################


# NOTE: These patches and layers are incorrect!
bridge_705_patches = [
    Patch(y_min=-1, y_max=0, z_min=-16.6, z_max=16.6),
    Patch(y_min=-10, y_max=-1, z_min=-5, z_max=5)]
bridge_705_layers = [
    Layer(
        y_min=-0.4, y_max=-0.4, z_min=-15, z_max=15, num_fibers=20,
        area_fiber=4.9e-4),
    Layer(
        y_min=-8, y_max=-8, z_min=-4.5, z_max=4.5, num_fibers=10,
        area_fiber=4.9e-4),
    Layer(
        y_min=-9, y_max=-9, z_min=-4.5, z_max=4.5, num_fibers=10,
        area_fiber=4.9e-4)]


def bridge_705_2d(
        name: str = "Bridge 705", length: float = bridge_705_length,
        width: float = bridge_705_width, lanes: List[Lane] = bridge_705_lanes,
        piers: List[float] = bridge_705_piers,
        layers: List[Layer] = bridge_705_layers,
        patches: List[Patch] = bridge_705_patches,
        sections: Optional[List[Section2D]] = None,
        supports: List[Fix] = bridge_705_supports_2d,
        base_mesh_deck_nodes_x: int = 412, base_mesh_deck_nodes_z: int = None,
        base_mesh_pier_nodes_y: int = None, base_mesh_pier_nodes_z: int = None,
        ) -> Bridge:
    """A 2D model of bridge 705 in Amsterdam."""
    if sections is None:
        sections = [Section2D(patches=patches, layers=layers)]
    return Bridge(
        name=name, length=length, width=width, lanes=lanes, supports=supports,
        sections=sections, dimensions=Dimensions.D2,
        base_mesh_deck_nodes_x=base_mesh_deck_nodes_x)


############################
##### 3D deck sections #####
############################


def load_bridge_705_deck_sections():
    with open("bridge705/bridge_705_mod.org") as f:
        values = list(map(
            lambda l: list(map(float, l.split("|")[1:-1])),
            f.readlines()[2:]))
    return [Section3D(
            start_z_frac=(position / 1000) / bridge_705_width,
            density=density * 1E6,
            thickness=thickness / 1000,
            youngs=youngs,
            poissons=0.2)
        for position, density, thickness, youngs in values]

bridge_705_sections_3d = load_bridge_705_deck_sections()


############################
##### 3D pier sections #####
############################


pier_thickness_top, pier_thickness_bottom = 1.266, 0.362
num_pier_sections = 20
bridge_705_pier_sections = [
    Section3DPier(
        density=2.724, thickness=np.interp(
            start_frac_len, [0, 1],
            [pier_thickness_top, pier_thickness_bottom]),
        youngs=38400, poissons=0.2, start_frac_len=start_frac_len)
    for start_frac_len in np.linspace(0, 1, num_pier_sections)]

assert np.isclose(bridge_705_pier_sections[0].thickness, pier_thickness_top)
assert np.isclose(bridge_705_pier_sections[-1].thickness, pier_thickness_bottom)


##################################
##### single section variant #####
##################################


bridge_705_single_sections = (
    deepcopy(bridge_705_sections_3d[len(bridge_705_sections_3d) // 2]),
    deepcopy(bridge_705_pier_sections[len(bridge_705_pier_sections) // 2]))
for section in bridge_705_single_sections:
    section.start_x_frac = 0
    section.start_z_frac = 0
    section.start_frac_len = 0


#######################
##### 3D supports #####
#######################


bridge_705_supports_z = [2.167 + 3.666/2]  # To first support + half support.
# For remaining supports add space between support and support width.
for _ in range(3):
    bridge_705_supports_z.append(bridge_705_supports_z[-1] + 4.734 + 3.666)
bridge_705_supports_z = list(map(
    lambda x: x - half_width, bridge_705_supports_z))
# Ignoring beginning and end of bridge.
bridge_705_supports_3d = []
for x_index, _support_x in enumerate(bridge_705_piers[1:-1]):
    # The x_index goes from 0 to 5.
    # Only indices 2 and 3 (middle 2 rows) have x translation fixed.
    # print(f"*******************")
    # print(f"x_index = {x_index}")
    for _support_z in bridge_705_supports_z:
        bridge_705_supports_3d.append(Support3D(
            x=_support_x, z=_support_z, length=3.1, height=3.5,
            width_top=3.666, width_bottom=1.8,
            sections=bridge_705_pier_sections, fix_x_rotation=True,
            fix_y_rotation=True, fix_z_rotation=False,
            fix_x_translation=(x_index in [2, 3])))


def bridge_705_3d(
        name: str = "bridge-705", length: float = bridge_705_length,
        width: float = bridge_705_width, lanes: List[Lane] = bridge_705_lanes,
        sections: Optional[List[Section3D]] = bridge_705_sections_3d,
        supports: List[Support3D] = bridge_705_supports_3d,
        base_mesh_deck_nodes_x: int = 412, base_mesh_deck_nodes_z: int = 133,
        base_mesh_pier_nodes_y: int = 17, base_mesh_pier_nodes_z: int = 16,
        single_sections: Optional[Tuple[Section, Section]] = None) -> Bridge:
    """A constructor for a 3D model of bridge 705 in Amsterdam.

    The arguments have default values that come from a Diana model, but allow
    for being overridden if you want to change the mesh density or number of
    piers etc.. For documentation of the arguments see the 'Bridge' class.

    """
    return Bridge(
        name=name, length=length, width=width, lanes=lanes, supports=supports,
        sections=sections, dimensions=Dimensions.D3,
        base_mesh_deck_nodes_x=base_mesh_deck_nodes_x,
        base_mesh_deck_nodes_z=base_mesh_deck_nodes_z,
        base_mesh_pier_nodes_y=base_mesh_pier_nodes_y,
        base_mesh_pier_nodes_z=base_mesh_pier_nodes_z,
        single_sections=single_sections)


# Configs (normal and testing) for bridge 705.


def bridge_705_test_config(bridge: Callable[..., Bridge]) -> Config:
    """A less accurate 'Config' for bridge 705 in Amsterdam."""
    c = bridge_705_config(
        generated_dir="generated-data-test",
        bridge=lambda: bridge(
            name="Bridge 705-test",
            base_mesh_deck_nodes_x=50,
            base_mesh_deck_nodes_z=20,
            base_mesh_pier_nodes_y=5,
            base_mesh_pier_nodes_z=5)
        )
    c.event_metadata_path += ".test"
    return c


def bridge_705_debug_config(bridge: Callable[..., Bridge]) -> Config:
    """A low-as-possible accuracy 'Config' for bridge 705 in Amsterdam."""
    c = bridge_705_config(
        generated_dir="generated-data-debug",
        bridge=lambda: bridge(
            name="Bridge 705-debug",
            base_mesh_deck_nodes_x=3,
            base_mesh_deck_nodes_z=3,
            base_mesh_pier_nodes_y=3,
            base_mesh_pier_nodes_z=3)
        )
    c.event_metadata_path += ".debug"
    c.time_step = 1 / 100
    return c


def bridge_705_config(
        bridge: Callable[..., Bridge], generated_dir: str = "generated-data",
        max_shell_area: Optional[float]=None) -> Config:
    """A 'Config' for bridge 705 in Amsterdam."""
    return Config(
        bridge=bridge, vehicle_data_path="data/a16-data/a16.csv",
        vehicle_pdf=[(11.5, 5.9), (12.2, 0.3), (43, 0.1)],
        # (2.4, 0.7), (5.6, 90.1), (11.5, 5.9), (12.2, 0.3), (43, 0.1)],
        vehicle_pdf_col="length", generated_dir=generated_dir,
        max_shell_area=max_shell_area)
