shopt -s globstar
pipenv run black -t py37 --check code/**/*.py
pipenv run pytest code/model/test_load.py\
  code/model/test_scenario.py\
  code/classify/data/test_responses.py

