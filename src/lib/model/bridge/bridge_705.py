"""Specification and Config for bridge 705 in Amsterdam."""
import os
from copy import deepcopy
from typing import Callable, List, Optional

import findup
import numpy as np

from bridge_sim.model import (
    Config,
    Dimensions,
    Lane,
    Material,
    MaterialSupport,
    Bridge,
    Support,
)
from lib.fem.run.opensees import os_runner
from util import round_m


__dir__ = os.path.dirname(findup.glob(".git"))


#################################
##### Length, width & lanes #####
#################################


bridge_705_length = 102.75
bridge_705_width = 33.2
half_width = bridge_705_width / 2
bridge_705_lanes = [
    Lane(z0=4 - half_width, z1=12.4 - half_width, ltr=True),
    Lane(z0=20.8 - half_width, z1=29.2 - half_width, ltr=False),
]


#######################
##### 2D supports #####
#######################


# Pier locations in meters (includes bridge beginning and end).
bridge_705_piers = [0]
bridge_705_spans = [13.125, 15.3, 15.3, 15.3, 15.3, 15.3, 13.125]
for _span_distance in bridge_705_spans:
    bridge_705_piers.append(bridge_705_piers[-1] + _span_distance)


############################
##### 3D deck sections #####
############################


def bridge_705_deck_sections():
    with open(os.path.join(__dir__, "data/bridge705/bridge-705.org")) as f:
        values = list(
            map(lambda l: list(map(float, l.split("|")[1:-1])), f.readlines()[2:],)
        )
    # A list of each deck section, with incorrect 'end_z_frac'.
    _deck_sections = [
        Material(
            density=density * 1e6,
            thickness=thickness / 1000,
            youngs=youngs,
            poissons=0.2,
            start_x_frac=0,
            start_z_frac=(position / 1000) / bridge_705_width,
            end_x_frac=1,
            end_z_frac=1,
        )
        for position, density, thickness, youngs in values
    ]
    # Update 'end_z_frac'.
    for i in range(len(_deck_sections) - 1):
        _deck_sections[i].end_z_frac = _deck_sections[i + 1].start_z_frac
    return _deck_sections


############################
##### 3D pier sections #####
############################

pier_thickness_top, pier_thickness_bottom = 1.266, 0.362

# Function to generate material properties from fraction of pier length.
pier_section_f = lambda start_frac_len: MaterialSupport(
    density=2.724,
    thickness=round_m(
        np.interp(start_frac_len, [0, 1], [pier_thickness_bottom, pier_thickness_top])
    ),
    youngs=38400,
    poissons=0.2,
    start_frac_len=start_frac_len,
)


##################################
##### single section variant #####
##################################


def bridge_705_single_sections():
    result = (
        deepcopy(bridge_705_deck_sections()[len(bridge_705_deck_sections()) // 2]),
        deepcopy(pier_section_f(0.5)),
    )
    for section in result:
        section.start_x_frac = 0
        section.start_z_frac = 0
        section.start_frac_len = 0
    return result


#######################
##### 3D supports #####
#######################


bridge_705_supports_z = [2.167 + 3.666 / 2]  # To first support + half support.
# For remaining supports add space between support and support width.
for _ in range(3):
    bridge_705_supports_z.append(bridge_705_supports_z[-1] + 4.734 + 3.666)
bridge_705_supports_z = list(map(lambda x: x - half_width, bridge_705_supports_z))
# Ignoring beginning and end of bridge.
bridge_705_supports_3d = []
for x_index, _support_x in enumerate(bridge_705_piers[1:-1]):
    # The x_index goes from 0 to 5.
    # Only indices 2 and 3 (middle 2 rows) have x translation fixed.
    # print(f"*******************")
    # print(f"x_index = {x_index}")
    for z_index, _support_z in enumerate(bridge_705_supports_z):
        bridge_705_supports_3d.append(
            Support(
                x=_support_x,
                z=_support_z,
                length=3.1,
                height=3.5,
                width_top=3.666,
                width_bottom=1.8,
                materials=pier_section_f,
                # sections=bridge_705_pier_sections,
                fix_x_translation=(x_index in [2, 3]),
                fix_y_translation=True,
                fix_z_translation=True,
                # fix_z_translation=z_index == 0,
                # fix_z_translation=z_index == (len(bridge_705_supports_z) // 2),
                fix_x_rotation=False,
                fix_y_rotation=False,
                fix_z_rotation=False,
            )
        )


def bridge_705_3d(
    name: str = "bridge-705",
    accuracy: str = "full",
    length: float = bridge_705_length,
    width: float = bridge_705_width,
    lanes: List[Lane] = bridge_705_lanes,
    sections: Optional[List[Material]] = None,
    supports: List[Support] = bridge_705_supports_3d,
    base_mesh_deck_max_x: int = 0.5,
    base_mesh_deck_max_z: int = 0.5,
    base_mesh_pier_max_long: int = 0.5,
    **kwargs,
) -> Bridge:
    """A constructor for a 3D model of bridge 705 in Amsterdam.

    The arguments have default values that come from a Diana model, but allow
    for being overridden if you want to change the mesh density or number of
    piers etc.. For documentation of the arguments see the 'Bridge' class.

    """
    if sections is None:
        sections = bridge_705_deck_sections()
    return Bridge(
        name=name,
        data_id=accuracy,
        length=length,
        width=width,
        lanes=lanes,
        supports=supports,
        materials=sections,
        base_mesh_deck_max_x=base_mesh_deck_max_x,
        base_mesh_deck_max_z=base_mesh_deck_max_z,
        base_mesh_pier_max_long=base_mesh_pier_max_long,
        **kwargs,
    )


# Configs for bridge 705.


def bridge_705_low_config(bridge: Callable[..., Bridge]) -> Config:
    """A low accuracy 'Config' for bridge 705 in Amsterdam."""
    c = bridge_705_config(
        bridge=lambda: bridge(
            name="Bridge 705",
            accuracy="low",
            base_mesh_deck_max_x=10,
            base_mesh_deck_max_z=10,
            base_mesh_pier_max_long=3,
        )
    )
    return c


def bridge_705_med_config(bridge: Callable[..., Bridge]) -> Config:
    """A less accurate 'Config' for bridge 705 in Amsterdam."""
    return bridge_705_config(
        bridge=lambda: bridge(
            name="Bridge 705",
            accuracy="med",
            base_mesh_deck_max_x=1.5,
            base_mesh_deck_max_z=1.5,
            base_mesh_pier_max_long=0.5,
        )
    )


def bridge_705_config(bridge: Callable[..., Bridge]) -> Config:
    """A 'Config' for (bridge 705 in Amsterdam."""
    return Config(
        bridge=bridge,
        vehicle_data_path=os.path.join(__dir__, "data/traffic/traffic.csv"),
        vehicle_pdf=[
            (2.4, 5),
            (5.6, 45),
            (7.5, 30),
            (9, 15),
            (11.5, 4),
            (12.2, 0.5),
            (43, 0),
        ],
        vehicle_pdf_col="length",
        fem_runner=os_runner,
    )
