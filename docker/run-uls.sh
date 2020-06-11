#!/bin/bash
#SBATCH -n 16
#SBATCH -t 12:00:00
#SBATCH -p normal

cp "$HOME"/bridge-sim_v0.0.5.sif "$TMPDIR"/bridge-sim.sif
singularity exec "$TMPDIR"/bridge-sim.sif "$HOME"/sim-uls.sh
