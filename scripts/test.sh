set -euo pipefail

rm -rf test-data/
bash -c 'shopt -s globstar && poetry run black -t py37 --check bridge_sim/**/*.py'
poetry run pytest tests
