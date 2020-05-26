"""Low-level API for saving/loading responses from FE simulation.

This API is based on the 'bridge_sim.model.SimParams' class.

"""

from __future__ import annotations

import itertools
import os
from collections import deque
from copy import deepcopy
from timeit import default_timer as timer
from typing import Callable, Dict, List, TypeVar, Optional, Tuple

import dill
from pathos.multiprocessing import Pool

from bridge_sim.model import Bridge, Config, ResponseType
from bridge_sim.sim.model import SimParams, SimResponses
from bridge_sim.sim.util import _responses_path
from bridge_sim.util import print_d, print_i, safe_str, shorten_path

# Print debug information for this file.

D: str = "fem.run"
# D: bool = False

Parsed = TypeVar("Parsed")


class FEMRunner:
    """An interface to run simulations with an external FE program.

    NOTE: For running simulations and loading fem you probably want the
    higher-level API in 'bridge_sim.sim.responses'.

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


def load_fem_responses(
    c: Config,
    sim_params: SimParams,
    response_type: ResponseType,
    run: bool = False,
    run_only: bool = False,
    index: Optional[Tuple[int, int]] = None,
) -> "FEMResponses":
    """Load responses of one sensor type from a FE simulation.

    This function is a layer over 'FEMRunner.run' and additionally handles
    saving/loading results to/from disk -- only running the simulation if
    necessary.

    Args:
        c: simulation configuration object.
        sim_params: simulation parameters.
        response_type: responses to load from disk and return.
        run: run the simulation even if results are already saved.
        run_only: don't bother returning results
        index: simulation progress (n/m) printed if given.

    NOTE: Note-to-self. This function is NOT to take a DamageScenario. The whole
    'fem' module of this package should be separate from that abstraction.

    """
    if response_type not in c.sim_runner.supported_response_types(c.bridge):
        raise ValueError(f"{response_type} not supported by FEMRunner")

    prog_str = "1/1: "
    if index is not None:
        prog_str = f"{index[0]}/{index[1]}: "
    print_prog = lambda s: print_i(prog_str + s, end="\r")

    path = _responses_path(
        sim_runner=c.sim_runner, sim_params=sim_params, response_type=response_type,
    )
    print_i(f"Loading responses from: {path}")

    # Run the FEM simulation, and/or clean build artefacts, if requested.
    if run or not os.path.exists(path):
        print_prog(f"Running simulation")
        c.sim_runner.run([sim_params])
    else:
        print_prog(f"Not running simulation")
    # If only running was requested then we are done.
    if run_only:
        return None

    start = timer()
    try:
        with open(path, "rb") as f:
            responses = dill.load(f)
    # Try again on Exception.
    except Exception as e:
        print_i(f"\n{str(e)}\nremoving and re-running sim. {index} at {path}")
        os.remove(path)
        return load_fem_responses(
            c=c,
            sim_params=sim_params,
            response_type=response_type,
            run=run,
            run_only=run_only,
            index=index,
        )

    print_prog(f"Loaded Responses in {timer() - start:.2f}s, ({response_type})")

    start = timer()
    sim_responses = SimResponses(
        c=c,
        sim_params=sim_params,
        sim_runner=c.sim_runner,
        response_type=response_type,
        responses=responses,
    )
    print_prog(f"Built FEMResponses in {timer() - start:.2f}s, ({response_type})")

    return sim_responses


def load_expt_responses(
    c: Config,
    expt_params: List[SimParams],
    response_type: ResponseType,
    run_only: bool = False,
) -> List[SimResponses]:
    """Save/load responses of one sensor type for multiple simulations.

    The simulations will be run in parallel if 'Config.parallel > 1'. If the
    'run_only' option is passed, then the simulations will run but nothing will
    be returned.

    """
    indices_and_params = list(zip(itertools.count(), expt_params))

    def process(index_and_params, _run_only: bool = True):
        i, sim_params = index_and_params
        return load_fem_responses(
            c=deepcopy(c),
            sim_params=deepcopy(sim_params),
            response_type=response_type,
            run_only=_run_only,
            index=(i + 1, len(expt_params)),
        )

    # First run the simulations (if necessary), in parallel if requested. To
    # free resources as quickly as possible only 1 task is run per process.
    if c.parallel > 1:
        print(f"Running in parallel")
        with Pool(processes=c.parallel, maxtasksperchild=1) as pool:
            pool.map(process, indices_and_params)
    else:
        deque(map(process, indices_and_params), maxlen=0)
    # Return after generating results if requested...
    if run_only:
        return
    # ...otherwise yield all of the results.
    for index_params in indices_and_params:
        yield process(index_params, _run_only=False)
