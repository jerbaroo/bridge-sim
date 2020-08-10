set -x

poetry run stubgen bridge_sim/
export MYPYPATH=$(pwd)/out/bridge_sim/
poetry run mypy bridge_sim/
