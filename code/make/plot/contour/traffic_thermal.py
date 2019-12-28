from classify.scenario.bridge import ThermalBridge
from config import Config
from make.plot.contour.common import damage_scenario_traffic_plot
from model.response import ResponseType
from util import safe_str


def thermal_deck_load(c: Config, axial_delta_temp: float, moment_delta_temp: float):
    """Response to unit axial thermal deck loading."""
    response_types = [
        ResponseType.XTranslation,
        ResponseType.YTranslation,
        ResponseType.ZTranslation,
    ]
    damage_scenario_traffic_plot(
        c=c,
        response_types=response_types,
        damage_scenario=ThermalBridge(axial_delta_temp=c.unit_axial_delta_temp_c),
        titles=[
            f"{rt.name()} to {axial_delta_temp}C axial, {moment_delta_temp}C moment,\nthermal loading of the deck"
            for rt in response_types
        ],
        saves=[
            c.get_image_path(
                "contour-traffic",
                safe_str(
                    f"thermal-deck-axial-{axial_delta_temp}-moment-{moment_delta_temp}-{rt.name()})"
                )
                + ".pdf",
            )
            for rt in response_types
        ],
    )
