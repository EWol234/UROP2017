import rospy
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseStamped, Twist, Vector3, Point, Quaternion, Pose
import message_filters
import numpy

def callback(data, robo_pose):
	origin = data.info.origin
	resolution = data.info.resolution
	max_dist = 0.4
	rposx = robo_pose.pose.position.x
	rposy = robo_pose.pose.position.y
	print("rpos: "+str(rposx)+", "+str(rposy))
	print("called")
	for i in range(0, len(data.data)):
		if data.data[i] > 90:
			row = i / data.info.height
			column = i % data.info.height
			pose_x = origin.position.x + column*resolution
			pose_y = origin.position.y + row*resolution
			if pose_x >= rposx-max_dist and pose_x <= rposx+max_dist and pose_y >= rposy-max_dist and pose_y <= rposy+max_dist:
				print(str(pose_x)+", "+str(pose_y))

def listener():
	rospy.init_node('map_listener', anonymous=True)
	map_sub = message_filters.Subscriber("map", OccupancyGrid)
	pose_sub = message_filters.Subscriber("slam_out_pose", PoseStamped)
	ts = message_filters.ApproximateTimeSynchronizer([map_sub, pose_sub], 10, 3)
	ts.registerCallback(callback)
	rospy.spin()

if __name__ == '__main__':
	listener()

