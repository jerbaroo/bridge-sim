"""Run FEM simulations and generate responses."""
from __future__ import annotations

import os
from timeit import default_timer as timer
from typing import Callable, Dict, List, Optional, TypeVar

from config import Config
from fem.params import ExptParams, FEMParams
from fem.responses import FEMResponses
from model import Response
from model.bridge import Bridge
from model.response import ResponseType
from util import print_i

Parsed = TypeVar("Parsed")


class FEMRunner:
    """Run FEM simulations with an external program and generate responses.

    NOTE: For running simulations and loading responses you should instead use
    the load_fem_responses function.

    Args:
        supported_response_types: Callable[[Bridge], List[ResponseType]], the
            supported response types for a given bridge.

    """

    def __init__(
            self, c: Config, name: str,
            supported_response_types: Callable[[Bridge], List[ResponseType]],
            build: Callable[[Config, ExptParams, FEMRunner], ExptParams],
            run: Callable[[Config, ExptParams, FEMRunner, int], ExptParams],
            parse: Callable[[Config, ExptParams, FEMRunner], Parsed],
            convert: Callable[
                [Config, Parsed],
                Dict[int, Dict[ResponseType, List[Response]]]]):
        self.c = c
        self.name = name
        self.supported_response_types = supported_response_types
        self.built_files_dir = os.path.join(
            self.c.generated_dir, f"{self.name}/").lower()
        assert self.built_files_dir.endswith("/")
        if not os.path.exists(self.built_files_dir):
            os.makedirs(self.built_files_dir)

        self._build = build
        self._run = run
        self._parse = parse
        self._convert = convert

    def run(self, expt_params: ExptParams, run=True, save=True):

        supported_response_types = self.supported_response_types(self.c.bridge)
        # Check that all FEMParams contain supported response types.
        for fem_params in expt_params.fem_params:
            for response_type in fem_params.response_types:
                if response_type not in supported_response_types:
                    raise ValueError(
                        f"{response_type} not supported by {self}")

        start = timer()
        expt_params = self._build(self.c, expt_params, self)
        print_i(f"FEMRunner: built {self.name} model file(s) in"
                + f" {timer() - start:.2f}s")

        if run:
            for sim_ind, _ in enumerate(expt_params.fem_params):
                start = timer()
                expt_params = self._run(self.c, expt_params, self, sim_ind)
                print_i(f"FEMRunner: ran {self.name}"
                        + f" {sim_ind + 1}/{len(expt_params.fem_params)}"
                        + f" simulation in {timer() - start:.2f}s")

        if not save:
            return

        start = timer()
        parsed_by_type = self._parse(self.c, expt_params, self)
        print_i(f"FEMRunner: parsed all responses in"
                + f" {timer() - start:.2f}s")

        start = timer()
        sim_responses = self._convert(self.c, parsed_by_type)
        print_i(f"FEMRunner: converted all responses to [Response] in"
                + f" {timer() - start:.2f}s")

        for sim_ind in sim_responses:
            for response_type, responses in sim_responses[sim_ind].items():
                fem_responses = FEMResponses(
                    c=self.c, fem_params=expt_params.fem_params[sim_ind],
                    runner_name=self.name, response_type=response_type,
                    responses=responses, skip_build=True)

                start = timer()
                fem_responses.save(self.c)
                print_i(
                    f"FEMRunner: saved simulation {sim_ind + 1} FEMResponses"
                    + f" in ([Response]) in {timer() - start:.2f}s,"
                    + f"({response_type})")

    def fem_file_path(
            self, fem_params: FEMParams, ext: str, append: str = "") -> str:
        """A file path based on a bridge, FEMParams and this FEMRunner.

        Args:
            fem_params: FEMParams, parameters for a FEM simulation.
            ext: str, the file extension of the file.
            append: str, a string to append before the file extension.

        """
        load_str: str = fem_params.load_str()
        for char in "[]()":
            load_str = load_str.replace(char, "")
        append = append if len(append) == 0 else f"-{append}"
        return os.path.join(
            self.built_files_dir,
            f"{self.name}-{self.c.bridge.name}"
            + f"-{self.c.bridge.dimensions.name()}-{load_str}{append}.{ext}"
        ).replace(" ", "").lower()
