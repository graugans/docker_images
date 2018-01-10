FROM ubuntu:16.04

# Proxy settings
#ENV http_proxy "http://172.25.121.103:3128"
#ENV https_proxy "http://172.25.121.103:3128"

# change this if zour camera does have a different ip setting
ENV IFM3D_IP 192.168.0.69

RUN apt-get update && apt-get -y upgrade

# Required Packages for the Host Development System
RUN apt-get install -y --no-install-recommends \
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
    libpcl-dev \
    libproj-dev \
    build-essential \
    coreutils \
    dirmngr \
    gnupg2 \
    cmake \
    tmux \
    && rm -rf /var/lib/apt/lists/*

# setup keys
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 421C365BD9FF1F717815A3895523BAEEB01FA116

# setup sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list

# install bootstrap tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    python-rosdep \
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
RUN apt-get update && apt-get install -y \
    ros-kinetic-desktop=1.3.1-0* \
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
RUN git clone https://github.com/lovepark/ifm3d.git
RUN NPROC=`nproc||echo 1` &&  \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr ../ifm3d && \
    sudo make -j$NPROC install

# setup entrypoint
COPY ./ros_entrypoint.sh /home/ifm3d/ros/

# install ifm3d-ros
ENV LPR_ROS ~/ros

RUN mkdir ~/dev && \
    git clone https://github.com/lovepark/ifm3d-ros.git

RUN /bin/bash -c "source /opt/ros/$ROS_DISTRO/setup.bash && mkdir -p ~/catkin/ifm3d/src && \
    cd ~/catkin/ifm3d/src  && \
    catkin_init_workspace && \
    ln -s ~/dev/ifm3d-ros ifm3d && \
    cd ~/catkin/ifm3d && \
    catkin_make && \
    catkin_make -DCMAKE_INSTALL_PREFIX=${LPR_ROS}/ifm3d install"

RUN sudo chmod a+rwx /home/ifm3d/ros/ros_entrypoint.sh

ENTRYPOINT ["/home/ifm3d/ros/ros_entrypoint.sh"]
CMD ["bash"]
