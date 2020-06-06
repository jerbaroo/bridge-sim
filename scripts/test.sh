shopt -s globstar
pipenv run black -t py37 --check src/**/*.py 
pipenv run pytest tests
