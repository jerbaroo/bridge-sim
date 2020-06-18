"""Time series of responses to creep."""

from math import sqrt
from typing import List, Union

import numpy as np
from bridge_sim import sim
from bridge_sim.model import Config, ResponseType, Point

from bridge_sim.shrinkage import CementClass, RH, f_cm, notational_size
from bridge_sim.sim.model import Responses
from bridge_sim.util import print_d, convert_times
from numba import njit

D = True

a = {
    CementClass.Slow: -1,
    CementClass.Normal: 0,
    CementClass.Rapid: 1,
}
"""A power depending on cement class."""

a_1 = (35 / f_cm) ** 0.7
a_2 = (35 / f_cm) ** 0.2
a_3 = (35 / f_cm) ** 0.5


def creep_coeff(
    config: Config, cement_class: CementClass, times: List[float], x: float
) -> List[float]:
    """Creep coefficient over time.

    Args:
        config: simulation configuration object.
        cement_class: class of the cement.
        times: seconds when to compute strain.
        x: X position used to calculate cross-sectional area and perimeter.

    Returns: list of creep coefficient at each given time.

    """
    h_0 = notational_size(config=config, x=x)
    times = np.array(convert_times(f="second", t="day", times=times))
    t_0T = 7  # Temperature adjusted age of concrete.
    # The effect of type of cement on the creep.
    t_0 = max(t_0T * ((9 / (2 + t_0T ** 1.2)) ** a[cement_class]), 0.5)
    print_d(D, f"t_0 = {t_0}")
    # A factor to allow for the effect of relative humidity on the notational
    # creep coefficient.
    y_RH = None
    if f_cm <= 35:
        y_RH = 1 + ((1 - RH) / (0.1 * h_0 ** (1 / 3)))
    else:
        print_d(D, f"y_RH > 35")
        y_RH = (1 + ((1 - RH) / (0.1 * (h_0 ** (1 / 3))) * a_1)) * a_2
    print_d(D, f"y_RH = {y_RH}")
    # A factor to allow for the effect of concrete age at loading on the
    # notational creep coefficient.
    def B_t0(t_0_):
        return 1 / (0.1 + t_0_ ** 0.2)

    print_d(D, f"B_t0(t_0) = {B_t0(t_0)}")
    # A factor to allow for the effect of concrete strength on the notational
    # creep coefficient.
    B_fcm = 16.8 / sqrt(f_cm)
    print_d(D, f"B_fcm = {B_fcm}")
    # Notational creep coefficient.
    def y_0(t_0_):
        return y_RH * B_fcm * B_t0(t_0_)

    print_d(D, f"y_0(t_0_) = {y_0(t_0)}")
    B_H = None
    if f_cm <= 35:
        B_H = min(1500, (1.5 * (1 + (0.012 * RH * 100) ** 18) * h_0) + 250)
    else:
        B_H = min(
            1500 * a_3, (1.5 * (1 + (0.012 * RH * 100) ** 18) * h_0) + (250 * a_3)
        )
    print_d(D, f"B_H = {B_H}")
    # Describe the time course of the creep.
    def B_c(t_, t_0_):
        return np.power((t_ - t_0_) / (B_H + t_ - t_0_), 0.3)

    coeff = y_0(t_0) * B_c(times, t_0)
    # Set initial strain values to 0.
    i = 0
    while i < len(coeff) and not coeff[i] >= 0:
        coeff[i] = 0
    return coeff


def creep_responses(
    config: Config,
    times: List[float],
    responses: Union[Responses, List[List[float]]],
    points: List[Point],
    cement_class: CementClass,
    x: float,
    psi: float = 1,
) -> List[List[float]]:
    """Responses over time at points due to creep.

    Args:
        config: simulation configuration object.
        times: seconds when to compute responses.
        cement_class: class of the cement.
        x: X position used to calculate cross-sectional area and perimeter.

    Returns: NumPy array ordered by points then times.

    """
    coeff = creep_coeff(config=config, cement_class=cement_class, times=times, x=x)
    if isinstance(responses, Responses):
        responses_at = responses.at_decks(points)
    else:
        assert len(responses) == len(points)
        assert len(responses[0]) == len(times)
        responses_at = responses
    result = np.empty((len(points), len(times)))
    for p in range(len(points)):
        result[p] = responses_at[p] * (1 + (coeff * psi))
    return result


__all__ = ["creep_coeff", "creep_responses"]
