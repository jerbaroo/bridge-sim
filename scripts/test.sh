shopt -s globstar
pipenv run black -t py37 --check code/**/*.py
