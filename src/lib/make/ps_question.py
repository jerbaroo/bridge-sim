import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import model, sim, temperature, traffic, plot, util
from bridge_sim.model import Config
from bridge_sim.plot.util import equal_lims


def plot_year_effects(config: Config, x: float, z: float, num_years: int):
    """Plot all effects over a single year and 100 years at a point."""
    install_day = 37
    year = 2018
    weather = temperature.load("holly-springs-18")
    _0, _1, traffic_array = traffic.load_traffic(
        config, traffic.normal_traffic(config), 60 * 5
    )
    (
        ll_responses,
        ps_responses,
        temp_responses,
        shrinkage_responses,
        creep_responses,
    ) = np.repeat(None, 5)
    start_day, end_day = None, None

    def set_responses(n):
        nonlocal weather, start_day, end_day
        weather["temp"] = temperature.resize(weather["temp"], year=year)
        weather = temperature.repeat(weather, n)
        start_date, end_date = (
            weather["datetime"].iloc[0].strftime(temperature.f_string),
            weather["datetime"].iloc[-1].strftime(temperature.f_string),
        )
        start_day, end_day = install_day, 365 * n
        nonlocal ll_responses, ps_responses, temp_responses, shrinkage_responses, creep_responses
        (
            ll_responses,
            ps_responses,
            temp_responses,
            shrinkage_responses,
            creep_responses,
        ) = sim.responses.to(
            config=config,
            points=[model.Point(x=x, z=z)],
            traffic_array=traffic_array,
            response_type=model.RT.YTrans,
            with_creep=True,
            weather=weather,
            start_date=start_date,
            end_date=end_date,
            install_day=install_day,
            start_day=start_day,
            end_day=end_day,
            ret_all=True,
        )

    # from sklearn.decomposition import FastICA, PCA
    # ica = FastICA(n_components=3)
    # try_ = ica.fit_transform((ll_responses + temp_responses + creep_responses + shrinkage_responses).T)
    # plt.plot(try_)
    # plt.show()

    plt.landscape()
    lw = 2

    def legend():
        leg = plt.legend(
            facecolor="white",
            loc="upper right",
            framealpha=1,
            fancybox=False,
            borderaxespad=0,
        )
        for legobj in leg.legendHandles:
            legobj.set_linewidth(lw)

    plt.subplot(1, 2, 1)
    set_responses(1)
    xax = np.interp(
        np.arange(len(traffic_array)), [0, len(traffic_array) - 1], [start_day, end_day]
    )
    plt.plot(xax, ll_responses[0] * 1e3, c="green", label="traffic", lw=lw)
    plt.plot(xax, temp_responses[0] * 1e3, c="red", label="temperature")
    plt.plot(xax, shrinkage_responses[0] * 1e3, c="blue", label="shrinkage", lw=lw)
    plt.plot(xax, creep_responses[0] * 1e3, c="black", label="creep", lw=lw)
    legend()
    plt.ylabel("Y translation (mm)")
    plt.xlabel("Time (days)")

    plt.subplot(1, 2, 2)
    end_day = 365 * num_years
    set_responses(num_years)
    xax = (
        np.interp(
            np.arange(len(traffic_array)),
            [0, len(traffic_array) - 1],
            [start_day, end_day],
        )
        / 365
    )
    plt.plot(xax, ll_responses[0] * 1e3, c="green", label="traffic", lw=lw)
    plt.plot(xax, temp_responses[0] * 1e3, c="red", label="temperature")
    plt.plot(xax, shrinkage_responses[0] * 1e3, c="blue", label="shrinkage", lw=lw)
    plt.plot(xax, creep_responses[0] * 1e3, c="black", label="creep", lw=lw)
    legend()
    plt.ylabel("Y translation (mm)")
    plt.xlabel("Time (years)")

    equal_lims("y", 1, 2)
    plt.suptitle(f"Y translation at X = {x} m, Z = {z} m")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(config.get_image_path("classify/ps", "year-effect.png"))


def plot_sensor_placement(config: Config, num_years: int):
    all_points = [
        model.Point(x=x, z=z)
        for x in np.linspace(config.bridge.x_min, config.bridge.x_max, 300)
        for z in np.linspace(config.bridge.z_min, config.bridge.z_max, 100)
    ]
    response_type = model.ResponseType.YTrans
    install_day = 37
    year = 2018
    weather = temperature.load("holly-springs-18")
    config.sensor_freq = 1
    _0, _1, traffic_array = traffic.load_traffic(
        config, traffic.normal_traffic(config), 10
    )
    weather["temp"] = temperature.resize(weather["temp"], year=year)
    weather = temperature.repeat(weather, num_years)
    start_date, end_date = (
        weather["datetime"].iloc[0].strftime(temperature.f_string),
        weather["datetime"].iloc[-1].strftime(temperature.f_string),
    )
    start_day, end_day = install_day, 365 * num_years
    for pier in [9]:
        pier_centre = model.Point(
            x=config.bridge.supports[pier].x, z=config.bridge.supports[pier].z,
        )
        points = [p for p in all_points if pier_centre.distance(p) < 7]
        ps = model.PierSettlement(pier=pier, settlement=5 / 1e3)
        (
            _0,
            _1,
            temp_responses,
            shrinkage_responses,
            creep_responses,
        ) = sim.responses.to(
            config=config,
            points=points,
            traffic_array=traffic_array,
            response_type=response_type,
            with_creep=True,
            weather=weather,
            start_date=start_date,
            end_date=end_date,
            install_day=install_day,
            start_day=start_day,
            end_day=end_day,
            ret_all=True,
        )
        ps_responses = sim.responses.to_pier_settlement(
            config=config,
            points=points,
            responses_array=_0,
            response_type=response_type,
            pier_settlement=[(ps, ps)],
        ).T[-1]
        ps_responses += sim.responses.to_creep(
            config=config,
            points=points,
            responses_array=_0,
            response_type=response_type,
            pier_settlement=[(ps, ps)],
            install_pier_settlement=[ps],
            install_day=install_day,
            start_day=start_day,
            end_day=end_day,
        ).T[-1]
        long_term_responses = (
            temp_responses.T[-1] + shrinkage_responses.T[-1] + creep_responses.T[-1]
        )

        ############
        # Plotting #
        ############

        plt.landscape()
        plt.subplot(3, 1, 1)
        responses = sim.model.Responses(
            response_type=response_type,
            responses=list(zip(abs(long_term_responses) * 1e3, points)),
        )
        plot.contour_responses(config, responses, levels=30, interp=(200, 60))
        plot.top_view_bridge(config.bridge, piers=True)

        plt.subplot(3, 1, 2)
        responses = sim.model.Responses(
            response_type=response_type,
            responses=list(zip(abs(ps_responses) * 1e3, points)),
        )
        plot.contour_responses(config, responses, levels=30, interp=(200, 60))
        plot.top_view_bridge(config.bridge, piers=True)

        plt.subplot(3, 1, 3)
        responses = sim.model.Responses(
            response_type=response_type,
            responses=list(
                zip((abs(ps_responses) - abs(long_term_responses)) * 1e3, points)
            ),
        )
        plot.contour_responses(config, responses, levels=30, interp=(200, 60))
        plot.top_view_bridge(config.bridge, piers=True)

    plt.savefig(config.get_image_path("classify/ps", "placement.pdf"))


def plot_removal(config: Config, x: float, z: float):
    response_type = model.RT.YTrans
    weather = temperature.load("holly-springs-18")
    weather["temp"] = temperature.resize(weather["temp"], year=2018)
    start_date, end_date = (
        weather["datetime"].iloc[0].strftime(temperature.f_string),
        weather["datetime"].iloc[-1].strftime(temperature.f_string),
    )
    install_day = 37
    start_day, end_day = install_day, install_day + 365
    _0, _1, traffic_array = traffic.load_traffic(config, traffic.normal_traffic(config), time=60)
    responses = sim.responses.to(
        config=config,
        points=[model.Point(x=x, z=z)],
        traffic_array=traffic_array,
        response_type=response_type,
        with_creep=True,
        weather=weather,
        start_date=start_date,
        end_date=end_date,
        install_day=install_day,
        start_day=start_day,
        end_day=end_day,
        # ret_all=True,
    )[0] * 1e3

    def legend():
        return plt.legend(
            facecolor="white",
            loc="upper right",
            framealpha=1,
            fancybox=False,
            borderaxespad=0,
        )

    plt.landscape()
    plt.subplot(2, 2, 1)
    xax = np.interp(np.arange(len(weather)), [0, len(weather) - 1], [start_day, end_day])
    plt.plot(xax, weather["temp"], c="red")
    plt.ylabel("Temperature °C")
    plt.xlabel("Days since T_0")
    plt.title("Temperature in 2018")

    plt.subplot(2, 2, 2)
    xax = np.interp(np.arange(len(responses)), [0, len(responses) - 1], [start_day, end_day])
    plt.plot(xax, responses)
    plt.ylabel("Y translation (mm)")
    plt.xlabel("Days since T_0")
    plt.title("Y translation in 2018")

    plt.subplot(2, 2, 3)
    num_samples = 365 * 24
    temps = util.apply(weather["temp"], np.arange(num_samples))
    rs = util.apply(responses, np.arange(num_samples))
    lr, _ = temperature.regress_and_errors(temps, rs)
    lr_x = np.linspace(min(temps), max(temps), 100)
    y = lr.predict(lr_x.reshape((-1, 1)))
    plt.plot(lr_x, y, lw=2, c="red", label="linear fit")
    plt.scatter(temps, rs, s=2, alpha=0.5, label="hourly samples")
    leg = legend()
    leg.legendHandles[1]._sizes = [30]
    plt.ylabel("Y translation (mm)")
    plt.xlabel("Temperature °C")
    plt.title("Linear model from 2018 data")

    #############
    # 2019 data #
    #############

    weather_2019 = temperature.load("holly-springs")
    weather_2019["temp"] = temperature.resize(weather_2019["temp"], year=2019)
    start_date, end_date = (
        weather_2019["datetime"].iloc[0].strftime(temperature.f_string),
        weather_2019["datetime"].iloc[-1].strftime(temperature.f_string),
    )
    start_day, end_day = install_day + 365, install_day + (2 * 365)
    responses_2019 = sim.responses.to(
        config=config,
        points=[model.Point(x=x, z=z)],
        traffic_array=traffic_array,
        response_type=response_type,
        with_creep=True,
        weather=weather_2019,
        start_date=start_date,
        end_date=end_date,
        install_day=install_day,
        start_day=start_day,
        end_day=end_day,
    )[0] * 1e3

    plt.subplot(2, 2, 4)
    xax_responses = np.interp(np.arange(len(responses_2019)), [0, len(responses_2019) - 1], [start_day, end_day])
    plt.plot(xax_responses, responses_2019, label="2019 responses")
    temps_2019 = util.apply(weather_2019["temp"], xax_responses)
    y = lr.predict(temps_2019.reshape((-1, 1)))
    plt.plot(xax_responses, y, label="prediction")
    plt.ylabel("Y translation (mm)")
    plt.xlabel("Days since T_0")
    plt.title("Y translation in 2019")
    for legobj in legend().legendHandles:
        legobj.set_linewidth(2.0)

    plt.suptitle(f"Predicting effect from temperature at X = {x} m, Z = {z} m")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(config.get_image_path("classify/ps", "regress.pdf"))

