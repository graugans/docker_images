FROM ubuntu:16.04

# Proxy settings
#ENV http_proxy "http://172.25.121.103:3128"
#ENV https_proxy "http://172.25.121.103:3128"

RUN apt-get update && apt-get -y upgrade

# Required Packages for the Host Development System
RUN apt-get install -y libboost-all-dev \
    git \
    vim \
    iputils-ping \
    bash-completion \
    libgtest-dev \
    libgoogle-glog-dev \
    libxmlrpc-c++8-dev \
    libopencv-dev \
    libpcl-dev \
    libproj-dev \
    build-essential \
    coreutils \
    cmake

# Create a non-root user that will perform the actual build
RUN id ifm3d 2>/dev/null || useradd --uid 30000 --create-home ifm3d
RUN apt-get install -y sudo
RUN echo "ifm3d ALL=(ALL) NOPASSWD: ALL" | tee -a /etc/sudoers


USER ifm3d
WORKDIR /home/ifm3d
RUN git clone https://github.com/graugans/ifm3d.git
RUN cd ifm3d;git checkout -b windows/doc origin/windows/doc
RUN NPROC=`nproc||echo 1` &&  mkdir build && cd build && cmake -DCMAKE_INSTALL_PREFIX=/usr ../ifm3d && sudo make -j$NPROC install

