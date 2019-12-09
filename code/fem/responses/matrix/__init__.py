"""Responses of one type for a number of related simulations."""
import itertools
from pathos.multiprocessing import Pool
from typing import Callable, List

import numpy as np

from config import Config
from fem.params import ExptParams
from fem.responses import FEMResponses, load_fem_responses
from fem.run import FEMRunner
from model import Response
from model.response import ResponseType
from util import print_i


class ResponsesMatrix:
    """Indexed responses of one sensor type for a number of simulations."""

    def __init__(
        self,
        c: Config,
        response_type: ResponseType,
        expt_params: ExptParams,
        fem_runner: FEMRunner,
        expt_responses: List[FEMResponses],
        save_all: bool,
    ):
        self.c = c
        self.response_type = response_type
        self.expt_params = expt_params
        self.fem_runner = fem_runner
        self.expt_responses = expt_responses
        self.num_expts = len(expt_responses)
        self.save_all = save_all

    # def file_paths(self):
    #     """A unique file path for each simulation's responses."""
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
    ) -> Response:
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
        # Else interpolate responses between two experiment indices.
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

    @staticmethod
    def load(
        c: Config,
        id_str: str,
        expt_params: ExptParams,
        load_func: Callable[[ExptParams], "ResponsesMatrix"],
        fem_runner: FEMRunner,
        save_all: bool,
    ) -> "ResponsesMatrix":
        """Load and return a ResponsesMatrix.

        If a ResponsesMatrix is already available in memory with ID 'id_str'
        then that will be returned, otherwise a new ResponsesMatrix will be
        created by running simulations based on 'expt_params'.

        Args:
            c: Config, global configuration object.
            id_str: str, string uniquely identifying the ResponsesMatrix.
            expt_params: ExptParams, parameters for the simulations to run.
            load_func: Callable[[ExptParams], ResponsesMatrix], function that
                given simulation parameters runs simulations and returns a
                ResponsesMatrix.
            fem_runner: FEMRunner, program to run finite element simulations.
            save_all: bool, whether to save responses from all sensor types when
                running simulations, this is useful if simulations take a long
                time to run and you anticipate needing other sensor types.

        """
        # Load ResponsesMatrix if already in memory.
        if id_str in c.resp_matrices:
            return c.resp_matrices[id_str]
        # If save_all then set each FEMParams to all ResponseTypes, which
        # depends on the combination of FEMRunner and bridge.
        if save_all:
            all_response_types = fem_runner.supported_response_types(c.bridge)
            for fem_params in expt_params.sim_params:
                fem_params.response_types = all_response_types
        resp_matrix = load_func(expt_params)
        c.resp_matrices[id_str] = resp_matrix
        return resp_matrix


def load_expt_responses(
    c: Config,
    expt_params: ExptParams,
    response_type: ResponseType,
    sim_runner: FEMRunner,
) -> List[FEMResponses]:
    """Load responses of one sensor type for related simulations."""
    indices_and_params = list(zip(itertools.count(), expt_params.sim_params))

    def process(index_and_params):
        i, sim_params = index_and_params
        return load_fem_responses(
            c=c,
            sim_params=sim_params,
            response_type=response_type,
            sim_runner=sim_runner,
            index=(i + 1, len(expt_params.sim_params)),
        )

    if c.parallel:
        print_i("Running simulations in parallel")
        with Pool() as pool:
            results = pool.map(process, indices_and_params)
    else:
        results = []
        for index_params in indices_and_params:
            results.append(process(index_params))

    print()  # Add a newline to fix cursor position.
    return results
