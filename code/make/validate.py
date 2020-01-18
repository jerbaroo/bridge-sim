from config import Config
from model.load import PointLoad
from model.response import ResponseType
from fem.params import ExptParams, SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from util import clean_generated, print_s
from validate.campaign import displa_sensor_xz


def density_no_effect(c: Config):
    """Output maximum and minimum responses with different density values."""
    response_types = [ResponseType.YTranslation, ResponseType.Strain]
    pload = PointLoad(x_frac=0.5, z_frac=0.5, kn=100)
    c.bridge.type = "debugging"

    def set_density(density):
        for section in c.bridge.sections:
            print(section.density)
            section.density = density
        for pier in c.bridge.supports:
            if not callable(pier._sections):
                raise ValueError("Experiment requires callable pier sections")
            original_sections = pier._sections
            def new_sections(section_frac_len):
                section = original_sections(section_frac_len)
                section.density = density
                return section
            pier._sections = new_sections

    for density in [0.2, 100]:
        clean_generated(c)
        set_density(density)
        for response_type in response_types:
            sim_params = SimParams(
                response_types=[response_type],
                ploads=[pload],
            )
            sim_responses = load_fem_responses(
                c=c,
                sim_runner=OSRunner(c),
                response_type=response_type,
                sim_params=sim_params,
                run=True,
            )
            amax, amin = max(sim_responses.values()), min(sim_responses.values())
            print_s(f"Density's ratio = {density}")
            print_s(f"Max {response_type.name()} = {amax}")
            print_s(f"Min {response_type.name()} = {amin}")


def truck_1_time_series(c: Config):
    """Time series of 3 sensors to Truck 1's movement."""
    displa_labels = ["U13", "U26", "U29"]
    displa_points = []
    for displa_label in displa_labels:
        sensor_x, sensor_z = displa_sensor_xz[displa_label]
        displa_points.append(Point(x=sensor_x, y=0, z=sensor_z))
