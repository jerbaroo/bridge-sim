"""Specification and Config for bridge 705 in Amsterdam."""
from typing import List, Optional

from config import Config
from model.bridge import Dimensions, Bridge, Fix, Lane, Layer, Patch, Section, Section2D, Support


def bridge_705_config(
        name: str = "Bridge 705",
        length: Optional[float] = None,
        width: Optional[float] = None,
        lanes: Optional[List[Lane]] = None,
        piers: Optional[List[float]] = None,
        sections: Optional[List[Section]] = None,
        layers: Optional[List[Layer]] = None,
        patches: Optional[List[Patch]] = None,
        supports: Optional[List[Support]] = None,
        dimensions: Dimensions = Dimensions.D2,
        generated_dir: Optional[str] = None
        ) -> Config:
    """A Config for bridge 705 in Amsterdam."""
    return Config(
        lambda: bridge_705(
            name=name, length=length, width=width, lanes=lanes, piers=piers,
            sections=sections, layers=layers, patches=patches,
            supports=supports, dimensions=dimensions),
        vehicle_data_path="data/a16-data/a16.csv",
        vehicle_density=[(11.5, 5.9), (12.2, 0.3), (43, 0.1)],
            # (2.4, 0.7), (5.6, 90.1), (11.5, 5.9), (12.2, 0.3), (43, 0.1)],
        vehicle_density_col="length",
        vehicle_intensity=None,
        generated_dir=generated_dir)


def bridge_705(
        name: str = "Bridge 705",
        length: Optional[float] = None,
        width: Optional[float] = None,
        lanes: Optional[List[Lane]] = None,
        piers: Optional[List[float]] = None,
        sections: Optional[List[Section]] = None,
        layers: Optional[List[Layer]] = None,
        patches: Optional[List[Patch]] = None,
        supports: Optional[List[Support]] = None,
        dimensions: Dimensions = Dimensions.D2) -> Bridge:
    """A specification of bridge 705 in Amsterdam."""
    # Length & width.
    if length is None:
        length = 102
    if width is None:
        width = 33.2
    # Lanes.
    if lanes is None:
        lanes = [Lane(4, 12.4), Lane(20.8, 29.2)]
    # Supports.
    if piers is None:
        piers = [0]  # Pier locations in meters.
        for span_distance in [12.75, 15.3, 15.3, 15.3, 15.3, 15.3, 12.75]:
            piers.append(piers[-1] + span_distance)
    if supports is None:
        supports = [Fix(x / length, y=True) for x in piers]
        supports[0].x = True
    # Sections.
    if sections is None:
        if dimensions == Dimensions.D2:
            if patches is None:
                patches = [
                    Patch(y_min=-1, y_max=0, z_min=-16.6, z_max=16.6),
                    Patch(y_min=-10, y_max=-1, z_min=-5, z_max=5)]
            if layers is None:
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
            sections = [Section2D(patches=patches, layers=layers)]
        else:
            raise ValueError("No default sections for 3D model")
    # Put it all together.
    return Bridge(
        name=name,
        length=length,
        width=width,
        lanes=lanes,
        supports=supports,
        sections=sections,
        dimensions=dimensions)
