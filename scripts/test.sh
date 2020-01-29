shopt -s globstar
pipenv run black -t py37 --check code/**/*.py
pipenv run pytest -s code/model/test_load.py
