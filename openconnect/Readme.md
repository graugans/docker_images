# Introduction

The idea of this Dockerfile is to provide an VPN tunnel inside a Docker container to not mess with the entire routing of the host OS. This will allow to run dedicated commands like SSH in the VPN context. But does not require to use proxy dictated by the VPN in the host OS.

## Building the container

```
docker build  -t openconnect .
```

## Starting an VPN sesion

This will start a Docker instance with the name ``vpn``

```
docker run -ti --rm --cap-add NET_ADMIN --device /dev/net/tun --name vpn -e VPN_URL="https://<your company URI>" openconnect:latest
```
The instance above will ask you about the username and password


# Running an SSH shell in the VPN Docker instance


```
docker exec -ti vpn ssh <username>@<company-hostname>
```
