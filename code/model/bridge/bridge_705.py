"""Bridge and Config for bridge 705 in Amsterdam."""
from typing import List, Optional

from config import Config
from model.bridge import Bridge, Fix, Lane, Layer, Patch, Section


def bridge_705_config(
        name: str = "Bridge 705",
        length: Optional[float] = None,
        lanes: Optional[List[Lane]] = None,
        piers: Optional[List[float]] = None,
        patches: Optional[List[Patch]] = None,
        layers: Optional[List[Layer]] = None) -> Config:
    return Config(
        lambda: bridge_705(
            name=name, length=length, lanes=lanes, piers=piers,
            patches=patches, layers=layers),
        vehicle_data_path="data/a16-data/a16.csv",
        vehicle_density=[
            # (2.4, 0.7), (5.6, 90.1), (11.5, 5.9), (12.2, 0.3), (43, 0.1)],
            (11.5, 5.9), (12.2, 0.3), (43, 0.1)],
        vehicle_density_col="length",
        vehicle_intensity=None)


# TODO: Make into a reusable function.
def bridge_705(
        name: str = "Bridge 705",
        length: Optional[float] = None,
        lanes: Optional[List[Lane]] = None,
        piers: Optional[List[float]] = None,
        patches: Optional[List[Patch]] = None,
        layers: Optional[List[Layer]] = None) -> Bridge:

    if length == None:
        length = 102

    if lanes == None:
        lanes=[Lane(4, 12.4), Lane(20.8, 29.2)]

    if piers == None:
        piers = [0]  # Pier locations in meters.
        for span_distance in [12.75, 15.3, 15.3, 15.3, 15.3, 15.3, 12.75]:
            piers.append(piers[-1] + span_distance)

    fixed_nodes = [Fix(x / length, y=True) for x in piers]
    fixed_nodes[0].x = True

    if patches == None:
        patches = [
            Patch(y_min=-1, y_max=0, z_min=-16.6, z_max=16.6),
            Patch(y_min=-10, y_max=-1, z_min=-5, z_max=5)]

    if layers == None:
        layers = [
            Layer(
                y_min=-0.4, y_max=-0.4, z_min=-15, z_max=15,
                num_fibers=20, area_fiber=4.9e-4),
            Layer(
                y_min=-8, y_max=-8, z_min=-4.5, z_max=4.5,
                num_fibers=10, area_fiber=4.9e-4),
            Layer(
                y_min=-9, y_max=-9, z_min=-4.5, z_max=4.5,
                num_fibers=10, area_fiber=4.9e-4)]

    return Bridge(
        name=name,
        length=length,
        lanes=lanes,
        fixed_nodes=fixed_nodes,
        sections=[Section(patches=patches, layers=layers)])
