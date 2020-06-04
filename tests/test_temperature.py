from datetime import datetime

from bridge_sim.bridges import bridge_705
from bridge_sim.configs import opensees_default
from bridge_sim import temperature

c = opensees_default(bridge_705(0.5))
c.il_num_loads = 10


def test_resize():
    tmin, tmax = -20, 200
    weather = temperature.load("holly-springs")
    weather["temp"] = temperature.resize(weather["temp"], tmin=tmin, tmax=tmax)
    assert max(weather["temp"]) == tmax
    assert min(weather["temp"]) == tmin


def test_from_to_mins():
    weather = temperature.load("holly-springs")
    from_ = datetime.fromisoformat(f"2019-01-01T00:00")
    to = datetime.fromisoformat(f"2019-01-01T00:59")
    weather = temperature.from_to_mins(weather, from_, to)
    assert len(weather) == 60
