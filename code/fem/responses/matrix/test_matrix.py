"""Test that response matrices are loaded correctly."""
import os
from timeit import default_timer as timer

from fem.responses.matrix.dc import DCMatrix
from fem.responses.matrix.il import ILMatrix
from fem.run.opensees import OSRunner
from model.bridge.bridge_705 import bridge_705_2d, bridge_705_test_config
from model.response import ResponseType
from util import print_d

# TODO: Very bad test!

# Print debug information for this file.
D: bool = False

c = bridge_705_test_config(bridge_705_2d)


def clean():
    c.il_matrices = dict()


def test_os_il_matrix():
    return
    # Setup.
    response_type = ResponseType.XTranslation
    fem_runner = OSRunner(c)

    # Remove file first.
    clean()
    assert not os.path.exists(path)

    # Test time for one simulation.
    start = timer()
    ILMatrix.load(
        c=c, response_type=response_type, fem_runner=fem_runner, num_loads=1,
        save_all=False)
    time = timer() - start
    assert 0.1 < time < 2

    # Test file is created.
    assert os.path.exists(path)

    # Test time for saving all responses.
    clean()
    start = timer()
    ILMatrix.load(c, response_type, fem_runner, num_loads=1, save_all=True)
    time = timer() - start
    assert 0.5 < time < 4


def test_os_dc_matrices():
    return
    # Setup.
    fem_runner = OSRunner(c)
    response_type = ResponseType.XTranslation

    # Remove all response files.
    dc_matrix = DCMatrix.load(c, response_type, fem_runner, save_all=False)
    [os.remove(filepath) for filepath in dc_matrix.filepaths()]

    # Test time for one simulation.
    start = timer()
    dc_matrix = DCMatrix.load(c, response_type, fem_runner, save_all=False)
    time = timer() - start
    print_d(D, time)
    # TODO: Fix timing and assertion.
    # assert 1 < time and time < 3


def test_load_all_os_matrices():
    return
    c.il_matrices = dict()
    # Should run fast after the first time (may also be fast).
    # The second time should only require loading from disk.
    ILMatrix.load(c, ResponseType.Strain, OSRunner(c), num_loads=10)
    c.il_matrices = dict()
    start = timer()
    ILMatrix.load(c, ResponseType.Strain, OSRunner(c), num_loads=10)
    time = timer() - start
    assert 1 < time < 4
