shopt -s globstar
pipenv run black -t py37 --check code/**/*.py
pipenv run pytest code/model/test_load.py
pipenv run pytest code/model/test_scenario.py
pipenv run pytest code/classify/data/test_responses.py

