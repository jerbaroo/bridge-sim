from datetime import datetime

import numpy as np

from config import Config
from classify import temperature
from fem.responses import Responses
from model.bridge import Point
from model.response import ResponseType
from plot import plt
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck
from util import resize_units


def temp_contour_plot(c: Config, temp: int):
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
            c=c, response_type=response_type, points=deck_points, temps=[temp],
        ).T[0]
        # Resize responses if applicable to response type.
        resize_f, units = resize_units(response_type.units())
        if response_type == ResponseType.Strain:
            units = "E-6"
        elif resize_f is not None:
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
        plot_contour_deck(c=c, responses=responses, decimals=2)
        plt.title(f"{response_type.name()} at {temp} °C")

    plt.landscape()
    plt.subplot(2, 1, 1)
    plot_response_type(ResponseType.YTranslation)
    plt.subplot(2, 1, 2)
    plot_response_type(ResponseType.Strain)
    plt.tight_layout()
    plt.savefig(c.get_image_path("classify", f"temp-effect-{temp}.pdf"))
    plt.close()


def temp_gradient_plot(c: Config, date: str):
    """Plot the temperature gradient throughout the bridge deck."""
    from_ = datetime.fromisoformat(f"2019-07-01T00:00")
    to = datetime.fromisoformat(f"2019-07-02T23:59")
    temp = temperature.load(name=date)
    temp = temperature.from_to_mins(temp, from_, to)
    temps = temperature.resize(list(temp["temp"]))
    dates = temp["datetime"]
    temps_bottom, temps_top = temperature.temps_bottom_top(c=c, temps=temps)
    plt.plot(dates, temps, label="Air")
    plt.plot(dates, temps_bottom, label="Bottom of deck")
    plt.plot(dates, temps_top, label="Top of deck")
    plt.legend(loc="lower right")
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(c.get_image_path("temperature", "gradient.pdf"))
    plt.close()
