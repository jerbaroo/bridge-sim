"""Responses of one type for a number of related simulations."""
import itertools
from collections import deque
from copy import deepcopy
from pathos.multiprocessing import Pool
from typing import List

import numpy as np

from bridge_sim.model import Config, ResponseType
from lib.fem.params import SimParams
from lib.fem.responses import SimResponses, load_fem_responses
from lib.fem.run import FEMRunner


class ExptResponses:
    """Position indexed responses (one response type) for multiple simulations."""

    def __init__(
        self,
        c: Config,
        response_type: ResponseType,
        expt_params: List[SimParams],
        fem_runner: FEMRunner,
        expt_responses: List[SimResponses],
    ):
        self.c = c
        self.response_type = response_type
        self.expt_params = expt_params
        self.fem_runner = fem_runner
        self.expt_responses = expt_responses
        self.num_expts = len(expt_responses)

    # def file_paths(self):
    #     """A unique file path for each simulation's fem."""
    #     return [fem_responses_path(
    #             self.c, fem_params, self.response_type, self.fem_runner.name)
    #         for fem_params in self.expt_params.fem_params]

    def sim_response(
        self,
        expt_frac: float,
        x_frac: float,
        z_frac: float,
        y_frac: float = 1,
        time_index: int = 0,
    ) -> "Response":
        """The response at a position for a simulation.

        Args:
            expt_frac: float, fraction of experiments in [0 1].
            x_frac: float, response position on x-axis in [0 1].
            y_frac: float, response position on y-axis in [0 1].
            z_frac: float, response position on z-axis in [0 1].
            time_index: float, response position on z-axis in [0 1].

        """
        assert 0 <= expt_frac <= 1
        assert 0 <= x_frac <= 1

        # If an experiment index matches exactly, or not interpolating.
        # if expt_ind == int(expt_ind) or not interp_sim:

        expt_ind = np.interp(expt_frac, [0, 1], [0, self.num_expts - 1])
        return self.expt_responses[int(np.rint(expt_ind))].at(
            x_frac=x_frac, y_frac=y_frac, z_frac=z_frac, time_index=time_index
        )

        assert interp_sim
        # Else interpolate fem between two experiment indices.
        expt_ind_lo, expt_ind_hi = int(expt_ind), int(expt_ind) + 1
        expt_lo_frac, expt_hi_frac = np.interp(
            [expt_ind_lo, expt_ind_hi], [0, self.num_expts - 1], [0, 1]
        )
        # print_w(f"Interpolating between loads at indices {expt_ind_lo} & {expt_ind_hi}")
        # print_w(f"Interpolating between loads at {expt_lo_frac} & {expt_hi_frac}, real = {expt_frac}")
        response_lo = self.expt_responses[expt_ind_lo].at(
            x_frac=x_frac,
            y_frac=y_frac,
            z_frac=z_frac,
            time_index=time_index,
            interpolate=interp_response,
        )
        response_hi = self.expt_responses[expt_ind_hi].at(
            x_frac=x_frac,
            y_frac=y_frac,
            z_frac=z_frac,
            time_index=time_index,
            interpolate=interp_response,
        )
        response = np.interp(
            expt_frac, [expt_lo_frac, expt_hi_frac], [response_lo, response_hi]
        )
        # print(f"response = {response}, response_lo = {response_lo}, response_hi = {response_hi}")
        return response


def load_expt_responses(
    c: Config,
    expt_params: List[SimParams],
    response_type: ResponseType,
    run_only: bool = False,
) -> List[SimResponses]:
    """Load fem of one sensor type for related simulations.

    The simulations will be run in parallel if 'Config.parallel > 1'. If the
    'run_only' option is passed, then the simulations will run but nothing will
    be loaded into memory.

    """
    indices_and_params = list(zip(itertools.count(), expt_params))

    def process(index_and_params, _run_only: bool = True):
        i, sim_params = index_and_params
        return load_fem_responses(
            c=deepcopy(c),
            sim_params=deepcopy(sim_params),
            response_type=response_type,
            run_only=_run_only,
            index=(i + 1, len(expt_params)),
        )

    # First run the simulations (if necessary), in parallel if requested.
    if c.parallel > 1:
        with Pool(processes=c.parallel) as pool:
            pool.map(process, indices_and_params)
    else:
        deque(map(process, indices_and_params), maxlen=0)
    # Return after generating results if requested...
    if run_only:
        return
    # ...otherwise yield all of the results.
    for index_params in indices_and_params:
        yield process(index_params, _run_only=False)
