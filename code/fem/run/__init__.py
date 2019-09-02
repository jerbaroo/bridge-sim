"""Run FEM simulations and generate responses."""
from __future__ import annotations

import os
from timeit import default_timer as timer
from typing import Callable, Dict, List, Optional, TypeVar

from config import Config
from fem.params import ExptParams, FEMParams
from fem.responses import FEMResponses
from model import Response
from model.response import ResponseType
from util import print_i

Parsed = TypeVar("Parsed")


class FEMRunner:
    """Run FEM simulations with an external program and generate responses.

    Args:
        built_model_ext: str, extension of the built model file.
        built_files_dir: str, directory to save any built files in.

    """

    def __init__(
            self, c: Config, name: str,
            build: Callable[[Config, ExptParams, FEMRunner], ExptParams],
            run: Callable[[Config, ExptParams, FEMRunner, int], ExptParams],
            parse: Callable[[Config, ExptParams, FEMRunner], Parsed],
            convert: Callable[
                [Config, Parsed],
                Dict[int, Dict[ResponseType, List[Response]]]],
            built_model_ext: str = None, built_files_dir: Optional[str] = None):
        self.c = c
        self._build = build
        self._run = run
        self._parse = parse
        self._convert = convert
        self.name = name
        self.built_model_ext = built_model_ext
        if built_files_dir is None:
            built_files_dir = os.path.join(
                self.c.generated_dir, f"{self.name}/").lower()
        self.built_files_dir = built_files_dir
        assert self.built_files_dir.endswith("/")

    def run(self, expt_params: ExptParams, run=True, save=True):

        start = timer()
        expt_params = self._build(self.c, expt_params, self)
        print_i(f"FEMRunner: built {self.name} model file(s) in"
                + f" {timer() - start:.2f}s")

        if run:
            for sim_ind, _ in enumerate(expt_params.fem_params):
                start = timer()
                expt_params = self._run(self.c, expt_params, self, sim_ind)
                print_i(f"FEMRunner: ran {self.name}"
                        + f" {sim_ind + 1}/{len(expt_params.fem_params)}"
                        + f" simulation in {timer() - start:.2f}s")

        if not save:
            return

        start = timer()
        parsed_by_type = self._parse(self.c, expt_params, self)
        print_i(f"FEMRunner: parsed all responses in"
                + f" {timer() - start:.2f}s")

        start = timer()
        sim_responses = self._convert(self.c, parsed_by_type)
        print_i(f"FEMRunner: converted all responses to [Response] in"
                + f" {timer() - start:.2f}s")

        for sim in sim_responses:
            for response_type, responses in sim_responses[sim].items():
                fem_responses = FEMResponses(
                    c=self.c, fem_params=expt_params.fem_params[sim],
                    runner_name=self.name, response_type=response_type,
                    responses=responses, skip_build=True)

                start = timer()
                fem_responses.save(self.c)
                print_i(f"FEMRunner: saved simulation {sim + 1} FEMResponses"
                        + f" in ([Response]) in {timer() - start:.2f}s,"
                        + f"({response_type})")

    def fem_file_path(
            self, fem_params: FEMParams, ext: Optional[str] = None) -> str:
        """A file path based on a FEMParams and this FEMRunner .

        Args:
            fem_params: FEMParams, parameters for the FEM simulation.
            ext: Optional[str], if None then use fem_runner.built_model_ext,
                else the given file extension is used.

        """
        load_str: str = fem_params.load_str()
        for char in "[]()":
            load_str = load_str.replace(char, "")
        fem_id = f"{self.name}-{load_str}"

        ext = "." + self.built_model_ext if ext is None else ext
        return os.path.join(
            self.built_files_dir, f"{fem_id}{ext}").replace(" ", "").lower()
