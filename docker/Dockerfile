FROM ubuntu:bionic

# Copy project and set time zone.
COPY . bridge-sim
WORKDIR /bridge-sim
RUN apt-get update && ./docker/tzdata.sh

# Install Python 3.7.
WORKDIR /root
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y python3.7 python3-pip
RUN pip3 install pipenv

# Install bridge-sim Python dependencies.
WORKDIR /bridge-sim
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PIPENV_VENV_IN_PROJECT=true
RUN pipenv install --dev --python 3.7

# Additional software.
WORKDIR /root
RUN apt-get install -y vim wget

# Install OpenSees.
WORKDIR /root
RUN apt-get install -y make tcl8.6 tcl8.6-dev gcc g++ gfortran
RUN wget https://codeload.github.com/OpenSees/OpenSees/tar.gz/v3.2.0
RUN tar -xvzf v3.2.0 && mv OpenSees-3.2.0 OpenSees
COPY docker/Makefile.def.EC2-UBUNTU OpenSees/Makefile.def
RUN mkdir bin lib
WORKDIR /root/OpenSees
RUN make

WORKDIR /bridge-sim
# Necessary for bridge-sim to find project root.
RUN touch .git
# Overwrite the example with docker version.
RUN cp docker/example.py example.py
