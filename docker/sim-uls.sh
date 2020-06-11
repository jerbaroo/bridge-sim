#!/bin/bash
per_node=20
start=$((SLURM_ARRAY_TASK_ID * $per_node))

indices=""
end=$((start + per_node - 1))
for i in $(eval echo {$start..$end})
do
  indices="$indices $i"
done

cd /bridge-sim
set -x
./scripts/cli.sh --save-to $HOME/gen-data --msl 0.5 --parallel 14 run uls --point --indices "$indices"
