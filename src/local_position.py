# Script local_position.py is used to takeoff to 10 meters and then to make a square in the air.

from __future__ import print_function
import os
import numpy as np
import math
import sys
import rospy
import mavros
import threading
import time
import mavros_msgs
from mavros import command
from std_msgs.msg import String
from mavros_msgs import srv
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode
from mavros_msgs.srv import *

class Drone:
		
	def __init__(self):
		self.rate = 1
		self.connected = False
	
	def gps_callback(self,data):
		self.gps = data
		self.gps_read = True

	def connect(self, node: str, rate: int):
    		rospy.init_node(node, anonymous=True)
    		self.rate = rospy.Rate(rate)
    		self.connected = True
    		rospy.loginfo("Connected...")
	
	def arm(self):
		print("Arming...")
		rospy.wait_for_service('/mavros/cmd/arming')
		try:
			armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
			armService(True)
		except rospy.ServiceException as e:
			print ("Service arm call failed: %s" %e)	
 
	def takeoff(self):
		print("Takeoff ...")
		rospy.wait_for_service('/mavros/cmd/takeoff')
		try:
			takeoffService = rospy.ServiceProxy('/mavros/cmd/takeoff', CommandTOL)	
			response = takeoffService(altitude = 10, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
			rospy.loginfo(response)
		except rospy.ServiceException as e:
			print ("Service takeoff call failed: %s"%e)
			
	def move(self, x, y):
		goal_pose = PoseStamped()
		local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 10) 

		goal_pose.header.frame_id = "8"
		goal_pose.header.seq = 1
		goal_pose.pose.position.x = x
		goal_pose.pose.position.y = y
		goal_pose.pose.position.z = 2
		local_position_pub.publish(goal_pose)
		rospy.loginfo(goal_pose)
		time.sleep(5)
		
	
	def land(self):
		print("Landing... ")
		rospy.wait_for_service('/mavros/cmd/land')
		try:
			landService = rospy.ServiceProxy('/mavros/cmd/land', CommandTOL)
			response = landService(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
			rospy.loginfo(response)
		except rospy.ServiceException as e:
			print ("service land call failed: %s. The vehicle cannot land "%e) 
			
def main(args):
	v=Drone()
	v.connect("drone",rate=10)
	time.sleep(10)
	rospy.wait_for_service('/mavros/set_mode')
	change_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
	response = change_mode(custom_mode="GUIDED")
	print("Mode set to GUIDED")
	time.sleep(5)
	v.arm()
	time.sleep(5)
	v.takeoff()
	time.sleep(10)
	pos = [[0, 0], [-20, 0], [-20, -20], [0, -20], [0, 0]]
	i = 0
	while i < len (pos):
		x = pos [i] [0]
		y = pos [i] [1]
		v.move(x, y)
		i = i+1
	v.land()
	time.sleep(10)
	
if __name__ == "__main__":
	main(sys.argv)
