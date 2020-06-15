import numpy as np

from bridge_sim import bridges
from bridge_sim.sim.build import get_bridge_shells


def test_material_and_area_and_mass():
    bridge_705 = bridges.bridge_705(msl=10)()
    x, z = 0, -16.6
    material = bridge_705.deck_section_at(x=x, z=z)
    thickness = material.thickness
    density = material.density
    deck_shells, _ = get_bridge_shells(bridge_705)
    shell = deck_shells[0]
    # Assert the material and first node's positions are correct.
    assert shell.nodes()[0].x == x
    assert shell.nodes()[0].z == z
    assert shell.section == material
    # Assert area is correct.
    length, width = shell.length(), shell.width()
    assert np.isclose(shell.area(), length * width)
    # Assert mass is correct.
    assert np.isclose(shell.mass(), thickness * density * length * width)
