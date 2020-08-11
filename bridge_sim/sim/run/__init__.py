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
import numpy as np
from pathos.multiprocessing import Pool
from multiprocessing import shared_memory

from bridge_sim.model import (
    Bridge,
    Config,
    ResponseType,
    PointLoad,
    PierSettlement,
    Point,
)
from bridge_sim.sim.model import SimParams, SimResponses
from bridge_sim.sim.util import _responses_path
from bridge_sim.util import print_d, print_i, safe_str, shorten_path, print_w

# Print debug information for this file.

D: str = "fem.run"
# D: bool = False

Parsed = TypeVar("Parsed")


class FEMRunner:
    """An interface to run simulations with an external FE program.

    For running simulations and loading responses you probably want the
    higher-level API in 'bridge_sim.sim.responses'.

    NOTE: The FEMRunner class should have no knowledge of any specific FE
    package, this will allow for extending support to additional FE packages.

    Args:
        TODO: document this much better.

    """

    def __init__(
        self,
        name: str,
        supported_response_types: Callable[[Bridge], List[ResponseType]],
        build: Callable[[Config, List[SimParams], FEMRunner], List[SimParams]],
        run: Callable[[Config, List[SimParams], FEMRunner, int], List[SimParams]],
        parse: Callable[[Config, List[SimParams], FEMRunner], Parsed],
        convert: Callable[
            [Config, Parsed], Dict[int, Dict[ResponseType, List["Response"]]]
        ],
    ):
        self.name = name
        self.supported_response_types = supported_response_types
        self._build = build
        self._run = run
        self._parse = parse
        self._convert = convert

    def run(
        self,
        config: Config,
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
        expt_params = self._build(c=config, expt_params=expt_params, fem_runner=self)
        print_i(
            f"FEMRunner: built {self.name} model file(s) in"
            + f" {timer() - start:.2f}s"
        )

        # Running.
        for sim_ind, _ in enumerate(expt_params):
            start = timer()
            try:
                expt_params = self._run(config, expt_params, self, sim_ind)
            except PermissionError as e:
                raise PermissionError(
                    f"{e}\nOn Windows you can try adding the folder containing"
                    f" the '{self.name}' executable to your $PATH to avoid this"
                    " error."
                )
            print_i(
                f"FEMRunner: ran {self.name}"
                + f" {sim_ind + 1}/{len(expt_params)}"
                + f" simulation in {timer() - start:.2f} s"
            )

        # Parsing.
        start = timer()
        parsed_expt_responses = self._parse(config, expt_params, self)
        print_i(
            f"FEMRunner: parsed {self.name} responses in" + f" {timer() - start:.2f} s"
        )
        if return_parsed:
            return parsed_expt_responses
        print(parsed_expt_responses[0].keys())

        # Converting.
        start = timer()
        converted_expt_responses = self._convert(
            c=config,
            expt_params=expt_params,
            parsed_expt_responses=parsed_expt_responses,
        )
        print_i(f"FEMRunner: converted to [Response] in" + f" {timer() - start:.2f} s")
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
                    c=config,
                    sim_params=expt_params[sim_ind],
                    sim_runner=self,
                    response_type=response_type,
                    responses=responses,
                    build=False,
                )

                start = timer()
                fem_responses.save()
                print_i(
                    f"FEMRunner: saved simulation {sim_ind + 1} Responses"
                    + f" ({response_type}) in {timer() - start:.2f} s"
                )

    def sim_model_path(
        self,
        config: Config,
        sim_params: SimParams,
        ext: str,
        append: str = "",
        dirname: Optional[str] = None,
    ) -> str:
        """Deterministic path for a FE model file.

        Args:
            sim_params: simulation parameters.
            ext: filename extension without the dot.
            dirname: directory name, defaults to self.name.
            append: append to the filename (before the extension).

        """
        param_str = sim_params.id_str(config)
        append = append if len(append) == 0 else f"-{append}"
        filename = f"{config.bridge.id_str()}-params={param_str}{append}"
        if dirname is None:
            dirname = self.name
        dirname = safe_str(dirname)
        return shorten_path(
            config, safe_str(config.get_data_path(dirname, filename)) + f".{ext}"
        )

    def sim_out_path(
        self,
        config: Config,
        sim_params: SimParams,
        ext: str,
        dirname: Optional[str] = None,
        append: str = "",
        response_types: List[ResponseType] = [],
    ) -> str:
        """Deterministic path for unprocessed simulation output files.

        Args:
            sim_params: simulation parameters.
            ext: extension of the output file without the dot.
            dirname: directory name of output file. Defaults to FEMRunner.name + "-fem".
            append: append to the filename (before the extension).
            response_types: response types identifying the output file.

        """
        sim_params_copy = deepcopy(sim_params)
        sim_params_copy.response_types = response_types
        # Output files are response type specific, so append to filename.
        append += "".join([rt.name() for rt in response_types])
        if dirname is None:
            dirname = self.name + "-responses"
        return self.sim_model_path(
            config=config,
            sim_params=sim_params_copy,
            ext=ext,
            dirname=dirname,
            append=append,
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

    """
    if response_type not in c.sim_runner.supported_response_types(c.bridge):
        raise ValueError(f"{response_type} not supported by {c.sim_runner.name}")

    prog_str = ""
    if index is not None:
        prog_str = f"{index[0]}/{index[1]}: "
    print_prog = lambda s: print_i(prog_str + s, end="\n" if index is None else "\r")

    path = _responses_path(
        config=c,
        sim_runner=c.sim_runner,
        sim_params=sim_params,
        response_type=response_type,
    )

    # Run the FE simulation if requested.
    if run or not os.path.exists(path):
        print_prog(f"Running simulation")
        c.sim_runner.run(c, [sim_params])
    else:
        print_prog(f"Not running simulation")
    # If only running was requested then we are done.
    if run_only:
        return None

    print_i(f"Loading {response_type.name()} responses from: {path}")
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

    print_prog(f"Loaded {response_type.name()} Responses in {timer() - start:.2f}s")

    start = timer()
    sim_responses = SimResponses(
        c=c,
        sim_params=sim_params,
        sim_runner=c.sim_runner,
        response_type=response_type,
        responses=responses,
    )
    print_prog(f"Indexed {response_type.name()} Responses in {timer() - start:.2f}s")

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
    if not run_only:
        for index_params in indices_and_params:
            yield process(index_params, _run_only=False)


def pier_settlement(
    config: Config,
    response_type: ResponseType = ResponseType.YTrans,
    run_only: bool = False,
):
    """Yield all unit pier settlement simulation responses.

    Set 'config.parallel' before calling this function to run simulations in
    parallel.

    Args:
        config: simulation configuration object.
        response_type: response type of simulations.
        run_only: only run simulations, don't return responses.

    """
    return load_expt_responses(
        c=config,
        expt_params=[
            SimParams(
                pier_settlement=[
                    PierSettlement(pier=pier, settlement=config.unit_pier_settlement)
                ]
            )
            for pier in range(len(config.bridge.supports))
        ],
        response_type=response_type,
        run_only=run_only,
    )


def ulm_xzs(config: Config):
    """Axle positions for unit load simulations."""
    return [
        (x, z)
        for z, x in itertools.product(
            config.bridge.axle_track_zs(), config.bridge.wheel_track_xs(config),
        )
    ]


def ulm_point_loads(config: Config):
    """Point loads for each unit point-load simulation."""
    half_axle = config.axle_width / 2
    return [
        [
            PointLoad(x=x, z=z + half_axle, load=config.il_unit_load),
            PointLoad(x=x, z=z - half_axle, load=config.il_unit_load),
        ]
        for x, z in ulm_xzs(config)
    ]


def point_load(
    config: Config,
    indices: Optional[List[int]] = None,
    response_type: ResponseType = ResponseType.YTrans,
    run_only: bool = False,
):
    """Yield all unit pier point-load simulations responses.

    Set 'config.parallel' before calling this function to run simulations in
    parallel.

    Args:
        config: simulation configuration object.
        indices: only simulations with these indexes, valid indexes are
            [0 .. (wheel_tracks x uls -1)]. Optional, else run all simulations.
        response_type: response type of simulations.
        run_only: only run simulations, don't return responses.

    """
    expt_params = [
        SimParams(ploads=point_loads) for point_loads in ulm_point_loads(config)
    ]
    if indices is not None:
        expt_params = [expt_params[i] for i in indices]
        assert len(expt_params) == len(indices)
        print_i(f"Running {len(indices)} simulations: {indices}")
    return load_expt_responses(
        c=config,
        expt_params=expt_params,
        response_type=response_type,
        run_only=run_only,
    )


def temperature(
    config: Config,
    response_type: ResponseType = ResponseType.YTrans,
    run_only: bool = False,
):
    """Yield all unit temperature simulations responses.

    Set 'config.parallel' before calling this function to run simulations in
    parallel.

    Args:
        config: simulation configuration object.
        response_type: response type of simulations.
        run_only: only run simulations, don't return responses.

    """
    return load_expt_responses(
        c=config,
        expt_params=[
            SimParams(axial_delta_temp=config.unit_axial_delta_temp_c),
            SimParams(moment_delta_temp=config.unit_moment_delta_temp_c),
        ],
        response_type=response_type,
        run_only=run_only,
    )


def ulm_path(config: Config, response_type: ResponseType, points: List[Point]) -> str:
    """Unique path for a unit load matrix."""
    return safe_str(
        config.get_data_path(
            "ulm-path", f"{response_type.value}-{''.join(str(p) for p in points)}"
        )
    )


def load_ulm(config: Config, response_type: ResponseType, points: List[Point]):
    """Return a unit load matrix for some sensors.

    Args:
        config: simulation configuration object.
        response_type: type of sensor responses.
        points: points at which to calculate responses to unit loads.

    Returns: unit load matrix of shape (uls * lanes * 2, len(points)).

    """
    path = shorten_path(
        config,
        ulm_path(config=config, response_type=response_type, points=points),
        bypass_config=True,
    )
    print_i(f"ULM path = {path}")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return dill.load(f)

    point_loads = ulm_point_loads(config)
    shm_template = np.empty((len(point_loads), len(points)))
    shm = shared_memory.SharedMemory(create=True, size=shm_template.nbytes)
    # This try/except is to free shared-memory resources on KeyboardInterrupt.
    try:

        def set_ulm_entry(params):
            i_, pls = params
            assert len(pls) == 2
            existing_shm = shared_memory.SharedMemory(name=shm.name)
            ulm = np.ndarray(
                shm_template.shape, dtype=shm_template.dtype, buffer=existing_shm.buf
            )
            for j, response in enumerate(
                load_fem_responses(
                    c=config,
                    sim_params=SimParams(ploads=pls),
                    response_type=response_type,
                ).at_decks(points)
            ):
                ulm[i_][j] = response
            existing_shm.close()

        params_list = list(enumerate(point_loads))
        if config.parallel <= 1:
            print_w("Not loading ULM in parallel")
            list(map(set_ulm_entry, params_list))
        else:
            print_w(f"Loading ULM with {config.parallel} parallelism")
            with Pool(processes=config.parallel) as pool:
                pool.map(set_ulm_entry, params_list)
        result = np.ndarray(
            shm_template.shape, dtype=shm_template.dtype, buffer=shm.buf
        )
        result = np.array(result, copy=True)
        shm.close()
        shm.unlink()
    except KeyboardInterrupt as e:
        shm.close()
        shm.unlink()
        raise e
    with open(path, "wb") as f:
        dill.dump(result, f)
    return result
