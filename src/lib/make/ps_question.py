import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import model, sim, temperature, traffic
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
