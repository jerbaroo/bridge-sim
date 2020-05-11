"""Sections for elements."""
from collections import defaultdict

import numpy as np

from config import Config
from model.bridge import Section3D, Support3D
from util import round_m


# Sections indexed by strings that uniquely represent their values.
sections_by_value = dict()


def get_section(section: Section3D) -> Section3D:
    """An equivalent previously created Section if possible."""
    id_str = section.mat_id_str()
    if id_str not in sections_by_value:
        sections_by_value[id_str] = section
    return sections_by_value[id_str]


def section_for_deck_element(
    c: Config, element_x: float, element_z: float
) -> Section3D:
    """Section for an element on the deck.

    Creates a dict (if not already created) of all section's x positions, to z
    positions, to Section3D. Then iterates through sorted x positions finding
    the last one less than or equal to the given element's lowest x position,
    then does the same for the sorted z positions, then the section is found.

    Args:
        c: Config, global configuration object.
        element_x: float, x position which belongs in some section.
        element_z: float, z position which belongs in some section.

    """
    if callable(c.bridge.sections):
        raise NotImplementedError(
            "Function to vary material properties not yet supported"
        )

    return c.bridge.deck_section_at(x=element_x, z=element_z)


def section_for_pier_element(
    c: Config, pier: Support3D, start_frac_len: float
) -> Section3D:
    """Section for a shell element on a pier.

    Args:
        c: Config, global configuration object.
        pier: Support3DPier, the pier from which to select a section.
        element_start_frac_len: float, fraction of pier wall length.

    """

    # If 'pier.sections' is a function simply defer to that..
    if callable(pier.sections):
        return get_section(pier.sections(start_frac_len))

    # ..else find the last pier section where: the fraction of the pier wall's
    # length is less than the given value 'start_frac_len'.
    section = None
    for next_section in sorted(pier.sections, key=lambda s: s.start_frac_len):
        if next_section.start_frac_len <= start_frac_len:
            section = next_section
        else:
            break
    return get_section(section)
