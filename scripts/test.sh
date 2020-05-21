cd ..
shopt -s globstar
pipenv run black -t py37 --check src/**/*.py 
export NO_OS_TESTS="true"
pipenv run pytest src/lib/model/test_load.py\
  src/lib/model/test_scenario.py\
  src/lib/model/bridge/test_bridge.py\
  src/lib/classify/data/test_responses.py
