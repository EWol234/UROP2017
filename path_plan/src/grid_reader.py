import rospy
from nav_msgs.msg import OccupancyGrid, Path
from geometry_msgs.msg import PoseStamped, Twist, Vector3, Point, Quaternion, Pose
import message_filters
import math
import random
from q_node import Node
import std_msgs.msg
from rosgraph_msgs.msg import Clock

class path_planner:
	def __init__(self):
		self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
		self.path_pub = rospy.Publisher('/plan', Path, queue_size=1)
		self.path = Path()
		self.publish = False
	
	def pathPub(self, clock):
		if self.publish:
			self.path.header.stamp = rospy.Time.now()
		self.path_pub.publish(self.path)	

	def endOfTheLine(self, q, radius, obstacles):
	    for i1 in range(q.getIntCoord()[0] - radius, q.getIntCoord()[0] + radius):
	        for j1 in range(q.getIntCoord()[1] - radius, q.getIntCoord()[1] + radius):
			for point in obstacles:
               			if (i1, j1) == point:
					return True

	def genSuccessors(self, q, step):
	    (x, y) = q.getCoord()
	    return [Node(x+step, y), Node(x-step, y), Node(x, y+step), Node(x, y-step)]

	def makePlan(self, init_node, goal_node, obstacles, radius):
		initial_node = Node(init_node[0], init_node[1])
		goal = Node(goal_node[0], goal_node[1])
	
		closed_list = []
		open_list = [initial_node]
		delta = 12
		finished = False
	
		while not finished:
			if open_list:
				current_node = open_list[0]
			else:
				break
			
			index = 0
			for n in range(0, len(open_list)):
				if open_list[n].getHCost() < current_node.getHCost():
					current_node = open_list[n]
					index = n
			
			successors = self.genSuccessors(current_node, delta)
		
			for s in successors:
				s.setParent(current_node)
				s.setH(s.distance(goal)**2)
				if self.endOfTheLine(s, int(radius), obstacles):
					continue
		
				the_list = open_list + closed_list
			
				for node in the_list:
					if node.getCoord() == s.getCoord() and node.getHCost() <= s.getHCost():
						break
				else:
					open_list.append(s)
		
				if s.getIntCoord()[0] in range(goal.getIntCoord()[0]-int(delta), goal.getIntCoord()[0]+int(delta)) and s.getIntCoord()[1] in range(goal.getIntCoord()[1]-int(delta), goal.getIntCoord()[1]+int(delta)):
					finished = True
					return s
		    	print(current_node.getCoord())
			closed_list.append(open_list.pop(index))
	
	def createPath(self, points, origin, resolution):
		path = Path()
		path.header.stamp = rospy.Time.now()
		path.header.frame_id = 'map'
		for i in points:
			pose_stamp = PoseStamped()
			pose_stamp.header.stamp = rospy.Time.now()
			pose_stamp.header.frame_id = 'map'
			pose_stamp.pose.position.x = origin.position.x + i.getCoord()[0]*resolution
			pose_stamp.pose.position.y = origin.position.y + i.getCoord()[1]*resolution
			path.poses.append(pose_stamp)
		self.path = path
		self.publish = True
	
	def followPath(self, path, robo_pose):
		print("starting")
		cmdMsg =  Twist()
		linear = cmdMsg.linear
		angular = cmdMsg.angular
		if path.poses:
			next_pose = path.poses[0].pose
		else:
			next_pose = robo_pose.pose
		heading = math.atan2(robo_pose.pose.position.y-next_pose.position.y, robo_pose.pose.position.x-next_pose.position.x) - 3.1415
		q_heading = -math.sin(heading/2)

		angular.z = 0.5

		if robo_pose.pose.orientation.z - q_heading < 0.1 and robo_pose.pose.orientation.z - q_heading > -0.1:
			angular.z = 0
		self.pub.publish(cmdMsg)
		print(q_heading)
		print(robo_pose.pose.orientation.z)	
		
		linear.x = 0
		if angular.z == 0:
			linear.x = 0.2

		if robo_pose.pose.position.x - next_pose.position.x < 0.1 and robo_pose.pose.position.x - next_pose.position.x > -0.1 and robo_pose.pose.position.y - next_pose.position.y < 0.1 and robo_pose.pose.position.y - next_pose.position.y > -0.1:
			linear.x = 0
			angular.z = 0
			print("removed node")
			self.path.poses = self.path.poses[1:]
		self.pub.publish(cmdMsg)

	def callback(self, data, robo_pose, goal_pose):
		origin = data.info.origin
		resolution = data.info.resolution
		cmdMsg = Twist()
		linear = cmdMsg.linear
		max_dist = 0.3
		print("called")
		obstacles = []
		for i in range(0, len(data.data)):
			if data.data[i] > 90:
				row = i / data.info.height
				column = i % data.info.height
				obstacles.append((column, row))
		robot_grid = (int((robo_pose.pose.position.x-origin.position.x)/resolution), int((robo_pose.pose.position.y-origin.position.y)/resolution))
		goal_grid = (int((goal_pose.pose.position.x-origin.position.x)/resolution), int((goal_pose.pose.position.y-origin.position.y)/resolution))
		print(robot_grid)
		print(goal_grid)
		end_node = self.makePlan(robot_grid, goal_grid, obstacles, max_dist/resolution)
		next_node = True
		final = end_node
		points = []
		while next_node:
			points = [final] + points
			if final.getParent() is not False:
				final = final.getParent()
			else:
				next_node = False
		
		self.createPath(points, origin, resolution)

if __name__ == '__main__':
	rospy.init_node('map_listener')
	node = path_planner()
	map_sub = message_filters.Subscriber("map", OccupancyGrid)
	pose_sub = message_filters.Subscriber("slam_out_pose", PoseStamped)
	goal_sub = message_filters.Subscriber("move_base_simple/goal", PoseStamped)
	ts = message_filters.ApproximateTimeSynchronizer([map_sub, pose_sub, goal_sub], 10, 3)
	ts.registerCallback(node.callback)
	rospy.Subscriber("clock", Clock, node.pathPub)
	path_sub = message_filters.Subscriber("plan", Path)
	ts2 = message_filters.ApproximateTimeSynchronizer([path_sub, pose_sub], 10, 3)
	ts2.registerCallback(node.followPath)
	rospy.spin()

