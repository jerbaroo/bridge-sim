CAT << EOF
docker login --username=barischrooneyj

For the base image:
docker build -f docker/Dockerfile1 .
docker tag X barischrooneyj/bridge-sim-base

For the live image:
docker build -f docker/Dockerfile2 .
docker tag Y barischrooneyj/bridge-sim:version
docker push barischrooneyj/bridge-sim:version
EOF
