"""Run FEM simulations and generate fem."""
from __future__ import annotations

from copy import deepcopy
from timeit import default_timer as timer
from typing import Callable, Dict, List, TypeVar, Optional

from bridge_sim.model import ResponseType, Bridge
from lib.fem.params import SimParams
from lib.fem.responses import SimResponses
from bridge_sim.util import print_d, print_i, safe_str, shorten_path

# Print debug information for this file.
D: str = "fem.run"
# D: bool = False

Parsed = TypeVar("Parsed")


class FEMRunner:
    """An interface to run simulations with an external FE program .

    NOTE: For running simulations and loading fem you should instead use
    the higher-level 'load_fem_responses' function, or 'load_expt_responses'
    for parallelization.

    Args:
        supported_response_types: Callable[[Bridge], List[ResponseType]], the
            supported response types for a given bridge.

    """

    def __init__(
        self,
        c: "Config",
        name: str,
        exe_path: str,
        supported_response_types: Callable[[Bridge], List[ResponseType]],
        build: Callable[[Config, List[SimParams], FEMRunner], List[SimParams]],
        run: Callable[[Config, List[SimParams], FEMRunner, int], List[SimParams]],
        parse: Callable[[Config, List[SimParams], FEMRunner], Parsed],
        convert: Callable[
            [Config, Parsed], Dict[int, Dict[ResponseType, List[Response]]]
        ],
    ):
        self.c = c
        self.name = name
        self.exe_path = exe_path
        self.supported_response_types = supported_response_types
        self._build = build
        self._run = run
        self._parse = parse
        self._convert = convert

    def run(
        self,
        expt_params: List[SimParams],
        return_parsed: bool = False,
        return_converted: bool = False,
    ):
        """Run multiple simulations and save responses.

        TODO: Change ExptParams to SimParams.

        Args:
            expt_params: ExptParams, parameters for a number of simulations.
            return_parsed: bool, for testing, return parsed fem.
            return_converted: bool, for testing, return converted fem.

        """
        # Building.
        start = timer()
        expt_params = self._build(c=self.c, expt_params=expt_params, fem_runner=self,)
        print_i(
            f"FEMRunner: built {self.name} model file(s) in"
            + f" {timer() - start:.2f}s"
        )

        # Running.
        for sim_ind, _ in enumerate(expt_params):
            start = timer()
            expt_params = self._run(self.c, expt_params, self, sim_ind)
            print_i(
                f"FEMRunner: ran {self.name}"
                + f" {sim_ind + 1}/{len(expt_params)}"
                + f" simulation in {timer() - start:.2f}s"
            )

        # Parsing.
        start = timer()
        parsed_expt_responses = self._parse(self.c, expt_params, self)
        print_i(f"FEMRunner: parsed all fem in" + f" {timer() - start:.2f}s")
        if return_parsed:
            return parsed_expt_responses
        print(parsed_expt_responses[0].keys())

        # Converting.
        start = timer()
        converted_expt_responses = self._convert(
            c=self.c,
            expt_params=expt_params,
            parsed_expt_responses=parsed_expt_responses,
        )
        print_i(
            f"FEMRunner: converted all fem to [Response] in"
            + f" {timer() - start:.2f}s"
        )
        if return_converted:
            return converted_expt_responses
        print(converted_expt_responses[0].keys())

        # Saving.
        for sim_ind in converted_expt_responses:
            print_d(D, f"sim_ind = {sim_ind}")
            for response_type, responses in converted_expt_responses[sim_ind].items():
                print_d(D, f"response_type in converted = {response_type}")
                print(len(responses))
                fem_responses = SimResponses(
                    c=self.c,
                    sim_params=expt_params[sim_ind],
                    sim_runner=self,
                    response_type=response_type,
                    responses=responses,
                    build=False,
                )

                start = timer()
                fem_responses.save()
                print_i(
                    f"FEMRunner: saved simulation {sim_ind + 1} SimResponses"
                    + f" in ([Response]) in {timer() - start:.2f}s,"
                    + f"({response_type})"
                )

    def sim_model_path(
        self,
        sim_params: SimParams,
        ext: str,
        append: str = "",
        dirname: Optional[str] = None,
    ) -> str:
        """Deterministic path for a FE model file.

        :param sim_params: simulation parameters.
        :param ext: extension of the output file without the dot.
        :param dirname: directory name of output file. Defaults to FEMRunner.name.
        :param append: append to the filename (before the extension).
        :return: path for the output file.
        """
        param_str = sim_params.id_str()
        append = append if len(append) == 0 else f"-{append}"
        filename = f"{self.c.bridge.id_str()}-params={param_str}{append}"
        if len(sim_params.refinement_radii) > 0:
            filename += "-refined"
        if dirname is None:
            dirname = self.name
        dirname = safe_str(dirname)
        return shorten_path(
            self.c, safe_str(self.c.get_data_path(dirname, filename)) + f".{ext}"
        )

    def sim_out_path(
        self,
        sim_params: SimParams,
        ext: str,
        dirname: Optional[str] = None,
        append: str = "",
        response_types: List[ResponseType] = [],
    ) -> str:
        """Deterministic path for unprocessed simulation output files.

        :param sim_params: simulation parameters.
        :param ext: extension of the output file without the dot.
        :param dirname: directory name of output file. Defaults to FEMRunner.name + "-fem".
        :param append: append to the filename (before the extension).
        :param response_types: response types identifying the output file.
        :return: path for the output file.
        """
        sim_params_copy = deepcopy(sim_params)
        sim_params_copy.response_types = response_types
        # Output files are response type specific, so append to filename.
        append += "".join([rt.name() for rt in response_types])
        if dirname is None:
            dirname = self.name + "-responses"
        return self.sim_model_path(
            sim_params=sim_params_copy, ext=ext, dirname=dirname, append=append
        )
