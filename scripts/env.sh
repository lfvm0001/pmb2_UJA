#!/bin/bash

source /home/pal/pmb2_UJA/devel/setup.bash

export ROS_MASTER_URI=http://10.68.0.1:11311
export ROS_IP=10.68.0.1

exec "$@"