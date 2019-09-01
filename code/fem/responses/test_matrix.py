"""Test that OpenSees builds model files correctly."""
import os
from timeit import default_timer as timer

from fem.responses.matrix import DCMatrix, load_il_matrix
from fem.run.opensees import os_runner
from model.bridge.bridge_705 import bridge_705_config
from model.response import ResponseType
from util import print_d

# TODO: This is a very bad test.

c = bridge_705_config()
path = os.path.join(c.generated_dir,
    "responses/responses-pa-[(0.00, 1000.00)]-rt-XTranslation-ru-OpenSees.npy")


def clean():
    if os.path.exists(path):
        os.remove(path)
    c.il_matrices = dict()


def test_os_il_matrix():
    # Setup.
    response_type = ResponseType.XTranslation
    fem_runner = os_runner(c)

    # Remove file first.
    clean()
    assert not os.path.exists(path)

    # Test time for one simulation.
    start = timer()
    load_il_matrix(
        c=c, response_type=response_type, fem_runner=fem_runner, num_loads=1,
        save_all=False)
    time = timer() - start
    assert 0.1 < time and time < 2

    # Test file is created.
    assert os.path.exists(path)

    # Test time for saving all responses.
    clean()
    start = timer()
    ILMatrix.load(c, response_type, fem_runner, num_loads=1, save_all=True)
    time = timer() - start
    assert 0.5 < time and time < 4



def test_os_dc_matrices():
    # Setup.
    fem_runner = os_runner(c)
    response_type = ResponseType.XTranslation

    # Remove all response files.
    dc_matrix = DCMatrix.load(c, response_type, fem_runner, save_all=False)
    [os.remove(filepath) for filepath in dc_matrix.filepaths()]

    # Test time for one simulation.
    start = timer()
    dc_matrix = DCMatrix.load(c, response_type, fem_runner, save_all=False)
    time = timer() - start
    print_d(time)
    # TODO: Fix timing and assertion.
    # assert 1 < time and time < 3


def test_load_all_os_matrices():
    c.il_matrices = dict()
    # Should run fast after the first time (may also be fast).
    # The second time should only require loading from disk.
    ILMatrix.load(c, ResponseType.Strain, os_runner(c), num_loads=10)
    c.il_matrices = dict()
    start = timer()
    ILMatrix.load(c, ResponseType.Strain, os_runner(c), num_loads=10)
    time = timer() - start
    assert 1 < time and time < 4


if __name__ == "__main__":
    test_os_dc_matrices()
