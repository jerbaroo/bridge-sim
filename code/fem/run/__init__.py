"""Run FEM simulations and generate responses."""
from __future__ import annotations

from timeit import default_timer as timer
from typing import Callable, TypeVar

from config import Config
from fem.params import ExptParams, FEMParams
from fem.responses import FEMResponses
from model import *
from util import *


Parsed = TypeVar("parsed")


def fem_id(fem_params: FEMParams, fem_runner: FEMRunner) -> str:
    """A string unique to this FEMRunner and parameters."""
    load_str: str = fem_params.load_str()
    for char in "[]()":
        load_str = load_str.replace(char, "")
    return (f"{fem_runner.name}-{load_str}")


def fem_file_path(fem_params: FEMParams, fem_runner: FEMRunner) -> str:
    """A file path based on FEM parameters and runner."""
    return os.path.join(
        fem_runner.built_model_dir,
        f"{fem_id(fem_params, fem_runner)}.{fem_runner.built_model_ext}"
    ).replace(" ", "")


class FEMRunner():
    """Run FEM simulations and generate responses.

    Args:
        built_model_dir: str, directory to save the built model file in.

    """
    def __init__(self,
                 name: str,
                 build: Callable[[Config, ExptParams, FEMRunner], ExptParams],
                 run: Callable[[Config, ExptParams, FEMRunner], ExptParams],
                 parse: Callable[[Config, ExptParams, FEMRunner], Parsed],
                 convert: Callable[
                     [Config, Parsed],
                     Dict[int, Dict[ResponseType, List[Response]]]],
                 built_model_ext: str,
                 built_model_dir: str="."):
        self._build = build
        self._run = run
        self._parse = parse
        self._convert = convert
        self.name = name
        self.built_model_ext = built_model_ext
        self.built_model_dir = built_model_dir

    def run(self, c: Config, expt_params: ExptParams, run=True, save=True,
            remove=False):

        start = timer()
        expt_params = self._build(c, expt_params, self)
        print_i(f"FEMRunner: built {self.name} model file(s) in"
                + f" {timer() - start:.2f}s")

        if run:
            for sim_ind, _ in enumerate(expt_params.fem_params):
                start = timer()
                expt_params = self._run(c, expt_params, self, sim_ind)
                print_i(f"FEMRunner: ran {self.name}"
                        + f" {sim_ind + 1}/{len(expt_params.fem_params)}"
                        + f" simulation in {timer() - start:.2f}s")

        if remove:
            for fem_params in expt_params.fem_params:
                os.remove(built_model_path(fem_params, self))

        if not save:
            return

        start = timer()
        parsed_by_type = self._parse(c, expt_params, self)
        print_i(f"FEMRunner: parsed all responses in"
                + f" {timer() - start:.2f}s")

        start = timer()
        sim_responses = self._convert(c, parsed_by_type)
        print_i(f"FEMRunner: converted all responses to [Response] in"
                + f" {timer() - start:.2f}s")

        for sim in sim_responses:
            for response_type, responses in sim_responses[sim].items():
                start = timer()
                fem_responses = FEMResponses(
                    expt_params.fem_params[sim], self.name, response_type,
                    responses, skip_build=True)
                # print_i(f"FEMRunner: built simulation {sim + 1} FEMResponses"
                #         + f" in {timer() - start:.2f}s, ({response_type})")

                start = timer()
                fem_responses.save(c)
                print_i(f"FEMRunner: saved simulation {sim + 1} FEMResponses"
                        + f" in ([Response]) in {timer() - start:.2f}s,"
                        + f"({response_type})")
