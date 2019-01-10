# How to build the ifm3d lib

We do recommend the usage of [Docker](https://www.docker.com/) for building the source code. We have tested this with a *Ubuntu 16.04* installation and Docker version: *Docker version 17.09.0-ce, build afdb6d4*

# Install Docker

Check your distribution information how to install docker

# Build the Docker container

Change to the folder containing the ``Dockerfile`` and execute the following command:

```
sudo docker build -t ifm3d-indigo-ros .
```
If you are working behind a cooperate firewall which uses a proxy server you can pass the proxy address to the docker build argument

```
docker build --build-arg http_proxy=http://<proxy-address>:<proxy port> --build-arg https_proxy=http://<proxy-address>:<proxy port> -t ifm3d-indigo-ros .
```

## Run the docker container

To run the docker container execute the following command

```
docker run -ti ifm3d-indigo-ros:latest
```
If you are working behind a cooperate firewall which uses a proxy server you can pass the proxy address to the docker run argument

```
docker run --env http_proxy=http://<proxy address>:<proxy port> --env https_proxy=http://<proxy address>:<proxy port> -ti ifm3d-indigo-ros:latest .
```

# Run the ifm3d command within the docker container

```
docker run -ti ifm3d-indigo-ros:latest ifm3d dump
```

# Use an interactive shell for development purposes

```
docker run --interactive --tty --name ifm3d-indigo-ros --entrypoint /bin/bash ifm3d-indigo-ros:latest
```

### Spawn multiple TTYs to the running instance

This is achieved by the ``exec`` command
```
$ docker exec -t -i ifm3d-indigo-ros /bin/bash
```

# Start a container created with --name

If you try to start the docker container by executing
```
$ docker run --interactive --tty --name ifm3d-indigo-ros ifm3d-indigo-ros:latest /bin/bash
```
again you might receive something like this

```
$ docker run --interactive --tty --name ifm3d-indigo-ros ifm3d-indigo-ros:latest bash
docker: Error response from daemon: Conflict. The container name "/ifm3d" is already in use by container "7bc03a89a81183f51ed72e2a32ec048316defe40b1bc4829b16a65e70508832e". You have to remove (or rename) that container to be able to reuse that name.
```
To restart this docker instance execute the following
```
$ docker start ifm3d-indigo-ros
```
This wil not spawn a shell. To open a shell to the container you have to spawn a new tty
```
$ docker exec -t -i ifm3d-indigo-ros /bin/bash
```


