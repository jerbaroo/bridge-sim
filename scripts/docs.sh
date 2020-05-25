rm -rf docs/
pipenv run pdoc --html --output-dir build bridge_sim
mv build/bridge_sim docs/
rm -rf build/
pipenv run python scripts/docs-update.py
