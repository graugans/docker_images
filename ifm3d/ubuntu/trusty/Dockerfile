FROM ubuntu:14.04

# Proxy settings
#ENV http_proxy "http://xxx.xxx.xxx.xxx:xxxx"
#ENV https_proxy "http://xxx.xxx.xxx.xxx:xxxx"

ENV DEBIAN_FRONTEND noninteractive

# change this if zour camera does have a different ip setting
ENV IFM3D_IP 192.168.0.69

RUN apt-get update && apt-get -y upgrade

# Add support for PCL
RUN apt-get update && apt-get install -y software-properties-common && \
    add-apt-repository ppa:v-launchpad-jochen-sprickerhof-de/pcl

# Required Packages for the Host Development System
RUN apt-get update && apt-get install -y libboost-all-dev \
    git \
    vim-gtk \
    jq \
    libcurl4-openssl-dev \
    iputils-ping \
    bash \
    bash-completion \
    libgtest-dev \
    libgoogle-glog-dev \
    libxmlrpc-c++8-dev \
    libopencv-dev \
    libproj-dev \
    build-essential \
    coreutils \
    cmake \
    locales \
    ca-certificates \
    libpcl-all

# Set the locale
#RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
#    locale-gen en_US.UTF-8 && \
#    /usr/sbin/update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Create a non-root user that will perform the actual build
RUN id ifm3d 2>/dev/null || useradd --uid 30000 --create-home -s /bin/bash -U ifm3d
RUN apt-get update && apt-get install -y sudo
RUN echo "ifm3d ALL=(ALL) NOPASSWD: ALL" | tee -a /etc/sudoers

# install additional tooling
RUN apt-get update && apt-get install -y \
    tmux

# install vim plugins
USER ifm3d
WORKDIR /home/ifm3d

RUN git clone https://github.com/ifm/ifm3d.git
RUN NPROC=`nproc||echo 1` &&  \
    mkdir -p build/ifm3d && \
    cd ~/ifm3d; git checkout -b v0.8.3 v0.8.3 && \
    cd ~/build/ifm3d && \
    cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DBUILD_MODULE_PCICCLIENT=ON -DBUILD_MODULE_EXAMPLES=OFF -DCMAKE_INSTALL_PREFIX=/usr ../../ifm3d && \
    make -j$NPROC all && \
    sudo make -j$NPROC install


