"""Test config.py."""
import math

from config import Config
from model.bridge.bridge_705 import bridge_705_3d
from util import print_d

# Print debug information for this file.
D: bool = True


def test_max_shell_area():
    """Test that derived attributes are set correctly."""
    # Function from max_shell_area to a Config.
    dummy_config = lambda max_shell_area: Config(
        bridge_705_3d, "data/a16-data/a16.csv", [], 0, "length",
        max_shell_area=max_shell_area)
    # Get the default values without setting max_shell_area.
    c = dummy_config(None)
    default_node_step_x = c.os_node_step
    default_node_step_z = c.os_node_step_z
    default_support_num_nodes_z = c.os_support_num_nodes_z
    default_support_num_nodes_y = c.os_support_num_nodes_y
    # Assert max_shell_area is greater than bridge deck shell area.
    max_shell_area = 0.01  # 1 cm.
    c = dummy_config(max_shell_area)
    deck_shell_area = c.os_node_step * c.os_node_step_z
    print_d(D, f"Deck shell length = {c.os_node_step}")
    print_d(D, f"Deck shell width = {c.os_node_step_z}")
    print_d(D, f"Deck shell area = {deck_shell_area}")
    assert max_shell_area >= deck_shell_area
    # Assert one shell side is less than 2* the other side.
    # In other words that the shells are approximately square.
    min_deck_shell_dim = min(c.os_node_step, c.os_node_step_z)
    max_deck_shell_dim = max(c.os_node_step, c.os_node_step_z)
    assert max_deck_shell_dim < 2 * min_deck_shell_dim
    print_d(D, f"Deck shell length = {c.os_node_step}")
    print_d(D, f"Deck shell width = {c.os_node_step_z}")
    print_d(D, f"Deck shell area = {deck_shell_area}")
    # Assert max_shell_area is greater than support shell area.
    # TODO: This assumes supports are square, when they are not.
    #     Instead could get the maximum from the nodes directly (via d3.py).
    support = c.bridge.supports[0]
    wall_shell_length = support.height / (c.os_support_num_nodes_y + 1)
    wall_shell_width = support.width_top / (c.os_support_num_nodes_z + 1)
    wall_shell_area = wall_shell_length * wall_shell_width
    print_d(D, f"Wall shell length = {wall_shell_length}")
    print_d(D, f"Wall shell width = {wall_shell_width}")
    print_d(D, f"Wall shell area = {wall_shell_area}")
    assert max_shell_area >= wall_shell_area

