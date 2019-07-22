"""Test that Diana builds model files correctly."""
from config import Config, bridge_705_config
from fem.params import ExptParams, FEMParams
from fem.run import fem_file_path
from fem.run.diana.build import build_models
from model import *


def test_mobile_load():
    # Setup.
    c = bridge_705_config()
    response_type = ResponseType.XTranslation
    expt_params = ExptParams([
        FEMParams(
            loads=[Load(x_frac=0, kn=5000, axle_distances=[2, 3])],
            response_types=[response_type]),
        FEMParams(
            loads=[Load(x_frac=0.1, kn=5000, axle_distances=[2, 3])],
            response_types=[response_type]),
        FEMParams(
            loads=[Load(x_frac=0.2, kn=5000, axle_distances=[2, 3])],
            response_types=[response_type])
    ])

    # Run and read.
    build_models(c, expt_params)
    with open(c.di_model_path) as f:
        lines = f.readlines()

    # Test AXFORC.
    assert not any("AXFORC -4000" in line for line in lines)
    assert any("AXFORC -5000" in line for line in lines)

    # Test QUADIM.
    quadim = Load(0, 0).quadim
    assert not any("QUADIM 500 200" in line for line in lines)
    assert any("QUADIM 400 200" in line for line in lines)

    # Test AXWIDT.
    assert not any("AXWIDT 3000" in line for line in lines)
    assert any("AXWIDT 2000" in line for line in lines)

    # Test AXDIST.
    assert not any("AXDIST 3000 2000" in line for line in lines)
    assert any("AXDIST 2000 3000" in line for line in lines)
