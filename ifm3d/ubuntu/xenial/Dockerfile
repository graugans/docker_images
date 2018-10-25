FROM ubuntu:16.04

# Proxy settings
#ENV http_proxy "http://<proxy ip>:3128"
#ENV https_proxy "http://<proxy ip>:3128"

ENV DEBIAN_FRONTEND noninteractive

# change this if zour camera does have a different ip setting
ENV IFM3D_IP 192.168.0.69

RUN apt-get update && apt-get -y upgrade

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
    libpcl-dev \
    libproj-dev \
    build-essential \
    coreutils \
    cmake \
    clang-format \
    fonts-powerline \
    locales \
    ca-certificates \
    google-perftools \
    binutils \
    valgrind

# Set the locale
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    /usr/sbin/update-locale LANG=en_US.UTF-8

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
RUN mkdir -p /home/ifm3d/.vim
ADD vimrc /home/ifm3d/.vim

# Make vim airline look nice
RUN mkdir -p /home/ifm3d/.config/fontconfig/conf.d
ADD 50-enable-terminess-powerline.conf /home/ifm3d/.config/fontconfig/conf.d
RUN fc-cache -vf

RUN git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim && \
    vim +PluginInstall +qall

RUN git clone https://github.com/lovepark/ifm3d.git
RUN NPROC=`nproc||echo 1` &&  \
    mkdir -p build/ifm3d && \
    cd build/ifm3d && \
    cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DBUILD_MODULE_PCICCLIENT=ON -DCMAKE_INSTALL_PREFIX=/usr ../../ifm3d && \
    sudo make -j$NPROC install

RUN git clone https://github.com/lovepark/ifm3d-examples.git
RUN NPROC=`nproc||echo 1` &&  \
    mkdir -p build/ifm3d-examples && \
    cd build/ifm3d-examples && \
    cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_INSTALL_PREFIX=/usr ../../ifm3d-examples

RUN /home/ifm3d/.vim/bundle/YouCompleteMe/install.py --clang-completer
ADD .ycm_extra_conf.py /home/ifm3d/.vim

# we want fancy colors
ENV TERM=xterm-256color

