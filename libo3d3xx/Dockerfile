FROM ubuntu:16.04

# change this if zour camera does have a different ip setting
ENV O3D3XX_IP 192.168.0.69

RUN apt-get update && apt-get -y upgrade

# Required Packages for the Host Development System
RUN apt-get install -y libboost-all-dev \
    git \
    vim-nox \
    jq \
    libcurl4-openssl-dev \
    iputils-ping \
    bash \
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
RUN id o3d3xx 2>/dev/null || useradd --uid 30000 --create-home o3d3xx
RUN apt-get install -y sudo
RUN echo "o3d3xx ALL=(ALL) NOPASSWD: ALL" | tee -a /etc/sudoers

USER o3d3xx
WORKDIR /home/o3d3xx
RUN git clone https://github.com/lovepark/libo3d3xx.git

# Build and install the camera module
RUN NPROC=`nproc||echo 1` &&  \
    mkdir -p build/camera && \
    cd build/camera && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr -DBUILD_TESTS=OFF /home/o3d3xx/libo3d3xx/modules/camera && \
    make -j$NPROC  && \
    make -j$NPROC package && \
    sudo dpkg -i libo3d3xx-camera*.deb

# Build and install the framegrabber module
RUN NPROC=`nproc||echo 1` &&  \
    mkdir -p build/framegrabber && \
    cd build/framegrabber && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr -DBUILD_TESTS=OFF /home/o3d3xx/libo3d3xx/modules/framegrabber && \
    make -j$NPROC package && \
    sudo dpkg -i libo3d3xx-framegrabber*.deb

# Build and install the image module
RUN NPROC=`nproc||echo 1` &&  \
    mkdir -p build/image && \
    cd build/image && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr -DBUILD_TESTS=OFF /home/o3d3xx/libo3d3xx/modules/image && \
    make -j$NPROC package && \
    sudo dpkg -i libo3d3xx-image*.deb

