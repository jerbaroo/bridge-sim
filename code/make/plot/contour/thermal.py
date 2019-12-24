from config import Config
from fem.params import SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from model.response import ResponseType
from plot import plt
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck


def unit_axial_thermal_deck_load(c: Config):
    """Response to unit axial thermal deck loading."""
    response_types = [ResponseType.XTranslation, ResponseType.YTranslation, ResponseType.ZTranslation]
    for response_type in response_types:
        sim_responses = load_fem_responses(
            c=c,
            sim_runner=OSRunner(c),
            response_type=response_type,
            sim_params=SimParams(
                response_types=response_types,
                axial_delta_temp=c.unit_axial_delta_temp_c
            )
        )
        top_view_bridge(c.bridge, abutments=True, piers=True)
        plot_contour_deck(
            c=c,
            responses=sim_responses,
            levels=100,
        )
        plt.title(f"{response_type.name()} to {c.unit_axial_delta_temp_c}C axial thermal loading of the deck")
        plt.savefig(
            c.get_image_path(
                "contour",
                f"thermal-deck-unit-axial_load-{response_type.name()}.pdf"
            )
        )
        plt.close()


def unit_moment_thermal_deck_load(c: Config):
    """Response to unit moment thermal deck loading."""
    response_types = [ResponseType.XTranslation, ResponseType.YTranslation, ResponseType.ZTranslation]
    for response_type in response_types:
        sim_responses = load_fem_responses(
            c=c,
            sim_runner=OSRunner(c),
            response_type=response_type,
            sim_params=SimParams(
                response_types=response_types,
                moment_delta_temp=c.unit_moment_delta_temp_c
            )
        )
        top_view_bridge(c.bridge, abutments=True, piers=True)
        plot_contour_deck(
            c=c,
            responses=sim_responses,
            levels=100,
        )
        plt.title(f"{response_type.name()} to {c.unit_moment_delta_temp_c}C moment thermal loading of the deck")
        plt.savefig(
            c.get_image_path(
                "contour",
                f"thermal-deck-unit-moment-load-{response_type.name()}.pdf")
        )
        plt.close()


def unit_axial_thermal_deck_load(c: Config):
    """Response to unit axial thermal deck loading."""
    response_types = [ResponseType.XTranslation, ResponseType.YTranslation, ResponseType.ZTranslation]
    for response_type in response_types:
        sim_responses = load_fem_responses(
            c=c,
            sim_runner=OSRunner(c),
            response_type=response_type,
            sim_params=SimParams(
                response_types=response_types,
                axial_delta_temp=c.unit_axial_delta_temp_c
            )
        )
        top_view_bridge(c.bridge, abutments=True, piers=True)
        plot_contour_deck(
            c=c,
            responses=sim_responses,
            levels=100,
        )
        plt.title(f"{response_type.name()} to {c.unit_axial_delta_temp_c}C axial thermal loading of the deck")
        plt.savefig(
            c.get_image_path(
                "contour",
                f"thermal-deck-unit-axial_load-{response_type.name()}.pdf"
            )
        )
        plt.close()


def unit_moment_thermal_deck_load(c: Config):
    """Response to unit moment thermal deck loading."""
    response_types = [ResponseType.XTranslation, ResponseType.YTranslation, ResponseType.ZTranslation]
    for response_type in response_types:
        sim_responses = load_fem_responses(
            c=c,
            sim_runner=OSRunner(c),
            response_type=response_type,
            sim_params=SimParams(
                response_types=response_types,
                moment_delta_temp=c.unit_moment_delta_temp_c
            )
        )
        top_view_bridge(c.bridge, abutments=True, piers=True)
        plot_contour_deck(
            c=c,
            responses=sim_responses,
            levels=100,
        )
        plt.title(f"{response_type.name()} to {c.unit_moment_delta_temp_c}C moment thermal loading of the deck")
        plt.savefig(
            c.get_image_path(
                "contour",
                f"thermal-deck-unit-moment-load-{response_type.name()}.pdf")
        )
        plt.close()
