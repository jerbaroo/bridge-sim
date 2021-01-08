#!/usr/bin/env bash
set -euo pipefail

# Check versions to migrate to/from are correct.
RE='^[0-9]+([.][0-9]+)*$'
if ! [[ "$1" =~ $RE ]] ; then
  echo "error: first argument is not a number" >&2; exit 1
fi
if ! [[ "$2" =~ $RE ]] ; then
  echo "error: second argument is not a number" >&2; exit 1
fi
read -r -p "Migrating from v$1 to v$2, correct? [y/N]" RESPONSE 
case "$RESPONSE" in
  [yY][eE][sS]|[yY]) 
    echo "Okay, migrating from v$1 to v$2..."
    ;;
  *)
    echo "Exiting..." >&2; exit 1
    ;;
esac

# Assert we are on master branch, and it's clean.
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != *"master"* ]] ; then
  echo "error: not on master branch, exiting..." >&2; exit 1
fi
# if ! [[ -z "$(git status --porcelain)" ]]; then
#   echo "error: branch is not clean, exiting..." >&2; exit 1
# fi

# Check if docs are up-to-date.
# ./scripts/docs.sh
# if ! [[ -z "$(git status --porcelain docs)" ]]; then
#   echo "error: docs are not up-to-date, exiting..." >&2; exit 1
# fi

# Build Docker image.
docker build -f docker/Dockerfile .

# Run standard test suite.
export BRIDGE_SIM_TESTS=STANDARD
./scripts/test.sh

# Replace version numbers in files.
sed -i '' -e "s/$1/$2/g" README.org docker/Dockerfile pyproject.toml
echo "Replaced v$1 with v$2"

# Final instructions.
echo 'Check "git diff" manually'
git diff
echo 'Finally run these commands:'
echo "git commit -am 'Bump version to v$2'"
echo 'git push'
