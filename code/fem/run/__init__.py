"""
Run FEM simulations and generate responses.
"""
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
                 build: Callable[[Config, FEMParams], None],
                 run: Callable[[Config], None],
                 parse: Callable[
                     [Config, [ResponseType]],
                     Parsed],
                 convert: Callable[
                     [Config, Parsed, [ResponseType]],
                     Dict[ResponseType, [Response]]]):
        self._build = build
        self._run = run
        self._parse = parse
        self._convert = convert
        self.name = name

    def run(self, c: Config, fem_params: FEMParams):
        start = timer()
        self._build(c, fem_params)
        print_i(f"FEMRunner: built {self.name} model file in {timer() - start:.2f}s")

        start = timer()
        self._run(c)
        print_i(f"FEMRunner: ran {self.name} simulation in {timer() - start:.2f}s")

        start = timer()
        # TODO: Return parsing time per ResponseType.
        parsed_by_type = self._parse(c, fem_params.response_types)
        print_i(f"FEMRunner: parsed all responses in {timer() - start:.2f}s")

        start = timer()
        # TODO: Return conversion time per ResponseType.
        responses_by_type = self._convert(
            c, parsed_by_type, fem_params.response_types)
        print_i(f"FEMRunner: converted all to [Response] in {timer() - start:.2f}s")

        for response_type, responses in responses_by_type.items():
            start = timer()
            fem_responses = FEMResponses(
                fem_params, self.name, response_type, responses,
                skip_build=True)
            print_i(f"FEMRunner: built FEMResponses in {timer() - start:.2f}s, ({response_type})")

            start = timer()
            fem_responses.save(c)
            print_i(f"FEMRunner: saved FEMResponses ([Response]) in {timer() - start:.2f}s, ({response_type})")
