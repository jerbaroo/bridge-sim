from classify.scenario.bridge import ThermalBridge
from config import Config
from make.plot.contour.common import damage_scenario_contour_plot
from model.response import ResponseType
from util import safe_str


def unit_axial_thermal_deck_load(c: Config):
    """Response to unit axial thermal deck loading."""
    response_types = [ResponseType.XTranslation, ResponseType.YTranslation, ResponseType.ZTranslation]
    damage_scenario_contour_plot(
        c=c,
        response_types=response_types,
        damage_scenario=ThermalBridge(axial_delta_temp=c.unit_axial_delta_temp_c),
        titles=[f"{rt.name()} to {c.unit_axial_delta_temp_c}C axial thermal loading of the deck" for rt in response_types],
        saves=[
            c.get_image_path("contour", safe_str(f"thermal-deck-unit-axial_load-{rt.name()})") + ".pdf")
            for rt in response_types
        ]

    )


def unit_moment_thermal_deck_load(c: Config):
    """Response to unit moment thermal deck loading."""
    response_types = [ResponseType.XTranslation, ResponseType.YTranslation, ResponseType.ZTranslation]
    damage_scenario_contour_plot(
        c=c,
        response_types=response_types,
        damage_scenario=ThermalBridge(moment_delta_temp=c.unit_moment_delta_temp_c),
        titles=[f"{rt.name()} to {c.unit_moment_delta_temp_c}C moment thermal loading of the deck" for rt in response_types],
        saves=[
            c.get_image_path("contour", safe_str(f"thermal-deck-unit-moment_load-{rt.name()})") + ".pdf")
            for rt in response_types
        ]

    )


def unit_thermal_deck_load(c: Config):
    """Response to unit thermal deck loading."""
    response_types = [ResponseType.XTranslation, ResponseType.YTranslation, ResponseType.ZTranslation]
    damage_scenario_contour_plot(
        c=c,
        response_types=response_types,
        damage_scenario=ThermalBridge(
            axial_delta_temp=c.unit_axial_delta_temp_c,
            moment_delta_temp=c.unit_moment_delta_temp_c
        ),
        titles=[f"{rt.name()} to {c.unit_axial_delta_temp_c}C axial and \n {c.unit_moment_delta_temp_c}C moment thermal loading of the deck" for rt in response_types],
        saves=[
            c.get_image_path("contour", safe_str(f"thermal-unit-load-{rt.name()})") + ".pdf")
            for rt in response_types
        ]
    )
