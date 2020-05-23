rm -rf build/ docs/
pipenv run pdoc --html --output-dir build bridge_sim
mv build/bridge_sim docs/
