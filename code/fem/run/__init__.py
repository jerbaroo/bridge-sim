"""
Run FEM simulations and generate responses.
"""
from __future__ import annotations

import sys
from typing import Callable

from fem.params import FEMParams
from fem.responses import FEMResponses, NewFEMResponses
from config import Config


class FEMRunner():
    """Run FEM simulations and generate responses."""
    def __init__(self,
                 run: Callable[[Config, FEMParams],
                               Dict[Response, [_Response]]],
                 name: str):
        self._run = run
        self.name = name

    def run(self, c: Config, fem_params: FEMParams):
        print("Running FEMRunner._run")
        responses_by_type = self._run(c, fem_params)
        print("Collected responses from FEMRunner._run")
        for response_type, responses in responses_by_type.items():

            responses = list(responses)

            print(type(responses))
            print(len(responses))
            print(type(responses[0]))
            print(len(responses[0]))
            print(type(responses[0][0]))

            NewFEMResponses(
                fem_params,
                self.name,
                response_type,
                responses
            ).save(c)
