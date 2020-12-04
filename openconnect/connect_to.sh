#!/usr/bin/env bash

MY_UID=`id -u ${USER}`
MY_GID=`id -g ${USER}`


docker run -ti \
	   --rm \
	   --cap-add NET_ADMIN --device /dev/net/tun \
	   --name vpn \
	   --mount type=bind,source="$(pwd)"/target,target=/data  \
	   -e VPN_URL="${1}" \
	   -e APP_UID=${MY_UID} -e APP_GID=${MY_GID} \
	   openconnect:latest
