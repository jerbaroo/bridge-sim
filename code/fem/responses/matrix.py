"""Responses of one type for a number of related simulations."""
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from config import Config
from fem.params import ExptParams, FEMParams
from fem.responses import ExptResponses, fem_responses_path, load_expt_responses
from fem.run import FEMRunner
from fem.run.opensees import os_runner
from model import Response
from model.bridge.bridge_705 import bridge_705_config
from model.load import DisplacementCtrl, Load
from model.response import ResponseType
from util import print_w


# TODO: Replace ExptResponses.
class ResponsesMatrix:
    """Responses of one type for a number of related simulations."""
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

    def filepaths(self):
        """The filepath of each simulation's responses."""
        return [fem_responses_path(
                    self.c, fem_params, self.response_type,
                    self.fem_runner_name)
                for fem_params in self.expt_params.fem_params]

    # TODO: Rename to response, later.
    def response_(
            self, expt_frac: float, x_frac: float, y_frac: float = 0,
            z_frac: float = 0, time_index: int = 0) -> Response:
        """The response at a position for a simulation.

        Note that if expt_frac (e.g. 0.5) does not correspond exactly to a
        simulation index (e.g. 4.2 instead of 4), then the result will be
        interpolated from the results of the indices on both sides (e.g. 4 and
        5).

        Args:
            expt_frac: float, fraction of experiments in [0 1].
            x_frac: float, response position on x-axis in [0 1].

        """
        assert 0 <= expt_frac and expt_frac <= 1
        assert 0 <= x_frac and x_frac <= 1
        # If an exact experiment index is available, or interpolation is not
        # being used then return the response for the calculated experiment
        # index.
        expt_ind = np.interp(expt_frac, [0, 1], [0, self.num_expts - 1])
        if expt_ind == int(expt_ind):
            print_w(f"Not interpolating, expt_frac = {expt_frac}, expt_ind = {expt_ind}")
            return self.expt_responses[int(expt_ind)].at(
                x_frac=x_frac, y_frac=y_frac, z_frac=z_frac,
                time_index=time_index)
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


class DCMatrix(ResponsesMatrix):
    """Responses of one type for displacement control simulations."""

    # TODO Factor out to ResponsesMatrix.load.
    @staticmethod
    def load(
            c: Config, response_type: ResponseType, fem_runner: FEMRunner,
            displacement: float=0.1, save_all: bool=True):
        """Load a DCMatrix from disk, running simulations first if necessary.

        Args:
            response_type: ResponseType, the type of response to load.
            fem_runner: FEMRunner, the FEM program to run simulations with.
            displacement: float, the extent of the displacement at each pier.
            save_all: bool, save all response types when running a simulation.

        """

        def dc_matrix_id() -> str:
            return (f"dc-{response_type}-{fem_runner.name}-{displacement}")

        # Return ILMatrix if already calculated.
        id_ = dc_matrix_id()
        if id_ in c.il_matrices:
            return c.il_matrices[id_]

        # Determine simulation parameters.
        # If save_all is true pass all response types.
        response_types=(
            [rt for rt in ResponseType] if save_all else [response_type])
        expt_params = ExptParams([
            FEMParams(
                loads=[],
                displacement_ctrl=DisplacementCtrl(displacement, i),
                response_types=response_types)
            for i in range(len(c.bridge.fixed_nodes))])

        # Calculate DCMatrix, keep a reference and return.
        c.il_matrices[id_] = DCMatrix(
            c, response_type, expt_params, fem_runner.name,
            load_expt_responses(c, expt_params, response_type, fem_runner)) 
        return c.il_matrices[id_]


class ILMatrix(ResponsesMatrix):
    """Responses of one sensor type for influence line simulations."""

    def response_to(
            self, resp_x_frac: float, load_x_frac: float, load: float,
            y_frac: float = 1, z_frac: float = 0.5, time_index: int = 0):
        """The response value at a position to a load at a position.

        Args:
            resp_x_frac: float, response position on x-axis in [0 1].
            load_x_frac: float, load position on x-axis in [0 1].
            load: float, value of the load.

        """
        assert 0 <= resp_x_frac and resp_x_frac <= 1
        assert 0 <= load_x_frac and load_x_frac <= 1
        # TODO: Check arguments.
        response = self.response_(
            expt_frac=load_x_frac, x_frac=resp_x_frac, y_frac=y_frac,
            z_frac=z_frac, time_index=time_index)
        # print_d(f"resp_x_frac = {resp_x_frac}, load_x_frac = {load_x_frac}, load = {load}")
        return (response * (load / self.c.il_unit_load_kn))


def load_il_matrix(
        c: Config, response_type: ResponseType, fem_runner: FEMRunner,
        num_loads: int=100, save_all: bool=True) -> ILMatrix:
    """Load an ILMatrix from disk, running simulations first if necessary.

    Args:
        response_type: ResponseType, the type of sensor response to load.
        fem_runner: FEMRunner, the FEM program to run simulations with.
        num_loads: int, the number of equidistant positions to apply load.
        save_all: bool, save all response types when running a simulation.

    """

    def il_matrix_id() -> str:
        return (f"il-{response_type}-{fem_runner.name}-{c.il_unit_load_kn}"
                + f"-{num_loads}")

    # Return ILMatrix if already calculated.
    id_ = il_matrix_id()
    if id_ in c.il_matrices:
        return c.il_matrices[id_]

    # Determine simulation parameters.
    # If save_all is true pass all response types.
    response_types=(
        [rt for rt in ResponseType] if save_all else [response_type])
    expt_params = ExptParams([
        FEMParams(
            loads=[Load(x_frac, c.il_unit_load_kn)],
            response_types=response_types)
        for x_frac in np.linspace(0, 1, num_loads)])

    # Calculate ILMatrix, keep a reference and return.
    c.il_matrices[id_] = ILMatrix(
        c, response_type, expt_params, fem_runner.name,
        load_expt_responses(c, expt_params, response_type, fem_runner))
    return c.il_matrices[id_]
