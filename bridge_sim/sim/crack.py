from datetime import datetime
from typing import List

import bridge_sim.util
import numpy as np

from bridge_sim.internal.plot import plt
from bridge_sim.model import Config, Point
from bridge_sim.sim.responses import to_traffic_array
from bridge_sim.traffic import load_traffic, normal_traffic
from bridge_sim import temperature
from bridge_sim.util import safe_str


def crack_time_series(
    c: Config,
    traffic_array,
    traffic_array_mins: float,
    sensor: Point,
    crack_frac: float,
    damage,
    temps: List[float],
    solar: List[float],
):
    """Time series of sensor fem, vertical translation and strain XXB.

    Returns a NumPy array of dimensions (2 x len(traffic_array)).

    Args:
        c: Config, global configuration object.
        traffic_array: TrafficArray, traffic flowing over the bridge.
        traffic_array_mins: float, minutes of the the traffic flow.
        sensor: Point, point at which to collect fem.
        crack_frac: float, fraction of time series where crack occurs.
        damage: DamageScenario, scenarios that occurs at crack_frac.
        temps: List[float], list of air temperature, per temperature minute.
        solar: List[float], list of solar radiance, per temperature minute.

    """
    assert 0 <= crack_frac <= 1
    response_types = [ResponseType.YTranslation, ResponseType.Strain]
    half_i = int(len(traffic_array) * crack_frac)
    traffic_array_0, traffic_array_1 = traffic_array[:half_i], traffic_array[half_i:]
    assert len(traffic_array_0) + len(traffic_array_1) == len(traffic_array)

    half_t = int(len(temps) * crack_frac)
    assert len(temps) == len(solar)

    # Get the effect of temperature for both response types and damages.
    # In each case we have the full days worth of temperature fem.
    temp_effect = []
    for response_type in response_types:
        temp_effect_damages = []
        for di, ds in enumerate([HealthyDamage(), damage]):
            bots_tops, new_temp_effect = temperature.effect(
                c=ds.use(c)[0],
                response_type=response_type,
                points=[sensor],
                # One hour temperature data per minute of traffic data.
                len_per_hour=int(len(traffic_array) / traffic_array_mins)
                if di == 0
                else None,
                temps=temps if di == 0 else None,
                solar=solar if di == 0 else None,
                temps_bt=bots_tops.T[int(len(bots_tops.T) / 2) :].T
                if di == 1
                else None,
                ret_temps_bt=True,
            )
            bots_tops = np.array(bots_tops)
            temp_effect_damages.append(
                new_temp_effect[0]
                if di == 1
                else new_temp_effect[0][: int(len(new_temp_effect[0]) / 2)]
            )
        temp_effect.append(np.concatenate(temp_effect_damages))
        print(f"len(temps) = {len(temps)}")
        print(f"len_per_hour = {int(len(traffic_array) / traffic_array_mins)}")
        print(f"Temperature shape = {temp_effect[-1].shape}")
        plt.plot(temp_effect[-1])
        plt.savefig(
            c.get_image_path("crack", safe_str(f"save-temps-{response_type}.pdf"))
        )
        plt.close()

    responses = []
    for ri, rt in enumerate(response_types):
        responses_healthy_cracked = []
        for ds, ta in [(HealthyDamage(), traffic_array_0), (damage, traffic_array_1)]:
            print(
                f"Sections in scenarios scenario = {len(ds.use(c)[0].bridge.sections)}"
            )
            responses_healthy_cracked.append(
                to_traffic_array(
                    config=c,
                    traffic_array=ta,
                    response_type=rt,
                    damage_scenario=ds,
                    points=[sensor],
                ).T[0]
            )  # Responses from a single point.
        responses.append(np.concatenate(responses_healthy_cracked))
        print(f"shape fem without temp = {responses[-1].shape}")
        print(f"shape of temp effect = {temp_effect[ri].shape}")
        if rt == ResponseType.Strain:
            responses[ri] = resize_units("")[0](responses[ri])
        responses[ri] += bridge_sim.util.apply(temp_effect[ri], responses[ri])
    responses = np.array(responses)
    print(f"Responses shape = {responses.shape}")
    return responses


def time_series_plot(c: Config, n: float):
    """Plot 24min time series of cracking, for multiple cracked bridges.

    For each bridge (hard-coded), a time series of strain fem is plotted.
    For each bridge it is initially in healthy condition, and the crack occurs
    halfway through.

    Args:
        n: float, meters in front of the crack zone where to place sensor.

    """

    # First construct one day (24 minutes) of traffic.
    total_mins = 24
    total_seconds = total_mins * 60
    traffic_scenario = normal_traffic(c=c, lam=5, min_d=2)
    traffic_sequence, traffic, traffic_array = load_traffic(
        c=c, traffic_scenario=traffic_scenario, max_time=total_seconds,
    )
    traffic_array.shape

    # Temperatures for one day.
    temps_day = temperature.from_to_mins(
        temperature.load("holly-springs"),
        datetime.fromisoformat(f"2019-07-03T00:00"),
        datetime.fromisoformat(f"2019-07-03T23:59"),
    )
    print(f"len temps = {len(temps_day['solar'])}")
    print(f"len temps = {len(temps_day['temp'])}")

    # Then generate some cracking time series.
    damages = [
        HealthyDamage(),
        transverse_crack(),
        transverse_crack(length=14.0, at_x=48.0),
    ]
    sensors = [
        Point(x=52, z=-8.4),  # Sensor in middle of lane.
        Point(
            x=damages[1].crack_area(c.bridge)[0] - n, z=-8.4
        ),  # Sensor in front of crack zone.
        Point(
            x=damages[2].crack_area(c.bridge)[0] - n, z=-8.4
        ),  # Sensor in front of crack zone.
    ]
    [print(f"Sensor {i} = {sensors[i]}") for i in range(len(sensors))]
    time_series = [
        crack_time_series(
            c=c,
            traffic_array=traffic_array,
            traffic_array_mins=total_mins,
            sensor=sensor,
            crack_frac=0.5,
            damage=damage,
            temps=temps_day["temp"],
            solar=temps_day["solar"],
        )
        for damage, sensor in zip(damages, sensors)
    ]
    plt.portrait()
    for i, (y_trans, strain) in enumerate(time_series):
        x = np.arange(len(strain)) * c.sensor_freq / 60
        x_m = sensors[i].x
        damage_str = "Healthy Bridge"
        if i == 1:
            damage_str = "0.5 m crack zone"
        if i == 2:
            damage_str = "14 m crack zone"
        plt.subplot(len(time_series), 2, i * 2 + 1)
        plt.plot(x, y_trans * 1000, color="tab:blue")
        if i < len(time_series) - 1:
            plt.tick_params(axis="x", bottom=False, labelbottom=False)
        else:
            plt.xlabel("Hours")
        plt.title(f"At x = {x_m} m\n{damage_str}")
        plt.ylabel("Y trans. (mm)")

        plt.subplot(len(time_series), 2, i * 2 + 2)
        plt.plot(x, strain * 1e6, color="tab:orange")
        if i < len(time_series) - 1:
            plt.tick_params(axis="x", bottom=False, labelbottom=False)
        else:
            plt.xlabel("Hours")
        plt.title(f"At x = {x_m} m,\n{damage_str}")
        plt.ylabel("Microstrain XXB")
    plt.tight_layout()
    plt.savefig(c.get_image_path("crack", "time-series-q5.pdf"))
    plt.close()
