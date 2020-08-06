poetry run stubgen src/
export MYPYPATH=~/cs/bridge-sim/out/src/
poetry run mypy src/bridge_sim/
