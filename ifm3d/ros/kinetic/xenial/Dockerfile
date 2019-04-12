FROM ubuntu:16.04

# Proxy settings
#ENV http_proxy "http://172.25.121.103:3128"
#ENV https_proxy "http://172.25.121.103:3128"

# change this if zour camera does have a different ip setting
ENV IFM3D_IP 192.168.0.69

# Required Packages for the Host Development System
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends \
    libboost-all-dev \
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
    build-essential \
    coreutils \
    dirmngr \
    gnupg2 \
    cmake \
    tmux \
    && rm -rf /var/lib/apt/lists/*

# Add the universe repository to the package list
RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe


# setup keys
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 421C365BD9FF1F717815A3895523BAEEB01FA116

# setup sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list

# install bootstrap tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    python-rosdep \
    python3-ros-buildfarm \
    python-rosinstall \
    python-vcstools \
    && rm -rf /var/lib/apt/lists/*

# setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# bootstrap rosdep
RUN rosdep init \
    && rosdep update

# install ros packages
ENV ROS_DISTRO kinetic
# Why is the version number pinned to a specific version?
# --> https://github.com/osrf/docker_images/issues/171
RUN apt-get update && apt-get install -y \
    ros-kinetic-desktop-full=1.3.2-0* \
    python-catkin-tools \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    libhdf5-openmpi-dev \
    python-h5py \
    ros-kinetic-ros-numpy \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user that will perform the actual build
RUN id ifm3d 2>/dev/null || useradd --uid 30000 --create-home ifm3d
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sudo && \
    rm -rf /var/lib/apt/lists/*
RUN echo "ifm3d ALL=(ALL) NOPASSWD: ALL" | tee -a /etc/sudoers

USER ifm3d
WORKDIR /home/ifm3d

# Build & install ifm3d
RUN git clone --branch v0.9.2 https://github.com/lovepark/ifm3d.git
RUN /bin/bash -c "NPROC=`nproc||echo 1` &&  \
    mkdir build && \
    cd build && \
    source /opt/ros/$ROS_DISTRO/setup.bash && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr -DBUILD_MODULE_PCICCLIENT=ON ../ifm3d && \
    sudo make -j$NPROC -l$NPROC install"

# setup entrypoint
COPY ./ros_entrypoint.sh /

# Build & install ifm3d-ros
ENV LPR_ROS ~/ros

RUN mkdir ~/dev && \
    cd ~/dev && \
    git clone --branch v0.5.1 https://github.com/lovepark/ifm3d-ros.git

RUN /bin/bash -c "source /opt/ros/$ROS_DISTRO/setup.bash && mkdir -p ~/catkin/ifm3d/src && \
    cd ~/catkin/ifm3d/src  && \
    catkin_init_workspace && \
    ln -s ~/dev/ifm3d-ros ifm3d && \
    cd ~/catkin/ifm3d && \
    catkin_make && \
    catkin_make -DCMAKE_INSTALL_PREFIX=/home/ifm3d/ros/ifm3d install"

RUN sudo chmod a+rwx /ros_entrypoint.sh

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
