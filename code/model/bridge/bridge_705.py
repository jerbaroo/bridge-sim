"""Specification and Config for bridge 705 in Amsterdam."""
from typing import Callable, List, Optional

from config import Config
from model.bridge import Bridge, Dimensions, Fix, Lane, Layer, Patch, Section, Section2D, Section3D, Support, Support3D

# Values and a constructor for a 2D model of bridge 705.

bridge_705_length = 102.75
bridge_705_width = 33.2
bridge_705_lanes = [Lane(4, 12.4), Lane(20.8, 29.2)]
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


# Values and a constructor for a 3D model of bridge 705.


bridge_705_sections_3d = [
    Section3D(density=2.724E-03, thickness=0.75, youngs=38400, poissons=0.2)]
bridge_705_supports_z = [2.167 + 3.666/2]  # To first support + half support.
# For remaining supports add space between support and support width.
for _ in range(3):
    bridge_705_supports_z.append(bridge_705_supports_z[-1] + 4.734 + 3.666)
# Ignoring beginning and end of bridge.
bridge_705_supports_3d = []
for _support_x in bridge_705_piers[1:-1]:
    for _support_z in bridge_705_supports_z:
        bridge_705_supports_3d.append(Support3D(
            x=_support_x, z=_support_z, length=3.1, height=3.5,
            width_top=3.666, width_bottom=1.8))


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
    c.os_node_step = c.bridge.length / 5
    c.os_node_step_z = c.bridge.width / 5
    c.os_support_num_nodes_z = 3
    return c


def bridge_705_config(
        bridge: Callable[[], Bridge], generated_dir: str = "generated-data"
        ) -> Config:
    """A Config for bridge 705 in Amsterdam."""
    return Config(
        bridge=bridge, vehicle_data_path="data/a16-data/a16.csv",
        vehicle_density=[(11.5, 5.9), (12.2, 0.3), (43, 0.1)],
        # (2.4, 0.7), (5.6, 90.1), (11.5, 5.9), (12.2, 0.3), (43, 0.1)],
        vehicle_density_col="length", vehicle_intensity=None,
        generated_dir=generated_dir)
