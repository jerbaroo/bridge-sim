CAT << EOF
docker login --username=barischrooneyj
docker build -f docker/Dockerfile
docker tag Y barischrooneyj/bridge-sim:version
docker push barischrooneyj/bridge-sim:version
EOF
