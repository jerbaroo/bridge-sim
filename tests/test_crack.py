from bridge_sim import crack
from bridge_sim.configs import test_config


def test_crack():
    config, _ = test_config(msl=10)
    x, length = config.bridge.x_center, 2
    transverse_crack = crack.transverse_crack(length=length, at_x=x)
    crack_zone = transverse_crack.crack_zone(config.bridge)
    assert crack_zone.x_min == x
    assert crack_zone.x_max == x + length
    cracked_config = transverse_crack.crack(config)
    z = (crack_zone.z_min + crack_zone.z_max) / 2
    # Center of crack zone.
    x_center = (crack_zone.x_min + crack_zone.x_max) / 2
    crack_material = cracked_config.bridge.deck_section_at(x=x_center, z=z)
    uncracked_material = config.bridge.deck_section_at(x=x_center, z=z)
    assert crack_material.youngs_x() != uncracked_material.youngs_x()
    assert crack_material.youngs == uncracked_material.youngs
    assert crack_material.poissons == uncracked_material.poissons
    # Left of crack zone.
    x_left = x - 0.1
    crack_material = cracked_config.bridge.deck_section_at(x=x_left, z=z)
    uncracked_material = config.bridge.deck_section_at(x=x_left, z=z)
    assert crack_material.youngs_x() == uncracked_material.youngs_x()
    assert crack_material.youngs == uncracked_material.youngs
    assert crack_material.poissons == uncracked_material.poissons
    # Right of crack zone.
    x_right = x + length + 0.1
    crack_material = cracked_config.bridge.deck_section_at(x=x_right, z=z)
    uncracked_material = config.bridge.deck_section_at(x=x_right, z=z)
    assert crack_material.youngs_x() == uncracked_material.youngs_x()
    assert crack_material.youngs == uncracked_material.youngs
    assert crack_material.poissons == uncracked_material.poissons
