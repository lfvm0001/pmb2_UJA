#!/bin/bash

export ROS_MASTER_URI=http://10.68.0.1:11311
export ROS_IP=10.68.0.1

source /home/pal/pmb2_UJA/devel/setup.bash
source /opt/pal/cobalt/setup.bash


exec "$@"