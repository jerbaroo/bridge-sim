import numpy as np

import plot

from build_model import Fix, Load, Patch, build_model
from run_model import run_model


if __name__ == "__main__":
    build_model(
        fix=[Fix(x_pos, y=True) for x_pos in np.arange(0, 1.01, 1/7)],
        load=[Load(0.5, -5e5), Load(0.519, -5e5), Load(0.485, -5e5)]
    )
    x, y, stress_strain = run_model()
    plot.animate_translation(x, y)
    plot.animate_stress_strain(stress_strain)
    plot.animate_stress_strain(stress_strain, stress=False)
