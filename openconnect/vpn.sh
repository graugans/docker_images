#!/usr/bin/env bash

APP_UID=${APP_UID:-1000}
APP_GID=${APP_GID:-1000}

groupadd -g ${APP_GID} appuser
useradd -c 'container user' -u ${APP_UID} -g ${APP_GID} appuser
chown -R ${APP_UID}:${APP_GID} /data

echo "Try to connect with ${VPN_URL}"
openconnect ${VPN_URL}
