"""Time series of responses to shrinkage."""

from enum import Enum
from math import sqrt
from typing import List

import numpy as np
from numba import njit

from bridge_sim import sim
from bridge_sim.model import Config, Point, ResponseType
from bridge_sim.util import convert_times, print_d

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


def drying(cement_class: CementClass, h_0: float, times: List[float]) -> List[float]:
    """Strain due to drying shrinkage over time.

    Args:
        cement_class: class of the cement.
        h_0: notational size.
        times: seconds when to compute strain.

    Returns: list of strain at each given time.

    """
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
    h_0: float,
) -> List[List[float]]:
    """Responses over time at points due to drying shrinkage.

    Args:
        config: simulation configuration object.
        response_type: simulation response type.
        times: seconds when to compute responses.
        points: points where to compute responses.
        cement_class: class of the cement.
        h_0: notational size.

    Returns: NumPy array ordered by points then times.

    """
    strain = drying(cement_class=cement_class, h_0=h_0, times=times)
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


def total(cement_class: CementClass, h_0: float, times: List[float]) -> List[float]:
    """Strain due to drying and autogenous shrinkage over time.

    Args:
        cement_class: class of the cement.
        h_0: notational size.
        times: seconds when to compute strain.

    Returns: list of strain at each given time.

    """
    d = drying(cement_class=cement_class, h_0=h_0, times=times)
    a = autogenous(times)
    assert len(a) == len(d)
    result = d + a
    assert len(result) == len(d)
    assert result[0] == d[0] + a[0]
    return result


def total_responses(
    config: Config,
    response_type: ResponseType,
    times: List[float],
    points: List[Point],
    cement_class: CementClass,
    h_0: float,
) -> List[List[float]]:
    """Responses over time at points due to drying shrinkage.

    Args:
        config: simulation configuration object.
        response_type: simulation response type.
        times: seconds when to compute responses.
        points: points where to compute responses.
        cement_class: class of the cement.
        h_0: notational size.

    Returns: NumPy array ordered by points then times.

    """
    d = drying_responses(
        config=config,
        response_type=response_type,
        times=times,
        points=points,
        cement_class=cement_class,
        h_0=h_0,
    )
    a = autogenous_responses(
        config=config, response_type=response_type, times=times, points=points
    )
    assert d.shape == a.shape
    result = np.add(d, a)
    assert result.shape == d.shape
    assert result[0][0] == d[0][0] + a[0][0]
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
