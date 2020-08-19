FROM ubuntu:20.04
ENV OPENSEES_TAG v3.2.0
ENV BRIDGE_SIM_TAG v0.0.8.5
ENV PATH /root/.poetry/bin:/home/bin:$PATH
ENV DEBIAN_FRONTEND=noninteractive
# Install OpenSees.
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates g++ gcc gfortran git make \
      python3-dev tcl8.6 tcl8.6-dev && \
    mkdir /home/bin /home/lib && \
    cd /home && \
    git clone https://github.com/OpenSees/OpenSees.git && \
    cd /home/OpenSees && \
    git checkout $OPENSEES_TAG && \
    cp MAKES/Makefile.def.EC2-UBUNTU Makefile.def && \
    sed -i 's#BASE\t\t= ./usr/local#BASE\t\t= /usr/local#' Makefile.def && \
    sed -i 's#HOME\t\t= ./home#HOME\t\t= /home#' Makefile.def && \
    make
# Install bridge-sim.
RUN cd /home && \
    apt-get install -y --no-install-recommends curl ffmpeg python3 python3-venv && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
      | python3 && \
    git clone https://github.com/barischrooneyj/bridge-sim && \
    cd /home/bridge-sim && \
    git checkout $BRIDGE_SIM_TAG && \
    poetry install --no-dev && \
    poetry run python3 scripts/dockerize-example.py && \
    poetry run python3 example.py
# Cleanup.
RUN cd /home && \
    rm -r OpenSees lib && \
    apt-get remove ca-certificates curl git make python3-dev tcl8.6-dev && \
WORKDIR /home/bridge-sim
