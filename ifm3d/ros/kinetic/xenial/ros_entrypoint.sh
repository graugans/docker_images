#!/bin/bash
set -e

# setup ros environment
if [ -f /opt/ros/$ROS_DISTRO/setup.bash ]; then
  source /opt/ros/$ROS_DISTRO/setup.bash
fi

cd ${HOME}

export LPR_ROS=${HOME}/ros

if [ -d ${LPR_ROS} ]; then
    for i in $(ls ${LPR_ROS}); do
        if [ -d ${LPR_ROS}/${i} ]; then
            if [ -f ${LPR_ROS}/${i}/setup.bash ]; then
                source ${LPR_ROS}/${i}/setup.bash --extend
            fi
        fi
    done
fi

exec "$@"
