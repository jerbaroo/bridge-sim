shopt -s globstar
pipenv run black -t py37 --check src/**/*.py 
export NO_OS_TESTS="true"
pipenv run pytest tests
