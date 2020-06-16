import numpy as np

from bridge_sim import bridges, configs
from bridge_sim.sim.build import get_bridge_shells


def test_material_and_area_and_mass():
    config, _ = configs.test_config(msl=10)
    bridge_705 = config.bridge
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
    assert np.isclose(shell.mass(config), thickness * density * length * width)


def test_asphalt_mass():
    config, _ = configs.test_config(msl=2)
    deck_shells, _ = get_bridge_shells(config.bridge)
    # Not on lane.
    shell = deck_shells[0]
    config.self_weight_asphalt = True
    mass_with_asphalt = shell.mass(config)
    config.self_weight_asphalt = False
    mass_without_asphalt = shell.mass(config)
    assert mass_with_asphalt == mass_without_asphalt
    # On lane.
    lane = config.bridge.lanes[0]
    for shell in deck_shells:
        if lane.z_min <= shell.center().z <= lane.z_max:
            config.self_weight_asphalt = True
            mass_with_asphalt = shell.mass(config)
            config.self_weight_asphalt = False
            mass_without_asphalt = shell.mass(config)
        continue
    assert mass_with_asphalt > mass_without_asphalt
