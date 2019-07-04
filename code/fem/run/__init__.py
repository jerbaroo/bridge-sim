"""
Run FEM simulations and generate responses.
"""
from __future__ import annotations

import sys
from timeit import default_timer as timer
from typing import Callable

from fem.params import FEMParams
from fem.responses import NewFEMResponses
from config import Config
from util import *


class FEMRunner():
    """Run FEM simulations and generate responses."""
    def __init__(self,
                 run: Callable[
                    [Config, FEMParams],
                    [int, Dict[Response, [_Response]]]
                 ],
                 name: str):
        self._run = run
        self.name = name

    def run(self, c: Config, fem_params: FEMParams):
        print_i(f"Running {self.name} FEMRunner")
        start = timer()
        max_time, responses_by_type = self._run(c, fem_params)
        end = timer()
        print_i(f"Ran FEM simulation in {end - start:.2f}s")
        for response_type, responses in responses_by_type.items():
            start = timer()
            fem_responses = NewFEMResponses(
                fem_params,
                self.name,
                max_time,
                response_type,
                responses)
            end = timer()
            print_i(f"Built {response_type} FEMResponses in {end - start:.2f}s")
            start = timer()
            fem_responses.save(c)
            end = timer()
            print_i(f"Saved {response_type} FEMResponses in {end - start:.2f}s")
