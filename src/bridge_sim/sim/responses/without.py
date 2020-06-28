"""Functions to filter simulation responses."""

import numpy as np
from numpy import arccos, dot, pi, cross
from numpy.linalg import det, norm

from bridge_sim.model import Config, Point


# from: https://gist.github.com/nim65s/5e9902cd67f094ce65b0
def _distance_numpy(A, B, P):
    """ segment line AB, point P, where each one is an array([x, y]) """
    if all(A == P) or all(B == P):
        return 0
    if arccos(dot((P - A) / norm(P - A), (B - A) / norm(B - A))) > pi / 2:
        return norm(P - A)
    if arccos(dot((P - B) / norm(P - B), (A - B) / norm(A - B))) > pi / 2:
        return norm(P - B)
    return norm(cross(A - B, A - P)) / norm(B - A)


def edges(c: Config, radius: float):
    """Reject points on the bridge deck not close to edges."""

    def _without_edges(point: Point, r_) -> bool:
        if point.y != 0 or radius == 0:
            return False
        p2 = np.array([point.x, point.z])
        for edge_z0, edge_x0, edge_z1, edge_x1 in [
            (c.bridge.z_min, c.bridge.x_min, c.bridge.z_max, c.bridge.x_min),
            (c.bridge.z_max, c.bridge.x_min, c.bridge.z_max, c.bridge.x_max),
            (c.bridge.z_max, c.bridge.x_max, c.bridge.z_min, c.bridge.x_max),
            (c.bridge.z_min, c.bridge.x_max, c.bridge.z_min, c.bridge.x_min),
        ]:
            p0 = np.array([edge_x0, edge_z0])
            p1 = np.array([edge_x1, edge_z1])
            dist = _distance_numpy(p0, p1, p2)
            if dist <= radius:
                return True
        return False

    return _without_edges


def pier_lines(c: Config, radius: float):
    """Reject points on the deck not close to pier lines."""

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


def wheel_tracks(c: Config, radius: float):
    """Reject points on the deck not close to wheel tracks."""
    wheel_track_zs = c.bridge.wheel_track_zs(c)

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


def points(c: Config, pier_radius: float, track_radius: float, edge_radius: float):
    without_p = pier_lines(c=c, radius=pier_radius)
    without_t = wheel_tracks(c=c, radius=track_radius)
    without_e = edges(c=c, radius=edge_radius)

    def _without_points(point: Point) -> bool:
        return without_t(point) or without_p(point) or without_e(point, None)

    return _without_points
