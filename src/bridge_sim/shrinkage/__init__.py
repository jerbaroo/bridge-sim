"""Time series of responses to shrinkage."""

from enum import Enum
from math import sqrt
from typing import List, Optional

import numpy as np
from numba import njit

from bridge_sim import sim
from bridge_sim.model import Config, Point, ResponseType
from bridge_sim.util import convert_times, print_d, print_i

D = "bridge_sim.shrinkage"


class CementClass(Enum):
    """Cement class: BS EN 1992-1-1 31.2 (6)."""

    Slow = "S"
    Normal = "N"
    Rapid = "R"


a_ds1 = {
    CementClass.Slow: 3,
    CementClass.Normal: 4,
    CementClass.Rapid: 6,
}
"""Coefficient depending on cement class."""

a_ds2 = {
    CementClass.Slow: 0.13,
    CementClass.Normal: 0.12,
    CementClass.Rapid: 0.11,
}
"""Coefficient depending on cement class."""

f_ck = 30
f_cm = f_ck + 8
f_cmo = 10
t_s = 1  # Age of concrete (days) at beginning of drying concrete.
RH_0 = 1
RH = 0.7  # Ambient relative humidity.
h_0tab = [100, 200, 300, 500]
k_htab = [1, 0.85, 0.75, 0.7]


def notational_size(config: Config, x: Optional[float] = None):
    """Notational size in mm.

    Args:
        config: simulation configuration object
        x: X position used to calculate cross-sectional area and perimeter, if
            not given use the center of the bridge.
    """
    if x is None:
        x = config.bridge.x_center
    thicknesses = []
    for z in np.linspace(config.bridge.z_min, config.bridge.z_max, 100):
        thicknesses.append(config.bridge.deck_section_at(x=x, z=z).thickness)
    A_c = config.bridge.width * np.mean(thicknesses) * 1000 * 1000
    print_i(f"Mean thickness = {np.mean(thicknesses)}")
    u = (config.bridge.width + thicknesses[0] + thicknesses[-1]) * 1000
    h_0 = (2 * A_c) / u
    print_i("Drying shrinkage calculation:")
    print_i(f"    perimeter u = {u}")
    print_i(f"    A_c = {A_c}")
    print_i(f"    h_0 = {h_0}")
    return h_0


def drying(
    config: Config,
    cement_class: CementClass,
    times: List[float],
    x: Optional[float] = None,
) -> List[float]:
    """Strain due to drying shrinkage over time.

    For the notational size the A_c component, the cross-sectional area is
    calculated at the given X position, 100 points are sampled across the width
    of the bridge at that X position.

    Args:
        config: simulation configuration object.
        cement_class: class of the cement.
        times: seconds when to compute strain.
        x: X position used to calculate cross-sectional area and perimeter, if
            not given use the center of the bridge.

    Returns: list of strain at each given time.

    """
    h_0 = notational_size(config=config, x=x)
    t = np.array(convert_times(f="second", t="day", times=times))
    B_RH = 1.55 * (1 - (RH / RH_0) ** 3)
    print_d(D, f"B_RH = {B_RH}")
    E_cd0 = (
        0.85
        * (220 + 110 * a_ds1[cement_class])
        * np.exp(-a_ds2[cement_class] * f_cm / f_cmo)
        * 1e-6
        * B_RH
    )
    print_d(D, f"E_cd0 = {E_cd0}")
    k_h = np.interp([h_0], h_0tab, k_htab)[0]
    print_d(D, f"k_h = {k_h}")

    def B_ds(t_):
        return (t_ - t_s) / ((t_ - t_s) + 0.04 * sqrt(h_0 ** 3))

    return B_ds(t) * k_h * E_cd0


def drying_responses(
    config: Config,
    response_type: ResponseType,
    times: List[float],
    points: List[Point],
    cement_class: CementClass,
    x: Optional[float] = None,
) -> List[List[float]]:
    """Responses over time at points due to drying shrinkage.

    Args:
        config: simulation configuration object.
        response_type: simulation response type.
        times: seconds when to compute responses.
        points: points where to compute responses.
        cement_class: class of the cement.
        x: X position used to calculate cross-sectional area and perimeter, if
            not given use the center of the bridge.

    Returns: NumPy array ordered by points then times.

    """
    strain = drying(config=config, cement_class=cement_class, times=times, x=x)
    temp_deltas = strain / config.cte
    unit_uniforms = sim.responses.load(  # Response to unit uniform temp delta.
        config=config, response_type=response_type, temp_deltas=(1, None)
    ).at_decks(points)
    assert len(unit_uniforms) == len(points)
    assert not any(np.isinf(u) or np.isnan(u) for u in unit_uniforms)
    result = np.empty((len(points), len(times)))

    @njit(parallel=True)
    def build_result(result_, len_points):
        for i in range(len_points):
            result_[i] = temp_deltas * unit_uniforms[i]

    build_result(result, len(points))
    return result


def autogenous(times: List[float]) -> List[float]:
    """Strain due to drying shrinkage over time.

    Args:
        times: seconds when to compute strain.

    Returns: list of strain at each given time.

    """
    t = np.array(convert_times(f="second", t="day", times=times))
    E_cainf = 2.5 * (f_ck - 10) * 1e-6
    print_d(D, f"f_ck = {f_ck}")

    def B_as(t_):
        return 1 - np.exp(-0.2 * t_ ** 0.5)

    return B_as(t) * E_cainf


def autogenous_responses(
    config: Config,
    response_type: ResponseType,
    times: List[float],
    points: List[Point],
) -> List[List[float]]:
    """Responses over time at points due to autogenous shrinkage.

    Args:
        config: simulation configuration object.
        response_type: simulation response type.
        times: seconds when to compute responses.
        points: points where to compute responses.

    Returns: NumPy array ordered by points then times.

    """
    strain = autogenous(times=times)
    temp_deltas = strain / config.cte
    unit_uniforms = sim.responses.load(  # Response to unit uniform temp delta.
        config=config, response_type=response_type, temp_deltas=(1, None)
    ).at_decks(points)
    assert len(unit_uniforms) == len(points)
    assert not any(np.isinf(u) or np.isnan(u) for u in unit_uniforms)
    result = np.empty((len(points), len(times)))

    @njit(parallel=True)
    def build_result(result_, len_points):
        for i in range(len_points):
            result_[i] = temp_deltas * unit_uniforms[i]

    build_result(result, len(points))
    return result


def total(
    config: Config, cement_class: CementClass, times: List[float], x: float,
) -> List[float]:
    """Strain due to drying and autogenous shrinkage over time.

    Args:
        cement_class: class of the cement.
        times: seconds when to compute strain.
        x: X position used to calculate cross-sectional area and perimeter.

    Returns: list of strain at each given time.

    """
    d = drying(config, cement_class=cement_class, times=times, x=x)
    a = autogenous(times)
    assert len(a) == len(d)
    result = d + a
    assert len(result) == len(d)
    assert result[-1] == d[-1] + a[-1]
    return result


def total_responses(
    config: Config,
    response_type: ResponseType,
    times: List[float],
    points: List[Point],
    cement_class: CementClass = CementClass.Normal,
    x: Optional[float] = None,
) -> List[List[float]]:
    """Responses over time at points due to drying shrinkage.

    Args:
        config: simulation configuration object.
        response_type: simulation response type.
        times: seconds when to compute responses.
        points: points where to compute responses.
        cement_class: class of the cement.
        x: X position used to calculate cross-sectional area and perimeter, if
            not given use the center of the bridge.

    Returns: NumPy array ordered by points then times.

    """
    d = drying_responses(
        config=config,
        response_type=response_type,
        times=times,
        points=points,
        cement_class=cement_class,
        x=x,
    )
    a = autogenous_responses(
        config=config, response_type=response_type, times=times, points=points
    )
    assert d.shape == a.shape
    result = np.add(d, a)
    assert result.shape == d.shape
    assert result[0][-1] == d[0][-1] + a[0][-1]
    return result


__all__ = [
    "CementClass",
    "drying_responses",
    "drying",
    "autogenous",
    "autogenous_responses",
    "total",
    "total_responses",
]
