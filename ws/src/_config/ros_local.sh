#!/bin/sh
##########
# CONFIGURATION FOR USING REMOTE ROSCORE
##########
export ROS_MASTER_URI=http://127.0.0.1:11311
export ROS_PACKAGE_PATH=/home/user/ws/src:opt/ros/indigo/share:/opt/ros/indigo/stacks

. $(dirname ${BASH_SOURCE[0]})/../../../devel/setup.sh
exec "$@"
