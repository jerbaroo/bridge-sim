import numpy as np

from model.bridge import Bridge, Point


def without_pier_lines(bridge: Bridge, radius: float):
    """The given responses but without any around pier lines.

    This function only applies to sensors on the bridge deck.

    """
    def _without_pier_lines(point: Point) -> bool:
        if point.y != 0:
            return False
        p3 = np.array([point.x, point.z])
        for pier in bridge.supports:
            z_min, z_max = pier.z_min_max_top()
            for pier_x in pier.x_min_max_top():
                p1 = np.array([pier_x, z_min])
                p2 = np.array([pier_x, z_max])
                dist = np.cross(p2 - p1, p1 - p3) / np.linalg.norm(p2 - p1)
                # print(f"distance {dist} in without_pier_lines = {dist}")
                # print(f"from point {p3} to {p1} - {p2}")
                if dist <= radius:
                    return True
        return False
    return _without_pier_lines
