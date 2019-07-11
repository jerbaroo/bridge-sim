"""Build Diana model files."""
from config import Config
from fem.params import ExptParams
from model import *
from util import *


def diana_mobile_load(c: Config, expt_params: ExptParams):
    """MOBILE load command for a Diana model file."""
    # https://dianafea.com/manuals/d101/Analys/node32.html
    start_x = c.bridge.length * expt_params.fem_params[0].loads[0].x_pos * 1000
    end_x = c.bridge.length * expt_params.fem_params[-1].loads[0].x_pos * 1000
    lane = c.bridge.lanes[expt_params.fem_params[0].loads[0].lane]
    lane_z_center = lane.z_center() * 1000
    # Path is given by start_x, start_y, start_z, end_x, end_y, end_z.
    path = (f"{start_x:.0f} {lane_z_center:.0f} 4165"
            + f" {end_x:.0f} {lane_z_center:.0f} 4165")
    dinc = f"{(end_x - start_x) / len(expt_params.fem_params):.0f}"

    return (
          f"CASE 2"
        + f"\nMOBILE"
        + f"\n     ELEMEN 1-57129"
        + f"\n     DIRECT 3"
        + f"\n     CODE NONE"
        + f"\n     AXFORC -{int(expt_params.fem_params[0].loads[0].weight)}"
        + f"\n     QUADIM 960 900"
        + f"\n     AXWIDT 2300"
        + f"\n     AXDIST 3600 1350 1500"
        + f"\n     PATH {path}"
        + f"\n     POSINC {dinc}")


def build_models(c: Config, expt_params: ExptParams) -> ExptParams:
    """Build Diana model files.

    If all simulations consist of a single load (where each load is identical
    apart from x_pos), then Diana a will build a single model file using the
    MOBILE Diana load command. ExptParams.is_mobile will be True and the model
    will be built to c.di_model_path.

    NOTE: Diana units are in mm, length of bridge 705 is 102m or 102000mm.

    """
    with open(c.di_model_template_path) as f:
        in_tcl = f.read()

    # MOBILE Diana load.
    mobile_load = True
    # Each simulation must consist of only one load.
    for fem_params in expt_params.fem_params:
        if len(fem_params.loads) != 1:
            mobile_load = False
    # Each simulation's load must be equal (apart from x position).
    if mobile_load:
        for fp1, fp2 in zip(
                expt_params.fem_params[:-1], expt_params.fem_params[1:]):
            if fp1.loads[0].weight != fp2.loads[0].weight:
                mobile_load = False
            if fp1.loads[0].lane != fp2.loads[0].lane:
                mobile_load = False
            if fp1.response_types != fp2.response_types:
                mobile_load = False
            if fp2.loads[0].x_pos < fp1.loads[0].x_pos:
                mobile_load = False
    expt_params.mobile_load = mobile_load
    if mobile_load:
        mobile_load_str = diana_mobile_load(c, expt_params)
        out_tcl = in_tcl.replace("<<MOBILE>>", mobile_load_str)
        print_i(mobile_load_str)
        with open(c.di_model_path, "w") as f:
            f.write(out_tcl)
        return expt_params

    raise ValueError("Diana: only MOBILE load supported")
    # for fem_params in expt_params.fem_params:
        # out_tcl = in_tcl.replace("<<LOADS>>", diana_loads(c, fem_params.loads))
        # with open(fem_params.built_model_file, "w") as f:
        #     f.write(out_tcl)
