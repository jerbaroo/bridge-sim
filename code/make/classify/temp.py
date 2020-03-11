from datetime import datetime

import numpy as np

from config import Config
from classify import temperature
from fem.responses import Responses
from model.bridge import Point
from model.response import ResponseType
from plot import equal_lims, plt
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck
from util import resize_units


def temp_contour_plot(c: Config, temp_bottom: int, temp_top: int):
    """Plot the effect of temperature at a given temperature."""
    # Points on the deck to collect responses.
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
        # Resize responses if applicable to response type.
        resize_f, units = resize_units(response_type.units())
        if response_type == ResponseType.YTranslation:
            temp_effect = resize_f(temp_effect)
        responses = Responses(
            response_type=response_type,
            responses=[
                (temp_effect[p_ind], deck_points[p_ind])
                for p_ind in range(len(deck_points))
            ],
            units=units,
        )
        top_view_bridge(c.bridge, compass=False, lane_fill=False, piers=True)
        plot_contour_deck(c=c, responses=responses, decimals=6 if response_type == ResponseType.Strain else 2, loc="upper right")
        plt.title(f"{response_type.name()} when Tref,Tb,Tt = {c.bridge.ref_temp_c}°C,{temp_bottom}°C,{temp_top}°C")

    plt.landscape()
    plt.subplot(2, 1, 1)
    plot_response_type(ResponseType.YTranslation)
    plt.subplot(2, 1, 2)
    plot_response_type(ResponseType.Strain)
    plt.tight_layout()
    plt.savefig(c.get_image_path("classify", f"temp-effect-{temp_bottom}-{temp_top}.pdf"))
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
    dates_year = temp_year["datetime"]
    temps_year_bottom, temps_year_top = temperature.temps_bottom_top(
        c=c, temps=temps_year, len_per_hour=60
    )
    x, z = (c.bridge.x_max - (c.bridge.length / 2)), 0
    uniform_year, linear_year, effect_year = temperature.effect(
        c=c,
        response_type=ResponseType.YTranslation,
        points=[Point(x=x, y=0, z=z)],
        temps=temps_year,
        len_per_hour=60,
        d=True
    )
    plt.portrait()
    plt.subplot(3, 2, 1)
    plt.plot(dates_year, temps_year, label="Air")
    plt.plot(dates_year, temps_year_top, label="Top of deck")
    plt.plot(dates_year, temps_year_bottom, label="Bottom of deck")
    plt.legend(loc="lower right")
    plt.title("Annual temperature")
    plt.subplot(3, 2, 3)
    plt.plot(dates_year, linear_year, label="Linear component")
    plt.plot(dates_year, uniform_year, label="Uniform component")
    plt.legend(loc="lower right")
    plt.title("Annual gradient")
    plt.subplot(3, 2, 5)
    plt.plot(dates_year, effect_year[0] * 1000)
    plt.title(f"Annual Y translation\nat x={np.around(x, 1)} m, z={np.around(z, 1)} m")

    i, j = temperature.from_to_indices(df=temp_year, from_=from_, to=to)
    plt.subplot(3, 2, 2)
    plt.plot(dates_year[i:j+1], temps_year[i:j+1], label="Air")
    plt.plot(dates_year[i:j+1], temps_year_top[i:j+1], label="Top of deck")
    plt.plot(dates_year[i:j+1], temps_year_bottom[i:j+1], label="Bottom of deck")
    plt.legend(loc="lower right")
    plt.title("Two day temperature")
    plt.subplot(3, 2, 4)
    plt.plot(dates_year[i:j+1], linear_year[i:j+1], label="Linear component")
    plt.plot(dates_year[i:j+1], uniform_year[i:j+1], label="Uniform component")
    plt.legend(loc="lower right")
    plt.title("Two day gradient")
    plt.subplot(3, 2, 6)
    plt.plot(dates_year[i:j+1], effect_year[0][i:j+1] * 1000)
    plt.title(f"Two day Y translation\nat x={np.around(x, 1)} m, z={np.around(z, 1)} m")

    for ps in [(1, 2), (3, 4), (5, 6)]:
        equal_lims("y", 3, 2, ps)

    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(c.get_image_path("temperature", "gradient.pdf"))
    plt.close()
