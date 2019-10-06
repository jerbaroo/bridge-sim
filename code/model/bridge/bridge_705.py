"""Specification and Config for bridge 705 in Amsterdam."""
from typing import Callable, List, Optional

from config import Config
from model.bridge import Bridge, Dimensions, Fix, Lane, Layer, Patch, Section, Section2D, Section3D, Support, Support3D


#################################
##### Length, width & lanes #####
#################################


bridge_705_length = 102.75
bridge_705_width = 33.2
half_width = bridge_705_width / 2
bridge_705_lanes = [
    Lane(4 - half_width, 12.4 - half_width),
    Lane(20.8 - half_width, 29.2 - half_width)]


#######################
##### 2D supports #####
#######################


# Pier locations in meters (includes bridge beginning and end).
bridge_705_piers = [0]
bridge_705_spans = [13.125, 15.3, 15.3, 15.3, 15.3, 15.3, 13.125]
for _span_distance in bridge_705_spans:
    bridge_705_piers.append(bridge_705_piers[-1] + _span_distance)
print(bridge_705_spans)
for _i in range(len(bridge_705_spans)):
    print(sum(bridge_705_spans[:_i + 1]))
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
        supports: List[Fix] = bridge_705_supports_2d) -> Bridge:
    """A 2D model of bridge 705 in Amsterdam."""
    if sections is None:
        sections = [Section2D(patches=patches, layers=layers)]
    return Bridge(
        name=name, length=length, width=width, lanes=lanes, supports=supports,
        sections=sections, dimensions=Dimensions.D2)


############################
##### 3D deck sections #####
############################


bridge_705_sections_3d = [
    Section3D(density=2.724E-03, thickness=0.75,  youngs=38400, poissons=0.2, start_x_frac=0),
    Section3D(density=2.724E-03, thickness=0.74,  youngs=38400, poissons=0.2, start_x_frac=0.6    / c.bridge.length),
    Section3D(density=2.637E-03, thickness=0.655, youngs=38400, poissons=0.2, start_x_frac=0.601  / c.bridge.length),
    Section3D(density=2.664E-03, thickness=0.589, youngs=38400, poissons=0.2, start_x_frac=3.65   / c.bridge.length),
    Section3D(density=3.143E-03, thickness=0.5,   youngs=38400, poissons=0.2, start_x_frac=3.651  / c.bridge.length),
    Section3D(density=3.124E-03, thickness=0.5,   youngs=38400, poissons=0.2, start_x_frac=3.85   / c.bridge.length),
    Section3D(density=2.845E-03, thickness=0.5,   youngs=41291, poissons=0.2, start_x_frac=3.851  / c.bridge.length),
    Section3D(density=2.765E-03, thickness=0.65,  youngs=41291, poissons=0.2, start_x_frac=11.1   / c.bridge.length),
    Section3D(density=2.980E-03, thickness=0.65,  youngs=38400, poissons=0.2, start_x_frac=11.101 / c.bridge.length),
    Section3D(density=2.995E-03, thickness=0.65,  youngs=38400, poissons=0.2, start_x_frac=11.3   / c.bridge.length),
    Section3D(density=2.631E-03, thickness=0.739, youngs=38400, poissons=0.2, start_x_frac=11.301 / c.bridge.length),
    Section3D(density=2.617E-03, thickness=0.787, youngs=38400, poissons=0.2, start_x_frac=13.71  / c.bridge.length),
    Section3D(density=2.907E-03, thickness=0.65,  youngs=47277, poissons=0.2, start_x_frac=13.711 / c.bridge.length),
    Section3D(density=2.907E-03, thickness=0.65,  youngs=47277, poissons=0.2, start_x_frac=19.489 / c.bridge.length),
    Section3D(density=2.617E-03, thickness=0.787, youngs=38400, poissons=0.2, start_x_frac=19.49  / c.bridge.length),
    Section3D(density=2.631E-03, thickness=0.739, youngs=38400, poissons=0.2, start_x_frac=21.899 / c.bridge.length),
    Section3D(density=2.995E-03, thickness=0.65,  youngs=38400, poissons=0.2, start_x_frac=21.9   / c.bridge.length),
    Section3D(density=2.980E-03, thickness=0.65,  youngs=38400, poissons=0.2, start_x_frac=22.099 / c.bridge.length),
    Section3D(density=2.765E-03, thickness=0.65,  youngs=41291, poissons=0.2, start_x_frac=22.1   / c.bridge.length),
    Section3D(density=2.845E-03, thickness=0.65,  youngs=41291, poissons=0.2, start_x_frac=29.349 / c.bridge.length),
    Section3D(density=3.124E-03, thickness=0.5,   youngs=38400, poissons=0.2, start_x_frac=29.35  / c.bridge.length),
    Section3D(density=3.143E-03, thickness=0.5,   youngs=38400, poissons=0.2, start_x_frac=29.549 / c.bridge.length),
    Section3D(density=2.664E-03, thickness=0.589, youngs=38400, poissons=0.2, start_x_frac=29.55  / c.bridge.length),
    Section3D(density=2.637E-03, thickness=0.655, youngs=38400, poissons=0.2, start_x_frac=32.599 / c.bridge.length),
    Section3D(density=2.724E-03, thickness=0.74,  youngs=38400, poissons=0.2, start_x_frac=32.6   / c.bridge.length),
    Section3D(density=2.724E-03, thickness=0.75,  youngs=38400, poissons=0.2, start_x_frac=33.2   / c.bridge.length),
    ]


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
            fix_x_rotation=True, fix_y_rotation=True, fix_z_rotation=False,
            fix_x_translation=(x_index in [2, 3])))


def bridge_705_3d(
        name: str = "Bridge 705", length: float = bridge_705_length,
        width: float = bridge_705_width, lanes: List[Lane] = bridge_705_lanes,
        sections: Optional[List[Section3D]] = bridge_705_sections_3d,
        supports: List[Support3D] = bridge_705_supports_3d) -> Bridge:
    """A 3D model of bridge 705 in Amsterdam."""
    return Bridge(
        name=name, length=length, width=width, lanes=lanes, supports=supports,
        sections=sections, dimensions=Dimensions.D3)


# Configs (normal and testing) for bridge 705.


def bridge_705_test_config(bridge: Callable[[], Bridge]) -> Config:
    """A testing Config for bridge 705 in Amsterdam."""
    c = bridge_705_config(bridge=bridge, generated_dir="generated-data-test")
    c.event_metadata_path += ".test"
    c.os_node_step = c.bridge.length / 100
    c.os_node_step_z = c.bridge.width / 30
    c.os_support_num_nodes_z = 4
    c.os_support_num_nodes_y = 4
    return c


def bridge_705_config(
        bridge: Callable[[], Bridge], generated_dir: str = "generated-data",
        max_shell_area: Optional[float]=None) -> Config:
    """A Config for bridge 705 in Amsterdam."""
    return Config(
        bridge=bridge, vehicle_data_path="data/a16-data/a16.csv",
        vehicle_density=[(11.5, 5.9), (12.2, 0.3), (43, 0.1)],
        # (2.4, 0.7), (5.6, 90.1), (11.5, 5.9), (12.2, 0.3), (43, 0.1)],
        vehicle_density_col="length", vehicle_intensity=None,
        generated_dir=generated_dir, max_shell_area=max_shell_area)
