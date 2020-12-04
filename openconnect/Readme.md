# Introduction

The idea of this Dockerfile is to provide an VPN tunnel inside a Docker container to not mess with the entire routing of the host OS. This will allow to run dedicated commands like SSH in the VPN context. But does not require to use proxy dictated by the VPN in the host OS.

The wrapper ``connect_to`` and the entry point manage to convey the user and group IDs to the image and do provide an mount point to exchange data with the host and the container.

## Building the container

```
docker build  -t openconnect .
```

## Starting an VPN sesion

This will start a Docker instance with the name ``vpn``

```
connect_to.sh <https://Company-URL>
```
The instance above will ask you about the username and password


# Running an SSH shell in the VPN Docker instance


```
docker exec -ti --user $UID vpn ssh <username>@<company-hostname>
```

# Starting a Shell inside the VPN container

```
docker exec -ti --user $UID vpn bash
```

