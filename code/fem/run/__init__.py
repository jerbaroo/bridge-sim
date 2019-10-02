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
from util import print_i, pstr

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
            self.c.generated_dir, f"{self.name}").lower()
        if not os.path.exists(self.built_files_dir):
            os.makedirs(self.built_files_dir)

        self._build = build
        self._run = run
        self._parse = parse
        self._convert = convert

    def run(
            self, expt_params: ExptParams, return_parsed: bool = False,
            return_converted: bool = False, support_3d_nodes: bool = True):
        """Run simulations and save responses using this FEMRunner.

        Args:
            expt_params: ExptParams, parameters for a number of simulations.
            return_parsed: bool, return parsed responses, for testing.
            return_converted: bool, return converted responses, for testing.
            support_3d_nodes: bool, for testing, if False don't include support
                nodes.

        """

        supported_response_types = self.supported_response_types(self.c.bridge)
        # Check that all FEMParams contain supported response types.
        for fem_params in expt_params.fem_params:
            for response_type in fem_params.response_types:
                if response_type not in supported_response_types:
                    raise ValueError(
                        f"{response_type} not supported by {self}")

        # Building.
        start = timer()
        expt_params = self._build(
            c=self.c, expt_params=expt_params, fem_runner=self,
            support_3d_nodes=support_3d_nodes)
        print_i(f"FEMRunner: built {self.name} model file(s) in"
                + f" {timer() - start:.2f}s")

        # Running.
        for sim_ind, _ in enumerate(expt_params.fem_params):
            start = timer()
            expt_params = self._run(self.c, expt_params, self, sim_ind)
            print_i(f"FEMRunner: ran {self.name}"
                    + f" {sim_ind + 1}/{len(expt_params.fem_params)}"
                    + f" simulation in {timer() - start:.2f}s")

        # Parsing.
        start = timer()
        parsed_expt_responses = self._parse(self.c, expt_params, self)
        print_i(f"FEMRunner: parsed all responses in"
                + f" {timer() - start:.2f}s")
        if return_parsed:
            return parsed_expt_responses

        # Converting.
        start = timer()
        converted_responses = self._convert(
            c=self.c, expt_params=expt_params,
            parsed_expt_responses=parsed_expt_responses)
        print_i(f"FEMRunner: converted all responses to [Response] in"
                + f" {timer() - start:.2f}s")
        if return_converted:
            return converted_responses

        # Saving.
        for sim_ind in converted_responses:
            for response_type, responses in (
                    converted_responses[sim_ind].items()):
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

        This function is used for file paths of raw responses saved by the
        FEMRunner, you should not use this directly. Instead you may be
        interested in load_fem_responses or fem_responses_path.

        Args:
            fem_params: FEMParams, parameters for a FEM simulation.
            ext: str, a file extension without the dot.
            append: str, appended before the file extension.

        """
        load_str: str = fem_params.load_str()
        for char in "[]()":
            load_str = load_str.replace(char, "")
        append = append if len(append) == 0 else f"-{append}"
        return pstr(os.path.join(
            self.built_files_dir,
            f"{self.c.bridge.long_name()}-response-params={load_str}{append}"
        )).lower() + f".{ext}"
