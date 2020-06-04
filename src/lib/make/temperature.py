from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import temperature
from bridge_sim.model import Config, Point, ResponseType
from bridge_sim.util import plot_hours, print_i


def temp_contour_plot(c: Config, temp_bottom: int, temp_top: int):
    """Plot the effect of temperature at a given temperature."""
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
            c=c,
            response_type=response_type,
            points=deck_points,
            temps_bt=([temp_bottom], [temp_top]),
        ).T[0]
        responses = Responses(
            response_type=response_type,
            responses=[
                (temp_effect[p_ind], deck_points[p_ind])
                for p_ind in range(len(deck_points))
            ],
            units=units,
        )
        top_view_bridge(c.bridge, compass=False, lane_fill=False, piers=True)
        plot_contour_deck(
            c=c,
            responses=responses,
            decimals=6 if response_type == ResponseType.Strain else 2,
            loc="upper right",
        )
        plt.title(
            f"{response_type.name()} when Tref,Tb,Tt = {c.bridge.ref_temp_c}°C,{temp_bottom}°C,{temp_top}°C"
        )

    plt.landscape()
    plt.subplot(2, 1, 1)
    plot_response_type(ResponseType.YTranslation)
    plt.subplot(2, 1, 2)
    plot_response_type(ResponseType.Strain)
    plt.tight_layout()
    plt.savefig(
        c.get_image_path("classify", f"temp-effect-{temp_bottom}-{temp_top}.pdf")
    )
    plt.close()


def temp_gradient_plot(c: Config, date: str):
    """Plot the temperature gradient throughout the bridge deck."""
    temp_loaded = temperature.load(name=date)
    from_ = datetime.fromisoformat(f"2019-01-01T00:00")
    to = datetime.fromisoformat(f"2019-12-31T23:59")
    temp_year = temperature.from_to_mins(temp_loaded, from_, to)
    from_ = datetime.fromisoformat(f"2019-07-01T00:00")
    to = datetime.fromisoformat(f"2019-07-02T23:59")
    temps_year = temperature.resize(list(temp_year["temp"]))
    solar_year = temp_year["solar"]
    dates_year = temp_year["datetime"]
    temps_year_bottom, temps_year_top = temperature.temps_bottom_top(
        c=c, temps=temps_year, solar=solar_year, len_per_hour=60
    )
    x, z = 21, -8.4
    uniform_year_y, linear_year_y, effect_year_y = temperature.effect(
        c=c,
        response_type=ResponseType.YTranslation,
        points=[Point(x=x, y=0, z=z)],
        temps=temps_year,
        solar=solar_year,
        len_per_hour=60,
        d=True,
    )
    uniform_year_s, linear_year_s, effect_year_s = temperature.effect(
        c=c,
        response_type=ResponseType.Strain,
        points=[Point(x=x, y=0, z=z)],
        temps=temps_year,
        solar=solar_year,
        len_per_hour=60,
        d=True,
    )

    plt.portrait()
    plt.subplot(3, 2, 1)
    plt.plot(dates_year, temps_year_top, label="Top of deck")
    plt.plot(dates_year, temps_year, label="Air")
    plt.plot(dates_year, temps_year_bottom, label="Bottom of deck")
    plt.ylabel("Temperature °C ")
    plt.legend(loc="lower right")
    plt.title("Annual temperature")
    plt.subplot(3, 2, 5)
    plt.plot(dates_year, linear_year_y, label="Linear component")
    plt.plot(dates_year, uniform_year_y, label="Uniform component")
    plt.ylabel("Temperature °C ")
    plt.legend(loc="lower right")
    plt.title("Annual gradient")
    plt.subplot(3, 2, 3)
    plt.plot(dates_year, solar_year)
    plt.ylabel("Solar irradiance (W/m²)")
    plt.title("Annual solar irradiance")

    i, j = temperature.from_to_indices(df=temp_year, from_=from_, to=to)
    plt.subplot(3, 2, 2)
    plt.plot(dates_year[i : j + 1], temps_year_top[i : j + 1], label="Top of deck")
    plt.plot(dates_year[i : j + 1], temps_year[i : j + 1], label="Air")
    plt.plot(
        dates_year[i : j + 1], temps_year_bottom[i : j + 1], label="Bottom of deck"
    )
    plt.legend(loc="lower right")
    plt.title("Two day temperature")
    plt.subplot(3, 2, 6)
    plt.plot(dates_year[i : j + 1], linear_year_y[i : j + 1], label="Linear component")
    plt.plot(
        dates_year[i : j + 1], uniform_year_y[i : j + 1], label="Uniform component"
    )
    plt.legend(loc="lower right")
    plt.title("Two day gradient")
    plt.subplot(3, 2, 4)
    plt.plot(dates_year[i : j + 1], solar_year[i : j + 1])
    plt.title("Two day solar irradiance")

    for ps in [(1, 2), (3, 4), (5, 6)]:
        plt.subplot(3, 2, ps[1])
        plt.gca().set_yticklabels([])
        equal_lims("y", 3, 2, ps)

    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(
        c.get_image_path("temperature", f"gradient-1-{c.bridge.ref_temp_c}.pdf")
    )
    plt.close()

    plt.portrait()
    plt.subplot(2, 2, 1)
    plt.plot(dates_year, effect_year_y[0] * 1000)
    plt.ylabel("Y translation (mm)")
    plt.title(f"Annual Y translation\nat x={np.around(x, 1)} m, z={np.around(z, 1)} m")
    plt.subplot(2, 2, 3)
    plt.plot(dates_year, effect_year_s[0])
    plt.ylabel("Strain")
    plt.title(f"Annual strain\nat x={np.around(x, 1)} m, z={np.around(z, 1)} m")

    plt.subplot(2, 2, 2)
    plt.plot(dates_year[i : j + 1], effect_year_y[0][i : j + 1] * 1000)
    plt.title(f"Two day strain\nat x={np.around(x, 1)} m, z={np.around(z, 1)} m")
    plt.subplot(2, 2, 4)
    plt.plot(dates_year[i : j + 1], effect_year_s[0][i : j + 1])
    plt.title(f"Two day strain\nat x={np.around(x, 1)} m, z={np.around(z, 1)} m")

    for ps in [(1, 2), (3, 4)]:
        plt.subplot(2, 2, ps[1])
        plt.gca().set_yticklabels([])
        equal_lims("y", 2, 2, ps)

    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(c.get_image_path("temperature", "gradient-2.pdf"))
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
        config=config, response_type=ResponseType.StrainXXB,
        points=[Point(x=51)], weather=weather
    )[0]
    plt.scatter(weather["datetime"], effect * 1E6, c="g", s=1)
    plt.ylabel("Microstrain XXB")
    plt.gcf().autofmt_xdate()
    plt.title("Strain at X = 51 in May")
    print_i(f"Effect shape = {effect.shape}")

    # Save.
    plt.tight_layout()
    plt.savefig(config.get_image_path("verify/temperature", f"{fname}.pdf"))
    plt.close()
