"""
Run FEM simulations and generate responses.
"""
from typing import Callable

from fem.params import FEMParams
from config import Config


class FEMRunner():
    """Run FEM simulations and generate responses."""
    def __init__(self, run: Callable[[Config, FEMParams, str], None],
                 name: str):
        self.run = lambda c, params: run(c, params, self.name)
        self.name = name
