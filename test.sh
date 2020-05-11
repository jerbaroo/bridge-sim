shopt -s globstar
pipenv run black -t py37 --check private/**/*.py public/**/*.py
export NO_OS_TESTS="true"
pipenv run pytest private/lib/model/test_load.py\
  private/lib/model/test_scenario.py\
  private/lib/model/bridge/test_bridge.py\
  private/lib/classify/data/test_responses.py
