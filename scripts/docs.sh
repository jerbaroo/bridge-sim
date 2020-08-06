rm -rf docs/
poetry run pdoc --html --output-dir build bridge_sim
mv build/bridge_sim docs/
rm -rf build/
poetry run python scripts/docs-update.py
