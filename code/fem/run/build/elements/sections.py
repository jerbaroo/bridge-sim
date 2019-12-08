"""Sections for elements."""
from collections import defaultdict

from config import Config
from model.bridge import Section3D, Support3D
from util import round_m


# Sections indexed by strings that uniquely represent their values.
sections_by_value = dict()


def get_section(section: Section3D) -> Section3D:
    """An equivalent previously created Section if possible."""
    id_str = section.id_str()
    print(id_str)
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

    # Create the dictionary if not already created.
    if not hasattr(c.bridge, "deck_sections_dict"):
        c.bridge.deck_sections_dict = defaultdict(dict)
        for section in c.bridge.sections:
            c.bridge.deck_sections_dict[
                round_m(c.bridge.x(section.start_x_frac))
            ][round_m(c.bridge.z(section.start_z_frac))] = section

    # print(sorted(c.bridge.deck_sections_dict.keys()))
    # print(sorted(c.bridge.deck_sections_dict[0.0].keys()))

    element_x, element_z = round_m(element_x), round_m(element_z)
    # Find the last x position less than element_x.
    section_x = None
    for next_section_x in sorted(c.bridge.deck_sections_dict.keys()):
        if next_section_x <= element_x:
            section_x = next_section_x
        else:
            break
    # print(f"section_x = {section_x}")

    # Find the last z position less than element_z.
    section_z = None
    for next_section_z in sorted(c.bridge.deck_sections_dict[section_x].keys()):
        if next_section_z <= element_z:
            section_z = next_section_z
        else:
            break
        # print(f"next_section_z = {next_section_z}")
    # print(f"section_z = {section_z}")

    return get_section(c.bridge.deck_sections_dict[section_x][section_z])


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
