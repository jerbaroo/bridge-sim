"""
Run FEM simulations and generate responses.
"""
from __future__ import annotations

import sys
from timeit import default_timer as timer
from typing import Callable

from fem.params import FEMParams
from fem.responses import FEMResponses
from config import Config
from util import *


class FEMRunner():
    """Run FEM simulations and generate responses."""
    def __init__(self,
                 build: Callable[[Config, FEMParams], None],
                 run: Callable[[Config], None],
                 name: str):
        self._run = run
        self.name = name

    def run(self, c: Config, fem_params: FEMParams,
            response_types: [ResponseType]=None):
        print_i(f"FEMRunner: running {self.name} FEM")
        responses_by_type = self._run(c, fem_params)
        for response_type, responses in responses_by_type.items():
            if response_types is None or response_type in response_types:
                start = timer()
                fem_responses = FEMResponses(
                    fem_params, self.name, response_type, responses)
                end = timer()
                print_i(f"Built {response_type} FEMResponses in {end - start:.2f}s")
                start = timer()
                fem_responses.save(c)
                end = timer()
                print_i(f"Saved {response_type} FEMResponses in {end - start:.2f}s")
