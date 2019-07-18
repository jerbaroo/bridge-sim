"""Test that OpenSees builds model files correctly."""
import os
from timeit import default_timer as timer

from config import bridge_705_config
from fem.responses.il import ILMatrix
from fem.run.opensees import os_runner
from model import *


c = bridge_705_config()
path = os.path.join(c.generated_dir,
    "responses/responses-pa-[(0.00, 1000.00)]-rt-XTranslation-ru-OpenSees.npy")


def clean():
    if os.path.exists(path):
        os.remove(path)
    c.il_matrices = dict()


def test_os_il_matrices():
    # Setup.
    response_type = ResponseType.XTranslation
    fem_runner = os_runner(c)

    # Remove file first.
    clean()
    assert not os.path.exists(path)

    # Test time for one simulation.
    start = timer()
    ILMatrix.load(c, response_type, fem_runner, num_loads=1, save_all=False)
    time = timer() - start
    assert 0.1 < time and time < 1

    # Test file is created.
    assert os.path.exists(path)

    # Test time for saving all responses.
    clean()
    start = timer()
    ILMatrix.load(c, response_type, fem_runner, num_loads=1, save_all=True)
    time = timer() - start
    assert 2 < time and time < 3


def test_load_all_os_matrices():
    c.il_matrices = dict()
    # Should run fast after the first time (may also be fast).
    ILMatrix.load(c, ResponseType.Strain, os_runner(c))
    c.il_matrices = dict()
    start = timer()
    ILMatrix.load(c, ResponseType.Strain, os_runner(c))
    time = timer() - start
    assert 1.5 < time and time < 2.5
