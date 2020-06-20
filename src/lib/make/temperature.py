from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import temperature
from bridge_sim.model import Config, Point, ResponseType
from bridge_sim.sim.model import Responses
from bridge_sim.util import plot_hours, print_i, safe_str
from bridge_sim.plot import contour_responses, top_view_bridge
from bridge_sim.plot.util import equal_lims


def temp_contour_plot(c: Config, temp_bottom: float, temp_top: float):
    """Contour plot of responses for a temperature profile."""
    # Points on the deck to collect fem.
    deck_points = [
        Point(x=x, y=0, z=z)
        for x in np.linspace(
            c.bridge.x_min, c.bridge.x_max, num=int(c.bridge.length * 2)
        )
        for z in np.linspace(
            c.bridge.z_min, c.bridge.z_max, num=int(c.bridge.width * 2)
        )
    ]

    def plot_response_type(response_type: ResponseType):
        # Temperature effect.
        temp_effect = temperature.effect(
            config=c,
            response_type=response_type,
            points=deck_points,
            temps_bt=([temp_bottom], [temp_top]),
        ).T[0]
        print_i(f"temp shape = {temp_effect.shape}")
        responses = Responses(
            response_type=response_type,
            responses=[
                (temp_effect[p_ind], deck_points[p_ind])
                for p_ind in range(len(deck_points))
            ],
        ).without_nan_inf()
        if response_type.is_strain():
            responses = responses.map(lambda r: r * 1e6)
        else:
            responses.units = "mm"
            responses = responses.map(lambda r: r * 1e3)
        top_view_bridge(c.bridge, abutments=True, piers=True, units="m")
        contour_responses(config=c, responses=responses)
        plt.title(
            "Microstrain XXB" if response_type.is_strain() else response_type.name()
        )

    plt.landscape()
    plt.subplot(2, 1, 1)
    plot_response_type(ResponseType.YTrans)
    plt.subplot(2, 1, 2)
    plot_response_type(ResponseType.StrainXXB)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.suptitle(
        f"T_REF, T_bot, T_top = {c.bridge.ref_temp_c} °C, {temp_bottom} °C, {temp_top} °C"
    )
    plt.savefig(
        c.get_image_path(
            "thesis/temperature", safe_str(f"contour-{temp_bottom}-{temp_top}") + ".pdf"
        )
    )
    plt.close()


def temp_profile_plot(c: Config, fname: str):
    """Plot the temperature profile throughout the bridge deck."""
    x, z = 21, -8.4
    # Load weather data.
    weather = temperature.load(name=fname)
    weather["temp"] = temperature.resize(list(weather["temp"]), year=2019)
    # Convert to minutely.
    from_ = datetime.fromisoformat(f"2019-01-01T00:00")
    to = datetime.fromisoformat(f"2019-12-31T23:59")
    temp_year = temperature.from_to_mins(weather, from_, to)
    # Temperature profile.
    temps_year_bottom, temps_year_top = temperature.temp_profile(
        temps=temp_year["temp"], solar=temp_year["solar"],
    )
    # Calculate responses.
    uniform_year_y, linear_year_y, effect_year_y = temperature.effect(
        config=c,
        response_type=ResponseType.YTrans,
        points=[Point(x=x, y=0, z=z)],
        weather=temp_year,
        d=True,
    )
    effect_year_s = temperature.effect(
        config=c,
        response_type=ResponseType.StrainXXB,
        points=[Point(x=x, y=0, z=z)],
        weather=temp_year,
    )

    def legend_lw(leg):
        for legobj in leg.legendHandles:
            legobj.set_linewidth(3.0)

    plt.portrait()
    plt.subplot(3, 2, 1)
    plt.plot(temp_year["datetime"], temps_year_top, label="Top of deck", c="tab:red")
    plt.plot(temp_year["datetime"], temp_year["temp"], label="Air", c="tab:blue")
    plt.plot(
        temp_year["datetime"], temps_year_bottom, label="Bottom of deck", c="tab:orange"
    )
    plt.ylabel("Temperature °C")
    legend_lw(plt.legend(loc="lower right"))
    plt.title("Annual temperature")
    plt.subplot(3, 2, 5)
    plt.plot(temp_year["datetime"], linear_year_y, label="Linear", c="tab:blue")
    plt.plot(temp_year["datetime"], uniform_year_y, label="Uniform", c="tab:orange")
    plt.ylabel("Temperature °C")
    legend_lw(plt.legend(loc="lower right"))
    plt.title("Annual gradient")
    plt.subplot(3, 2, 3)
    plt.scatter(temp_year["datetime"], temp_year["solar"], c="tab:red", s=1)
    plt.ylabel("Solar radiation (W/m²)")
    plt.title("Annual solar radiation")

    from_ = datetime.fromisoformat(f"2019-07-01T00:00")
    to = datetime.fromisoformat(f"2019-07-02T23:59")
    temp_month = temperature.from_to_mins(df=temp_year, from_=from_, to=to)
    # Temperature profile.
    temps_month_bottom, temps_month_top = temperature.temp_profile(
        temps=temp_month["temp"], solar=temp_month["solar"],
    )
    uniform_month_y, linear_month_y, effect_month_y = temperature.effect(
        config=c,
        response_type=ResponseType.YTrans,
        points=[Point(x=x, y=0, z=z)],
        weather=temp_month,
        d=True,
    )

    plt.subplot(3, 2, 2)
    plt.plot(
        temp_month["datetime"], temps_month_top, label="Top of deck", c="tab:red", lw=3
    )
    plt.plot(
        temp_month["datetime"], temp_month["temp"], label="Air", c="tab:blue", lw=3
    )
    plt.plot(
        temp_month["datetime"],
        temps_month_bottom,
        label="Top of deck",
        c="tab:orange",
        lw=3,
    )
    legend_lw(plt.legend(loc="lower right"))
    plt.title("Two day temperature")
    plt.subplot(3, 2, 6)
    plt.plot(temp_month["datetime"], linear_month_y, label="Linear", c="tab:blue", lw=3)
    plt.plot(
        temp_month["datetime"], uniform_month_y, label="Uniform", c="tab:orange", lw=3
    )
    legend_lw(plt.legend(loc="lower right"))
    plt.title("Two day gradient")
    plt.subplot(3, 2, 4)
    plt.scatter(temp_year["datetime"], temp_year["solar"], c="tab:red", s=1)
    plt.title("Two day solar radiation")

    for ps in [(1, 2), (3, 4), (5, 6)]:
        plt.subplot(3, 2, ps[1])
        plt.gca().set_yticklabels([])
        equal_lims("y", 3, 2, ps)

    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(c.get_image_path("thesis/temperature", "profile.pdf"))
    plt.close()


def temperature_effect(config: Config, fname: str):
    weather = temperature.load(name=fname)
    weather["temp"] = temperature.resize(weather["temp"], year=2019)
    print_i(f"Min/max temp = {min(weather['temp'])}, {max(weather['temp'])}")
    print_i(f"Min/max solar = {min(weather['solar'])}, {max(weather['solar'])}")

    # Plot the temperature.
    plt.portrait()
    plt.subplot(4, 1, 1)
    plt.scatter(weather["datetime"], weather["temp"], c="b", s=1)
    plt.ylabel("Temperature (°C)")
    plt.gcf().autofmt_xdate()
    plt.title(f"Temperature from {str(fname[0]).upper()}{fname[1:]}")

    # Plot the temperature in May.
    plt.subplot(4, 1, 2)
    weather_may = temperature.from_to_mins(
        weather,
        from_=datetime.strptime("01/05/19 00:00", "%d/%m/%y %H:%M"),
        to=datetime.strptime("31/05/19 23:59", "%d/%m/%y %H:%M"),
    )
    plot_hours(weather_may)
    plt.scatter(weather_may["datetime"], weather_may["temp"], c="b", s=1)
    plt.ylabel("Temperature (°C)")
    plt.gcf().autofmt_xdate()
    plt.title(f"Temperature in May")

    # Plot the solar radiation.
    plt.subplot(4, 1, 3)
    plt.scatter(weather["datetime"], weather["solar"], c="r", s=1)
    plt.ylabel("Solar radiation")
    plt.gcf().autofmt_xdate()
    plt.title(f"Solar radiation from {str(fname[0]).upper()}{fname[1:]}")

    # Plot the effect at two points.
    plt.subplot(4, 1, 4)
    effect = temperature.effect(
        config=config,
        response_type=ResponseType.StrainXXB,
        points=[Point(x=51)],
        weather=weather,
    )[0]
    plt.scatter(weather["datetime"], effect * 1e6, c="g", s=1)
    plt.ylabel("Microstrain XXB")
    plt.gcf().autofmt_xdate()
    plt.title("Strain at X = 51 in May")
    print_i(f"Effect shape = {effect.shape}")

    # Save.
    plt.tight_layout()
    plt.savefig(config.get_image_path("verification/temperature", f"{fname}.png"))
    plt.close()
