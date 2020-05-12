cd src
rm -rf build dist
pipenv run python setup.py sdist bdist_wheel
