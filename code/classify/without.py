import numpy as np
from numpy import arccos, dot, pi, cross
from numpy.linalg import det, norm

from config import Config
from model.bridge import Point


# from: https://gist.github.com/nim65s/5e9902cd67f094ce65b0
def _distance_numpy(A, B, P):
    """ segment line AB, point P, where each one is an array([x, y]) """
    if all(A == P) or all(B == P):
        return 0
    if arccos(dot((P - A) / norm(P - A), (B - A) / norm(B - A))) > pi / 2:
        return norm(P - A)
    if arccos(dot((P - B) / norm(P - B), (A - B) / norm(A - B))) > pi / 2:
        return norm(P - B)
    return norm(cross(A-B, A-P))/norm(B-A)


def without_pier_lines(c: Config, radius: float):
    """Points without any around pier lines.

    This function only applies to sensors on the bridge deck.

    """
    def _without_pier_lines(point: Point) -> bool:
        if point.y != 0 or radius == 0:
            return False
        p3 = np.array([point.x, point.z])
        for pier in c.bridge.supports:
            z_min, z_max = pier.z_min_max_top()
            for pier_x in pier.x_min_max_top():
                p1 = np.array([pier_x, z_min])
                p2 = np.array([pier_x, z_max])
                # dist = abs(np.cross(p2 - p1, p1 - p3) / np.linalg.norm(p2 - p1))
                dist = _distance_numpy(p1, p2, p3)
                # print(f"distance {dist} in without_pier_lines = {dist}")
                # print(f"from point {p3} to {p1} - {p2}")
                # print(f"radius = {radius}")
                if dist <= radius:
                    return True
        return False
    return _without_pier_lines


def without_wheel_tracks(c: Config, radius: float):
    """Points without any around wheel tracks.

    This function only applies to sensors on the bridge deck.

    """
    wheel_track_zs = c.bridge.wheel_tracks(c)
    def _without_pier_lines(point: Point) -> bool:
        if point.y != 0 or radius == 0:
            return False
        p3 = np.array([point.x, point.z])
        for wheel_track_z in wheel_track_zs:
            p1 = np.array([c.bridge.x_min, wheel_track_z])
            p2 = np.array([c.bridge.x_max, wheel_track_z])
            dist = _distance_numpy(p1, p2, p3)
            if dist <= radius:
                return True
                # p2 = np.array([pier_x, z_max])
                # dist = abs(np.cross(p2 - p1, p1 - p3) / np.linalg.norm(p2 - p1))
                # print(f"distance {dist} in without_pier_lines = {dist}")
                # print(f"from point {p3} to {p1} - {p2}")
                # print(f"radius = {radius}")
        return False
    return _without_pier_lines
