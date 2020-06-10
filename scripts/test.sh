shopt -s globstar
rm -rf test-data/
pipenv run black -t py37 --check src/**/*.py && pipenv run pytest tests
