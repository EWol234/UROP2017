#!/bin/sh
##########
# CONFIGURATION FOR USING REMOTE ROSCORE
##########
export ROS_MASTER_URI=http://10.0.0.102:11311
export ROS_IP=10.0.0.102 
export ROS_HOSTNAME=dbot2
export ROS_PACKAGE_PATH=/home/user/ws/src:opt/ros/indigo/share:/opt/ros/indigo/stacks

. $(dirname ${BASH_SOURCE[0]})/home/user/ws/devel/setup.sh
exec "$@"
