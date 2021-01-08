#!/usr/bin/env bash
set -euo pipefail

VERSION=$(sed -n '2p' docker/Dockerfile | awk '{print $3}')
read -r -p "Tag Docker image as $VERSION, correct? [y/N]" RESPONSE 
case "$RESPONSE" in
  [yY][eE][sS]|[yY]) 
    echo "Okay, tagging Docker iamge as $VERSION..."
    ;;
  *)
    echo "Exiting..." >&2; exit 1
    ;;
esac
docker login --username=jerbaroo
docker build -f docker/Dockerfile .
docker tag Y "jerbaroo/bridge-sim:v$1"
docker push "jerbaroo/bridge-sim:v$1"
