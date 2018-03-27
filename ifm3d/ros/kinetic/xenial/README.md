# How to build the ifm3d lib

We do recommend the usage of [Docker](https://www.docker.com/) for building the source code. We have tested this with a *Ubuntu 16.04* installation and Docker version: *Docker version 17.09.0-ce, build afdb6d4*

# Install Docker

Check your distribution information how to install docker

# Build the Docker container

Change to the folder containing the ``Dockerfile`` and execute the following command:

```
sudo docker build -t ifm3d-ros .
```
If you are working behind a cooperate firewall which uses a proxy server you can pass the proxy address to the docker build argument

```
docker build --build-arg http_proxy=http://<proxy-address>:<proxy port> --build-arg https_proxy=http://<proxy-address>:<proxy port> -t ifm3d-ros .
```

## Run the docker container

To run the docker container execute the following command

```
docker run -ti ifm3d-ros:latest
```
If you are working behind a cooperate firewall which uses a proxy server you can pass the proxy address to the docker run argument

```
docker run --env http_proxy=http://<proxy address>:<proxy port> --env http_proxys=http://<proxy address>:<proxy port> -ti ifm3d-ros:latest .
```

# Run the ifm3d command within the docker container

```
docker run -ti ifm3d-ros:latest ifm3d dump
```

# Use an interactive shell for development purposes

```
docker run --interactive --tty --entrypoint /bin/bash ifm3d-ros:latest
```
