"""Parse responses from a Diana simulation."""
from collections import defaultdict
from timeit import default_timer as timer
from typing import List

from config import Config
from fem.params import ExptParams
from fem.run import Parsed
from model import *
from util import *


def parse_translation(c: Config):
    """Parse translation responses as tuples, indexed by simulation timestep.

    NOTE: timestep starts at 0.

    """
    with open(c.di_translation_path) as f:
        lines = f.readlines()
    time = 0
    time_header = True
    data = defaultdict(list)  # Data for each subsequent timestep.
    for line in lines:
        # Need to find beginning of data.
        if time_header:
            if line.strip().startswith("Nodnr"):
                time_header = False
        else:
            nums = line.split()
            # Else parse data if possible.
            if len(nums) == 7:
                line_data = list(map(float, nums))
                data[time].append(line_data)
            # Else beginning of new header.
            else:
                time += 1
                time_header = True
    return data


def parse_strain(c: Config):
    """Parse strain responses as tuples, indexed by simulation timestep.

    NOTE: timestep starts at 0.

    """
    with open(c.di_strain_path) as f:
        lines = f.readlines()
    time = 0
    elmnr = None
    time_header = True
    data = defaultdict(list)  # Data for each subsequent timestep.
    for line in lines:
        # Need to find beginning of data.
        if time_header:
            if line.strip().startswith("Elmnr"):
                time_header = False
        else:
            nums = line.split()
            # Else parse data (with new element number) if possible.
            if len(nums) == 12:
                line_data = list(map(float, nums))
                data[time].append(line_data)
                elmnr = line_data[0]
            # Else parse data if possible.
            elif len(nums) == 11:
                line_data = [elmnr] + list(map(float, nums))
                data[time].append(line_data)
            # Else beginning of new header.
            else:
                time += 1
                time_header = True
    return data


def parse_responses(c: Config, expt_params: ExptParams) -> Parsed:
    """Parse responses from a Diana simulation."""
    if not expt_params.is_mobile_load():
        raise ValueError("Diana: only MOBILE load supported")

    results = dict()

    def parse_type(response_type: ResponseType):
        return response_type in expt_params.fem_params[0].response_types

    if (parse_type(ResponseType.XTranslation)
            or parse_type(ResponseType.YTranslation)):
        start = timer()
        parsed_translation = parse_translation(c)
        print_i(f"Diana: Parsed translation responses in {timer() - start:.2f}s")
        results["translation"] = parsed_translation

    if (parse_type(ResponseType.Strain)):
        start = timer()
        parsed_strain = parse_strain(c)
        print_i(f"Diana: Parsed strain responses in {timer() - start:.2f}s")
        results["strain"] = parsed_strain

    return results
