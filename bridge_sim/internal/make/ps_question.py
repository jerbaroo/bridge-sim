import os
from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import model, sim, temperature, traffic, plot, util
from bridge_sim.model import Config, Point, Bridge
from bridge_sim.plot.util import equal_lims
from bridge_sim.sim.responses import without
from bridge_sim.util import print_i, print_w
from bridge_sim.internal.plot import axis_cmap_r


def plot_year_effects(config: Config, x: float, z: float, num_years: int):
    """Plot all effects over a single year and 100 years at a point."""
    install_day = 37
    year = 2018
    weather = temperature.load("holly-springs-18")
    _0, _1, traffic_array = traffic.load_traffic(
        config, traffic.normal_traffic(config), 60 * 10
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
        weather = temperature.repeat(config, "holly-springs-18", weather, n)
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
    plt.savefig(config.get_image_path("classify/ps", f"year-effect-{x}-{z}.png"))


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
    weather = temperature.repeat(config, "holly-springs-18", weather, num_years)
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
    _0, _1, traffic_array = traffic.load_traffic(
        config, traffic.normal_traffic(config), time=60
    )
    responses = (
        sim.responses.to(
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
        )[0]
        * 1e3
    )

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
    xax = np.interp(
        np.arange(len(weather)), [0, len(weather) - 1], [start_day, end_day]
    )
    plt.plot(xax, weather["temp"], c="red")
    plt.ylabel("Temperature °C")
    plt.xlabel("Days since T_0")
    plt.title("Temperature in 2018")

    plt.subplot(2, 2, 2)
    xax = np.interp(
        np.arange(len(responses)), [0, len(responses) - 1], [start_day, end_day]
    )
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
    responses_2019 = (
        sim.responses.to(
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
        )[0]
        * 1e3
    )

    plt.subplot(2, 2, 4)
    xax_responses = np.interp(
        np.arange(len(responses_2019)),
        [0, len(responses_2019) - 1],
        [start_day, end_day],
    )
    plt.plot(xax_responses, responses_2019, label="2019 responses")
    temps_2019 = util.apply(weather_2019["temp"], xax_responses)
    y = lr.predict(temps_2019.reshape((-1, 1)))
    plt.plot(xax_responses, y, label="prediction")
    plt.ylabel("Y translation (mm)")
    plt.xlabel("Days since T_0")
    plt.title("Y translation in 2019")
    for legobj in legend().legendHandles:
        legobj.set_linewidth(2.0)

    plt.suptitle(f"Predicting long-term effect at X = {x} m, Z = {z} m")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(config.get_image_path("classify/ps", "regress.pdf"))


def plot_removal_2(config: Config, x: float, z: float):
    response_type = model.RT.YTrans
    weather_2018 = temperature.load("holly-springs-18")
    weather_2018["temp"] = temperature.resize(weather_2018["temp"], year=2018)
    start_date, end_date = (
        weather_2018["datetime"].iloc[0].strftime(temperature.f_string),
        weather_2018["datetime"].iloc[-1].strftime(temperature.f_string),
    )
    install_day = 37
    start_day, end_day = install_day, install_day + 365
    _0, _1, traffic_array = traffic.load_traffic(
        config, traffic.normal_traffic(config), time=60
    )
    responses_2018 = (
        sim.responses.to(
            config=config,
            points=[model.Point(x=x, z=z)],
            traffic_array=traffic_array,
            response_type=response_type,
            with_creep=True,
            weather=weather_2018,
            start_date=start_date,
            end_date=end_date,
            install_day=install_day,
            start_day=start_day,
            end_day=end_day,
            # ret_all=True,
        )[0]
        * 1e3
    )
    num_samples = 365 * 24
    temps = util.apply(weather_2018["temp"], np.arange(num_samples))
    rs = util.apply(responses_2018, np.arange(num_samples))
    lr, err = temperature.regress_and_errors(temps, rs)

    def legend():
        plt.legend(
            facecolor="white",
            loc="lower left",
            framealpha=1,
            fancybox=False,
            borderaxespad=0,
            labelspacing=0.02,
        )

    ##############################
    # Iterate through each year. #
    ##############################

    plt.landscape()
    weather_2019 = temperature.load("holly-springs")
    weather_2019["temp"] = temperature.resize(weather_2019["temp"], year=2019)
    start_date, end_date = (
        weather_2019["datetime"].iloc[0].strftime(temperature.f_string),
        weather_2019["datetime"].iloc[-1].strftime(temperature.f_string),
    )
    for y_i, year in enumerate([2019, 2024, 2039]):
        plt.subplot(3, 1, y_i + 1)
        start_day = install_day + ((year - 2018) * 365)
        end_day = start_day + 365
        responses_2019 = (
            sim.responses.to(
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
            )[0]
            * 1e3
        )
        # Plot actual values.
        xax = np.interp(
            np.arange(len(responses_2019)), [0, len(responses_2019) - 1], [0, 364]
        )
        plt.plot(xax, responses_2019, label="responses in year", lw=2)
        # Daily prediction.
        xax_responses = np.arange(365)
        temps_2019 = util.apply(weather_2019["temp"], xax_responses)
        y_daily = lr.predict(temps_2019.reshape((-1, 1)))
        y_2_week = [
            np.mean(y_daily[max(0, i - 14) : min(i + 14, len(y_daily))])
            for i in range(len(y_daily))
        ]
        for percentile, alpha in [(100, 20), (75, 40), (50, 60), (25, 100)]:
            err = np.percentile(err, percentile)
            p = percentile / 100
            plt.fill_between(
                xax_responses,
                y_2_week + (err * p),
                y_2_week - (err * p),
                color="orange",
                alpha=alpha / 100,
                label=f"{percentile}% of regression error",
            )
        plt.plot(xax_responses, y_daily, color="black", lw=2, label="daily prediction")
        plt.plot(
            xax_responses, y_2_week, color="red", lw=2, label="2 week sliding window"
        )
        plt.ylabel("Y. trans (mm)")
        plt.title(f"Year {year}")
        if y_i == 0:
            legend()
        if y_i == 2:
            plt.xlabel("Days in year")
        else:
            plt.tick_params("x", bottom=False, labelbottom=False)
    equal_lims("y", 3, 1)
    plt.suptitle(f"Predicting long-term effects at X = {x} m, Z = {z} m")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(config.get_image_path("classify/ps", "regress-2.pdf"))


def plot_removal_3(config: Config, x: float, z: float):
    # First calculate the linear model.
    response_type = model.RT.YTrans
    weather_2018 = temperature.load("holly-springs-18")
    weather_2018["temp"] = temperature.resize(weather_2018["temp"], year=2018)
    start_date, end_date = (
        weather_2018["datetime"].iloc[0].strftime(temperature.f_string),
        weather_2018["datetime"].iloc[-1].strftime(temperature.f_string),
    )
    install_day = 37
    start_day, end_day = install_day, install_day + 365
    _0, _1, traffic_array = traffic.load_traffic(
        config, traffic.normal_traffic(config), time=60
    )
    responses_2018 = (
        sim.responses.to(
            config=config,
            points=[model.Point(x=x, z=z)],
            traffic_array=traffic_array,
            response_type=response_type,
            with_creep=True,
            weather=weather_2018,
            start_date=start_date,
            end_date=end_date,
            install_day=install_day,
            start_day=start_day,
            end_day=end_day,
        )[0]
        * 1e3
    )
    num_samples = 365 * 24
    temps = util.apply(weather_2018["temp"], np.arange(num_samples))
    rs = util.apply(responses_2018, np.arange(num_samples))
    lr, _ = temperature.regress_and_errors(temps, rs)
    # Calculate long-term weather.
    NUM_YEARS = 5
    PIER = 5
    long_weather = deepcopy(weather_2018)
    long_weather["temp"] = temperature.resize(long_weather["temp"], year=2019)
    print_i(f"Repeating {NUM_YEARS} of weather data")
    long_weather = temperature.repeat(
        config, "holly-springs-18", long_weather, NUM_YEARS
    )
    print_i(f"Repeated {NUM_YEARS} of weather data")
    start_date, end_date = (
        long_weather["datetime"].iloc[0].strftime(temperature.f_string),
        long_weather["datetime"].iloc[-1].strftime(temperature.f_string),
    )
    start_day = install_day + 365
    end_day = start_day + 365 * NUM_YEARS
    MAX_PS = 20
    THRESHES = np.arange(0, MAX_PS, 1)
    acc_mat = np.zeros((MAX_PS, len(THRESHES)))
    fp_mat = np.zeros(acc_mat.shape)
    fn_mat = np.zeros(acc_mat.shape)
    tp_mat = np.zeros(acc_mat.shape)
    tn_mat = np.zeros(acc_mat.shape)
    for p_i, ps in enumerate(range(MAX_PS)):
        print_i(f"Using pier settlement = {ps} mm")
        long_responses = sim.responses.to(
            config=config,
            points=[model.Point(x=x, z=z)],
            traffic_array=traffic_array,
            response_type=response_type,
            with_creep=True,
            pier_settlement=[
                (
                    model.PierSettlement(pier=PIER, settlement=0.00001),
                    model.PierSettlement(pier=PIER, settlement=ps / 1e3),
                )
            ],
            install_pier_settlement=[],
            weather=long_weather,
            start_date=start_date,
            end_date=end_date,
            install_day=install_day,
            start_day=start_day,
            end_day=end_day,
            ret_all=False,
            ignore_pier_creep=True,
        )
        healthy_responses = sim.responses.to(
            config=config,
            points=[model.Point(x=x, z=z)],
            traffic_array=traffic_array,
            response_type=response_type,
            with_creep=True,
            pier_settlement=[],
            install_pier_settlement=None,
            weather=long_weather,
            start_date=start_date,
            end_date=end_date,
            install_day=install_day,
            start_day=start_day,
            end_day=end_day,
            ret_all=False,
            ignore_pier_creep=True,
        )
        plt.plot(healthy_responses[0] * 1e3, label="healthy")
        plt.plot(long_responses[0] * 1e3, label="pier settlement")
        plt.legend()
        plt.savefig(config.get_image_path("hello", f"q3-{p_i}.png"))
        plt.close()
        for t_i, thresh in enumerate(THRESHES):
            thresh *= -1
            print(thresh)
            print(max(healthy_responses[0]))
            print(min(healthy_responses[0]))
            print(max(long_responses[0]))
            print(min(long_responses[0]))
            fp = len([x for x in healthy_responses[0] * 1e3 if x <= thresh])
            tp = len([x for x in long_responses[0] * 1e3 if x <= thresh])
            tn = len([x for x in healthy_responses[0] * 1e3 if x > thresh])
            fn = len([x for x in long_responses[0] * 1e3 if x > thresh])
            acc_mat[p_i][t_i] = (tp + tn) / (tp + tn + fp + fn)
            fp_mat[p_i][t_i] = fp
            tp_mat[p_i][t_i] = tp
            fn_mat[p_i][t_i] = fn
            tn_mat[p_i][t_i] = tn

        ##################
        # Save matrices. #
        ##################

        plt.imshow(acc_mat, cmap=axis_cmap_r)
        plt.savefig(config.get_image_path("hello", f"mat.png"))
        plt.close()

        plt.imshow(fp_mat, cmap=axis_cmap_r)
        plt.savefig(config.get_image_path("hello", f"mat-fp.png"))
        plt.close()

        plt.imshow(fn_mat, cmap=axis_cmap_r)
        plt.savefig(config.get_image_path("hello", f"mat-fn.png"))
        plt.close()

        plt.imshow(tp_mat, cmap=axis_cmap_r)
        plt.savefig(config.get_image_path("hello", f"mat-tp.png"))
        plt.close()

        plt.imshow(tn_mat, cmap=axis_cmap_r)
        plt.savefig(config.get_image_path("hello", f"mat-tn.png"))
        plt.close()


def support_with_points(bridge: Bridge, delta_x: float):
    for support in bridge.supports:
        if support.x < bridge.length / 2:
            s_x = support.x - ((support.length / 2) + delta_x)
        else:
            s_x = support.x + ((support.length / 2) + delta_x)
        support.point = Point(x=s_x, z=support.z)
        for support_2 in bridge.supports:
            if support_2.z == support.z and np.isclose(
                support_2.x, bridge.length - support.x
            ):
                support.opposite_support = support_2
        print_w(f"Support sensor at X = {support.point.x}, Z = {support.point.z}")
        if not hasattr(support, "opposite_support"):
            raise ValueError("No opposite support")
    return bridge.supports


def plot_min_diff(config: Config, num_years: int, delta_x: float = 0.5):
    plt.landscape()
    log_path = config.get_image_path("classify/q1", "min-thresh.txt")
    if os.path.exists(log_path):
        os.remove(log_path)
    install_day = 37
    start_day, end_day = install_day, 365 * num_years
    year = 2018
    weather = temperature.load("holly-springs-18")
    _0, _1, traffic_array = traffic.load_traffic(
        config, traffic.normal_traffic(config), 60 * 10
    )
    weather["temp"] = temperature.resize(weather["temp"], year=year)
    # weather = temperature.repeat(config, "holly-springs-18", weather, num_years)
    start_date, end_date = (
        weather["datetime"].iloc[0].strftime(temperature.f_string),
        weather["datetime"].iloc[-1].strftime(temperature.f_string),
    )
    # For each support load the responses to traffic and assign to "Support".
    for s_i, support in enumerate(support_with_points(config.bridge, delta_x=delta_x)):
        support.responses = (
            sim.responses.to_traffic_array(
                config=config,
                points=[support.point],
                traffic_array=traffic_array,
                response_type=model.RT.YTrans,
                # with_creep=True,
                # weather=weather,
                # start_date=start_date,
                # end_date=end_date,
                # install_day=install_day,
                # start_day=start_day,
                # end_day=end_day,
            )[0]
            * 1e3
        )
    # Determine max difference for each sensor pair.
    for s_i, support in enumerate(config.bridge.supports):
        min1, max1 = min(support.responses), max(support.responses)
        min2, max2 = (
            min(support.opposite_support.responses),
            max(support.opposite_support.responses),
        )
        delta_1, delta_2 = abs(min1 - max2), abs(min2 - max1)
        # max_delta = max(abs(support.responses - support.opposite_support.responses))
        support.max_delta = max(delta_1, delta_2)
        to_write = f"Max delta {support.max_delta} for support {s_i}, sensor at X = {support.point.x}, Z = {support.point.z}"
        with open(log_path, "a") as f:
            f.write(to_write)
    # Bridge supports.
    plot.top_view_bridge(config.bridge, lanes=True, piers=True, units="m")
    for s_i, support in enumerate(config.bridge.supports):
        if s_i % 4 == 0:
            support.max_delta = max(
                support.max_delta, config.bridge.supports[s_i + 3].max_delta
            )
        elif s_i % 4 == 1:
            support.max_delta = max(
                support.max_delta, config.bridge.supports[s_i + 1].max_delta
            )
        elif s_i % 4 == 2:
            support.max_delta = max(
                support.max_delta, config.bridge.supports[s_i - 1].max_delta
            )
        elif s_i % 4 == 3:
            support.max_delta = max(
                support.max_delta, config.bridge.supports[s_i - 3].max_delta
            )
        plt.scatter([support.point.x], [support.point.z], c="red")
        plt.annotate(
            f"{np.around(support.max_delta, 2)} mm",
            xy=(support.point.x - 3, support.point.z + 2),
            color="b",
            size="large",
        )
    plt.title("Maximum difference between symmetric sensors")
    plt.tight_layout()
    plt.savefig(config.get_image_path("classify/q1", "min-thresh.pdf"))


def plot_contour_q2(config: Config, num_years: int, delta_x: float = 0.5):
    # Select points: over the deck and the sensors!
    points = [
        Point(x=x, z=z)
        for x in np.linspace(config.bridge.x_min, config.bridge.x_max, 100)
        for z in np.linspace(config.bridge.z_min, config.bridge.z_max, 30)
    ]
    sensor_points = [
        s.point for s in support_with_points(config.bridge, delta_x=delta_x)
    ]
    points += sensor_points
    install_day = 37
    start_day, end_day = install_day, 365 * num_years
    year = 2018
    weather = temperature.load("holly-springs-18")
    # Responses aren't much from traffic, and we are getting the maximum from 4
    # sensors, so short traffic data doesn't really matter.
    _0, _1, traffic_array = traffic.load_traffic(
        config, traffic.normal_traffic(config), 10
    )
    weather["temp"] = temperature.resize(weather["temp"], year=year)
    # weather = temperature.repeat(config, "holly-springs-18", weather, num_years)
    start_date, end_date = (
        weather["datetime"].iloc[0].strftime(temperature.f_string),
        weather["datetime"].iloc[-1].strftime(temperature.f_string),
    )
    # Generate the data!
    responses = (
        sim.responses.to(
            config=config,
            points=points,
            traffic_array=traffic_array,
            response_type=model.RT.YTrans,
            with_creep=True,
            weather=weather,
            start_date=start_date,
            end_date=end_date,
            install_day=install_day,
            start_day=start_day,
            end_day=end_day,
        )
        * 1e3
    )
    # Convert to Responses, determining maximum response per point.
    max_responses = [min(rs) for rs in responses]
    sensor_responses = max_responses[-len(sensor_points) :]
    responses = sim.model.Responses(
        response_type=model.RT.YTrans,
        responses=[(r, p) for r, p in zip(max_responses, points)],
        units="mm",
    ).without(without.edges(config, 2))
    # Adjust maximum responses per sensor so they are symmetric!
    for s_i, support in enumerate(support_with_points(config.bridge, delta_x=delta_x)):
        support.max_response = sensor_responses[s_i]
    for support in support_with_points(config.bridge, delta_x=delta_x):
        support.max_response = min(
            support.max_response, support.opposite_support.max_response
        )
    for s_i, support in enumerate(support_with_points(config.bridge, delta_x=delta_x)):
        if s_i % 4 == 0:
            support.max_response = max(
                support.max_response, config.bridge.supports[s_i + 3].max_response
            )
        elif s_i % 4 == 1:
            support.max_response = max(
                support.max_response, config.bridge.supports[s_i + 1].max_response
            )
        elif s_i % 4 == 2:
            support.max_response = max(
                support.max_response, config.bridge.supports[s_i - 1].max_response
            )
        elif s_i % 4 == 3:
            support.max_response = max(
                support.max_response, config.bridge.supports[s_i - 3].max_response
            )
    plt.landscape()
    plot.contour_responses(config, responses, interp=(200, 60), levels=20)
    plot.top_view_bridge(config.bridge, lanes=True, piers=True, units="m")
    for s_i, support in enumerate(support_with_points(config.bridge, delta_x=delta_x)):
        plt.scatter([support.point.x], [support.point.z], c="black")
        plt.annotate(
            f"{np.around(support.max_response, 2)}",
            xy=(support.point.x - 3, support.point.z + 2),
            color="black",
            size="large",
        )
    plt.title(
        f"Minimum Y translation over {num_years} years \n from traffic, temperature, shrinkage & creep"
    )
    plt.tight_layout()
    plt.savefig(config.get_image_path("classify/q2", "q2-contour.pdf"))
    plt.close()


def plot_min_ps_1(config: Config, num_years: int, delta_x: float = 0.5):
    THRESH = 2  # Pier settlement from question 1.
    plt.landscape()
    log_path = config.get_image_path("classify/q1b", "min-ps.txt")
    if os.path.exists(log_path):  # Start with fresh logfile.
        os.remove(log_path)
    install_day = 37
    start_day, end_day = install_day, 365 * num_years
    year = 2018
    weather = temperature.load("holly-springs-18")
    _0, _1, traffic_array = traffic.load_traffic(
        config, traffic.normal_traffic(config), 60 * 10
    )
    weather["temp"] = temperature.resize(weather["temp"], year=year)
    # weather = temperature.repeat(config, "holly-springs-18", weather, num_years)
    start_date, end_date = (
        weather["datetime"].iloc[0].strftime(temperature.f_string),
        weather["datetime"].iloc[-1].strftime(temperature.f_string),
    )
    # For each support..
    for s_i, support in enumerate(support_with_points(config.bridge, delta_x=delta_x)):
        # ..increase pier settlement until threshold triggered.
        for settlement in np.arange(0, 10, 0.1):
            responses = (
                sim.responses.to(
                    config=config,
                    points=[support.point, support.opposite_support.point],
                    traffic_array=traffic_array,
                    response_type=model.RT.YTrans,
                    with_creep=True,
                    weather=weather,
                    start_date=start_date,
                    end_date=end_date,
                    install_day=install_day,
                    start_day=start_day,
                    end_day=end_day,
                    pier_settlement=[
                        (
                            model.PierSettlement(pier=s_i, settlement=0),
                            model.PierSettlement(pier=s_i, settlement=settlement / 1e3),
                        )
                    ],
                    skip_weather_interp=True,
                )
                * 1e3
            )
            delta = max(abs(responses[0] - responses[1]))
            to_write = f"Max delta {delta} for settlement {settlement} mm for support {s_i}, sensor at X = {support.point.x}, Z = {support.point.z}"
            print_w(to_write)
            # Because of "abs", "delta" will be positive.
            if delta > THRESH:
                break
        # Write the minimum settlement value for this support to a file.
        with open(log_path, "a") as f:
            f.write(to_write)
        # Annotate the support with the minimum settlement value.
        plt.scatter([support.point.x], [support.point.z], c="red")
        plt.annotate(
            f"{np.around(settlement, 2)} mm",
            xy=(support.point.x - 3, support.point.z + 2),
            color="b",
            size="large",
        )
    # Plot the results.
    plot.top_view_bridge(config.bridge, lanes=True, piers=True, units="m")
    plt.title("Minimum pier settlement detected (Question 1B)")
    plt.tight_layout()
    plt.savefig(config.get_image_path("classify/q1b", "q1b-min-ps.pdf"))
    plt.close()


def plot_min_ps_2(config: Config, num_years: int, delta_x: float = 0.5):
    THRESH = 6  # Pier settlement from question 1.
    plt.landscape()
    log_path = config.get_image_path("classify/q2b", "2b-min-ps.txt")
    if os.path.exists(log_path):  # Start with fresh logfile.
        os.remove(log_path)
    install_day = 37
    start_day, end_day = install_day, 365 * num_years
    year = 2018
    weather = temperature.load("holly-springs-18")
    _0, _1, traffic_array = traffic.load_traffic(
        config, traffic.normal_traffic(config), 60 * 10
    )
    weather["temp"] = temperature.resize(weather["temp"], year=year)
    # weather = temperature.repeat(config, "holly-springs-18", weather, num_years)
    start_date, end_date = (
        weather["datetime"].iloc[0].strftime(temperature.f_string),
        weather["datetime"].iloc[-1].strftime(temperature.f_string),
    )
    for s_i, support in enumerate(support_with_points(config.bridge, delta_x=delta_x)):
        # Increase pier settlement until threshold triggered.
        for settlement in np.arange(0, 10, 0.1):
            responses = (
                sim.responses.to(
                    config=config,
                    points=[support.point],
                    traffic_array=traffic_array,
                    response_type=model.RT.YTrans,
                    with_creep=True,
                    weather=weather,
                    start_date=start_date,
                    end_date=end_date,
                    install_day=install_day,
                    start_day=start_day,
                    end_day=end_day,
                    pier_settlement=[
                        (
                            model.PierSettlement(pier=s_i, settlement=0),
                            model.PierSettlement(pier=s_i, settlement=settlement / 1e3),
                        )
                    ],
                    skip_weather_interp=True,
                )
                * 1e3
            )
            # Determine the minimum response for this level of settlement.
            max_r = min(responses[0])
            to_write = f"Min {max_r} for settlement {settlement} mm for support {s_i}, sensor at X = {support.point.x}, Z = {support.point.z}"
            print_w(to_write)
            if max_r < -THRESH:
                break
        # Write the minimum response and settlement for this support to a file.
        with open(log_path, "a") as f:
            f.write(to_write)
        plt.scatter([support.point.x], [support.point.z], c="red")
        plt.annotate(
            f"{np.around(settlement, 2)} mm",
            xy=(support.point.x - 3, support.point.z + 2),
            color="b",
            size="large",
        )
    plot.top_view_bridge(config.bridge, lanes=True, piers=True, units="m")
    plt.title("Minimum pier settlement detected (Question 2B)")
    plt.tight_layout()
    plt.savefig(config.get_image_path("classify/q2b", "q2b-min-ps.pdf"))
