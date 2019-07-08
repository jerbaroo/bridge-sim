"""
Run FEM simulations and generate responses.
"""
from __future__ import annotations

import sys
from timeit import default_timer as timer
from typing import Callable, Generic, TypeVar

from fem.params import FEMParams
from fem.responses import FEMResponses
from config import Config
from util import *

P = TypeVar("P")


class FEMRunner():
    """Run FEM simulations and generate responses."""
    def __init__(self,
                 name: str,
                 build: Callable[[Config, FEMParams], None],
                 run: Callable[[Config], None],
                 parse: Callable[
                     [Config, [ResponseType]],
                     Dict[ResponseType, P]],
                 convert: Callable[
                     [Config, Dict[ResponseType, P]],
                     Dict[Response_Type, [Response]]]):
        self._build = build
        self._run = run
        self._parse = parse
        self._convert = convert
        self.name = name

    def run(self, c: Config, fem_params: FEMParams,
            response_types: [ResponseType]=None):
        start = timer()
        self._build(c, fem_params)
        end = timer()
        print_i(f"FEMRunner: built model file in {end - start:.2f}s")

        start = timer()
        self._run(c)
        end = timer()
        print_i(f"FEMRunner: ran simulation in {end - start:.2f}s")

        start = timer()
        # TODO: Return parsing time per ResponseType.
        parsed_by_type = self._parse(c, response_types)
        end = timer()
        print_i(f"FEMRunner: parsed all responses in {end - start:.2f}s")

        start = timer()
        # TODO: Return conversion time per ResponseType.
        responses_by_type = self._convert(c, parsed_by_type)
        end = timer()
        print_i(f"FEMRunner: converted all to [Response] in {end - start:.2f}s")

        for response_type, responses in responses_by_type.items():
            if response_types is None or response_type in response_types:
                start = timer()
                fem_responses = FEMResponses(
                    fem_params, self.name, response_type, responses)
                end = timer()
                print_i(f"FEMRunner: built FEMResponses in {end - start:.2f}s, ({response_type})")

                start = timer()
                fem_responses.save(c)
                end = timer()
                print_i(f"FEMRunner: saved FEMResponses in {end - start:.2f}s, ({response_type})")
