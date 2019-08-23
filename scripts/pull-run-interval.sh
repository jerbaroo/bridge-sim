while true
do
  git pull
  (cd code && pipenv run python scripts/make_all.py)
done
