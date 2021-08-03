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
from mavros_msgs.msg import PositionTarget
from mavros_msgs.msg import GlobalPositionTarget
from geometry_msgs.msg import Twist
from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import SetMode
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import CommandTOL
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
			response = takeoffService(altitude = 2, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
			rospy.loginfo(response)
		except rospy.ServiceException as e:
			print ("Service takeoff call failed: %s"%e)
			
	def move(self):
		rospy.Subscriber("/mavros/global_position/global", NavSatFix, self.gps_callback)
		global_position_pub = rospy.Publisher('/mavros/setpoint_raw/global', GlobalPositionTarget, queue_size=1)
		g = GlobalPositionTarget() 
		g.latitude = -35.3632702
		g.longitude = 149.1652374
		g.altitude=2
		g.type_mask=4088
		g.coordinate_frame=6
		global_position_pub.publish(g)
		time.sleep(10)
			
		g.latitude = -35.3632702
		g.longitude = 149.1652582
		g.altitude=2
		g.type_mask=4088
		g.coordinate_frame=6
		global_position_pub.publish(g)
		time.sleep(10)
			
		g.latitude = -35.3632815
		g.longitude = 149.1652765
		g.altitude=2
		g.type_mask=4088
		g.coordinate_frame=6
		global_position_pub.publish(g)
		time.sleep(10)
			
		g.latitude = -35.363268
		g.longitude = 149.1652391
		g.altitude=2
		g.type_mask=4088
		g.coordinate_frame=6
		global_position_pub.publish(g)
		time.sleep(10)
	
						
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
	v.move()
	time.sleep(5)
	v.land()
	time.sleep(10)
	
if __name__ == "__main__":
	main(sys.argv)

