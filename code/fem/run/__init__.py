"""Run FEM simulations and generate responses."""
from __future__ import annotations

import sys
from timeit import default_timer as timer
from typing import Callable, TypeVar

from fem.params import FEMParams
from fem.responses import FEMResponses
from config import Config
from util import *


Parsed = TypeVar("parsed")


def built_model_path(fem_params: FEMParams, fem_runner: FEMRunner):
    """A file path based on FEM parameters and runner."""
    return (f"{fem_runner.built_model_path_prefix}-{fem_params.load_str()}"
            + f".{fem_runner.built_model_path_ext}")


class FEMRunner():
    """Run FEM simulations and generate responses."""
    def __init__(self,
                 name: str,
                 build: Callable[[Config, ExptParams, FEMRunner], ExptParams],
                 run: Callable[[Config, ExptParams, FEMRunner], ExptParams],
                 parse: Callable[
                     [Config, ExptParams, List[ResponseType]],
                     Parsed],
                 convert: Callable[
                     [Config, Parsed, List[ResponseType]],
                     Dict[int, Dict[ResponseType, List[Response]]]],
                 built_model_path_prefix: str,
                 built_model_path_ext: str):
        self._build = build
        self._run = run
        self._parse = parse
        self._convert = convert
        self.name = name
        self.built_model_path_prefix = built_model_path_prefix
        self.built_model_path_ext = built_model_path_ext

    def run(self, c: Config, expt_params: ExptParams, run=True, save=True):

        start = timer()
        expt_params = self._build(c, expt_params, self)
        print_i(f"FEMRunner: built {self.name} model file(s) in"
                + f" {timer() - start:.2f}s")

        if run:
            start = timer()
            expt_params = self._run(c, expt_params, self)
            print_i(f"FEMRunner: ran {len(expt_params.fem_params)} {self.name}"
                    + f" simulation in {timer() - start:.2f}s")

        for fem_params in expt_params.fem_params:
            os.remove(built_model_path(fem_params, self))

        if not save:
            return

        start = timer()
        parsed_by_type = self._parse(c, expt_params)
        print_i(f"FEMRunner: parsed all responses in"
                + f" {timer() - start:.2f}s")

        start = timer()
        sim_responses = self._convert(c, expt_params, parsed_by_type)
        print_i(f"FEMRunner: converted all to [Response] in"
                + f" {timer() - start:.2f}s")

        for sim in sim_responses:
            for response_type, responses in sim_responses[sim].items():
                start = timer()
                fem_responses = FEMResponses(
                    expt_params.fem_params[sim], self.name, response_type,
                    responses, skip_build=True)
                print_i(f"FEMRunner: built simulation {sim} FEMResponses in"
                        + f" {timer() - start:.2f}s, ({response_type})")

                start = timer()
                fem_responses.save(c)
                print_i(f"FEMRunner: saved simulation {sim} FEMResponses"
                        + f" ([Response]) in {timer() - start:.2f}s,"
                        + f"({response_type})")
