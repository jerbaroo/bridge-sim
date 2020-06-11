"""The bridge 705 in Amsterdam."""

import os
from copy import deepcopy

import numpy as np

from bridge_sim.model import Lane, Material, MaterialSupport, Support, Bridge
from bridge_sim.util import project_dir, round_m

#########################
# Length, width & lanes #
#########################

bridge_705_length = 102.75
bridge_705_width = 33.2
half_width = bridge_705_width / 2
bridge_705_lanes = [
    Lane(z0=4 - half_width, z1=12.4 - half_width, ltr=True),
    Lane(z0=20.8 - half_width, z1=29.2 - half_width, ltr=False),
]

############
# Supports #
############

# Pier locations in meters (includes bridge beginning and end).
bridge_705_piers = [0.0]
bridge_705_spans = [13.125, 15.3, 15.3, 15.3, 15.3, 15.3, 13.125]
for _span_distance in bridge_705_spans:
    bridge_705_piers.append(bridge_705_piers[-1] + _span_distance)

##################
# deck materials #
##################


def _bridge_705_deck_sections():
    with open(os.path.join(project_dir(), "data/bridge705/bridge-705.org")) as f:
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


##################
# Pier materials #
##################

pier_thickness_top, pier_thickness_bottom = 1.266, 0.362


def _pier_section_f(start_frac_len: float) -> MaterialSupport:
    """Material properties from fraction of pier length."""
    return MaterialSupport(
        density=2.724,
        thickness=round_m(
            np.interp(
                start_frac_len, [0, 1], [pier_thickness_bottom, pier_thickness_top]
            )
        ),
        youngs=38400,
        poissons=0.2,
        start_frac_len=start_frac_len,
    )


########################
# Two material variant #
########################


def _bridge_705_single_sections():
    result = (
        deepcopy(_bridge_705_deck_sections()[len(_bridge_705_deck_sections()) // 2]),
        deepcopy(_pier_section_f(0.5)),
    )
    for section in result:
        section.start_x_frac = 0
        section.start_z_frac = 0
        section.start_frac_len = 0
    return result


############
# Supports #
############

bridge_705_supports_z = [2.167 + 3.666 / 2]  # To first support + half support.
# For remaining supports add space between support and support width.
for _ in range(3):
    bridge_705_supports_z.append(bridge_705_supports_z[-1] + 4.734 + 3.666)
bridge_705_supports_z = list(map(lambda x: x - half_width, bridge_705_supports_z))
# Ignoring beginning and end of bridge.
bridge_705_supports_3d = []
for x_index, _support_x in enumerate(bridge_705_piers[1:-1]):
    for z_index, _support_z in enumerate(bridge_705_supports_z):
        bridge_705_supports_3d.append(
            Support(
                x=_support_x,
                z=_support_z,
                length=3.1,
                height=3.5,
                width_top=3.666,
                width_bottom=1.8,
                materials=_pier_section_f,
                fix_x_translation=(x_index in [2, 3]),
                fix_y_translation=True,
                fix_z_translation=True,
                fix_x_rotation=False,
                fix_y_rotation=False,
                fix_z_rotation=False,
            )
        )


def bridge_705(msl: float, single_sections: bool = False):
    """The bridge 705 in Amsterdam.

    Args:
        msl: maximum shell length.

    """
    return lambda: Bridge(
        name="bridge-705",
        length=bridge_705_length,
        width=bridge_705_width,
        supports=bridge_705_supports_3d,
        materials=_bridge_705_deck_sections(),
        lanes=bridge_705_lanes,
        msl=msl,
        single_sections=_bridge_705_single_sections() if single_sections else None,
    )
