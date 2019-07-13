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


class FEMRunner():
    """Run FEM simulations and generate responses."""
    def __init__(self,
                 name: str,
                 build: Callable[[Config, ExptParams], ExptParams],
                 run: Callable[[Config, ExptParams], ExptParams],
                 parse: Callable[
                     [Config, ExptParams, List[ResponseType]],
                     Parsed],
                 convert: Callable[
                     [Config, Parsed, List[ResponseType]],
                     Dict[int, Dict[ResponseType, List[Response]]]]):
        self._build = build
        self._run = run
        self._parse = parse
        self._convert = convert
        self.name = name

    def run(self, c: Config, expt_params: ExptParams):
        start = timer()
        expt_params = self._build(c, expt_params)
        print_i(f"FEMRunner: built {self.name} model file in"
                + f"{timer() - start:.2f}s")

        start = timer()
        expt_params = self._run(c, expt_params)
        print_i(f"FEMRunner: ran {self.name} simulation in"
                + f"{timer() - start:.2f}s")

        start = timer()
        parsed_by_type = self._parse(c, expt_params)
        print_i(f"FEMRunner: parsed all responses in"
                + f"{timer() - start:.2f}s")

        start = timer()
        sim_responses = self._convert(c, expt_params, parsed_by_type)
        print_i(f"FEMRunner: converted all to [Response] in"
                + f"{timer() - start:.2f}s")

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
