"""Responses of one type for a number of related simulations."""
from typing import List

import numpy as np

from config import Config
from fem.params import ExptParams
from fem.responses import fem_responses_path, FEMResponses, load_fem_responses
from fem.run import FEMRunner
from model import Response
from model.response import ResponseType
from util import print_w, print_i

# TODO: Replace by ResponsesMatrix (renamed to ExptResponses).
ExptResponses = List[FEMResponses]


# TODO: return ResponsesMatrix.
def load_expt_responses(
        c: Config, expt_params: ExptParams, response_type: ResponseType,
        fem_runner: FEMRunner) -> ExptResponses:
    """Load responses of one sensor type for a number of related simulations."""
    results = []
    for i, fem_params in enumerate(expt_params.fem_params):
        results.append(load_fem_responses(
            c, fem_params, response_type, fem_runner))
        print_i(f"Loading FEMResponses {i + 1}/{len(expt_params.fem_params)}")
    return results


# TODO: Replace ExptResponses.
class ResponsesMatrix:
    """Responses of one sensor type for a number of related simulations."""
    def __init__(
            self, c: Config, response_type: ResponseType,
            expt_params: ExptParams, fem_runner_name: str,
            expt_responses: ExptResponses):
        self.c = c
        self.response_type = response_type
        self.expt_params = expt_params
        self.fem_runner_name = fem_runner_name
        self.expt_responses = expt_responses
        self.num_expts = len(expt_responses)

    def file_paths(self):
        """A file path for each simulation's responses."""
        return [fem_responses_path(
                    self.c, fem_params, self.response_type,
                    self.fem_runner_name)
                for fem_params in self.expt_params.fem_params]

    # TODO: Rename to response, later.
    def response_(
            self, expt_frac: float, x_frac: float, y_frac: float = 0,
            z_frac: float = 0, time_index: int = 0, interpolate: bool = False
            ) -> Response:
        """The response at a position for a simulation.

        Note that if expt_frac (e.g. 0.5) does not correspond exactly to a
        simulation index (e.g. 4.2 instead of 4), then the result will be
        interpolated from the results of the indices on both sides (e.g. 4 and
        5).

        Args:
            expt_frac: float, fraction of experiments in [0 1].
            x_frac: float, response position on x-axis in [0 1].
            y_frac: float, response position on y-axis in [0 1].
            z_frac: float, response position on z-axis in [0 1].
            time_index: float, response position on z-axis in [0 1].
            interpolate: bool, whether to interpolate the response between
            responses from two simulations (true), or return the response from
            the closes simulation (false).

        """
        assert 0 <= expt_frac <= 1
        assert 0 <= x_frac <= 1

        # If an experiment index matches exactly, or not interpolating.
        expt_ind = np.interp(expt_frac, [0, 1], [0, self.num_expts - 1])
        if expt_ind == int(expt_ind) or not interpolate:
            # print_w(f"Not interpolating, expt_frac = {expt_frac}, expt_ind = {expt_ind}")
            return self.expt_responses[int(expt_ind)].at(
                x_frac=x_frac, y_frac=y_frac, z_frac=z_frac,
                time_index=time_index)

        if interpolate:
            raise RuntimeError("Should not be interpolating.")
        # Else interpolate responses between two experiment indices.
        expt_ind_lo, expt_ind_hi = int(expt_ind), int(expt_ind) + 1
        expt_lo_frac, expt_hi_frac = np.interp(
            [expt_ind_lo, expt_ind_hi], [0, self.num_expts - 1], [0, 1])
        print_w(f"Interpolating between loads at indices {expt_ind_lo} & {expt_ind_hi}")
        print_w(f"Interpolating between loads at {expt_lo_frac} & {expt_hi_frac}, real = {expt_frac}")
        response_lo = self.expt_responses[expt_ind_lo].at(
            x_frac=x_frac, y_frac=y_frac, z_frac=z_frac, time_index=time_index)
        response_hi = self.expt_responses[expt_ind_hi].at(
            x_frac=x_frac, y_frac=y_frac, z_frac=z_frac, time_index=time_index)
        response = np.interp(
            expt_frac,
            [expt_lo_frac, expt_hi_frac],
            [response_lo, response_hi])
        print(f"response = {response}, response_lo = {response_lo}, response_hi = {response_hi}")
        return response
