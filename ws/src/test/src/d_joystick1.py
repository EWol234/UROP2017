#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy

from centennial_msgs.msg import D_drivetrainCmd
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist, Vector3

import sys, select, termios, tty

class JoystickControllerNode:
	def __init__(self):
		rospy.Subscriber("/joy", Joy, self.joy_callback, queue_size=10)

		self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
		rospy.loginfo("initialized")

	def joy_callback(self, msg):
		axes = msg.axes
		buttons = msg.buttons
		roboSpeed = 1.0;

		cmdMsg=Twist()
		linear = cmdMsg.linear
		angular = cmdMsg.angular
		speed = axes[2]
		turn = axes[1]
		switch_dir = True
		
		if speed < 0.1 and speed > -0.1:
			speed = 0
			switch_dir = False
		if turn < 0.1 and turn > -0.1:
			turn = 0

		linear.x = speed * roboSpeed
		if switch_dir:
			angular.z = (linear.x / (abs(linear.x))) * turn  * 0.75
		else:
			angular.z = turn		
	
		self.pub.publish(cmdMsg)

if __name__ == "__main__":
	rospy.init_node("dbot_teleop")
	node = JoystickControllerNode()
	rospy.spin()

