"""Plots of a bridge's material properties."""
from matplotlib.cm import get_cmap

from config import Config
from fem.params import ExptParams, SimParams
from fem.run.build.elements import shells_by_id
from fem.run.opensees import OSRunner
from fem.run.opensees.build.d3 import build_model_3d
from plot.geometry.shell import shell_properties_3d
from plot import default_cmap, plt


def material_property_plots(c: Config):
    """3D shell plots of each material property."""
    build_model_3d(
        c=c, expt_params=ExptParams([SimParams([], [])]), os_runner=OSRunner(c)
    )
    shells = list(shells_by_id.values())
    deck_shells = [s for s in shells if not s.pier]
    pier_shells = [s for s in shells if s.pier]

    for shells_name, shells_ in [
        ("all", shells),
        ("deck", deck_shells),
        ("pier", pier_shells),
    ]:
        for material, units, prop_f in [
            ("Thickness", "m", lambda s: s.thickness),
            ("Youngs", "MPa", lambda s: s.youngs),
            ("Poisson's", "m/m", lambda s: s.poissons),
            ("Density", "kg/m", lambda s: s.poissons),
        ]:
            shell_properties_3d(shells=shells_, prop_units=units, prop_f=prop_f)
            plt.title(f"{material} of {c.bridge.name}")
            plt.savefig(c.get_image_path("info", f"{material}-{shells_name}.pdf"))
            plt.close()
