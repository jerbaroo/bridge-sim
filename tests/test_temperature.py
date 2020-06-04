from datetime import datetime

from bridge_sim import temperature


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
