# Script takeoff_and_land.py is used for simple takeoff to 10 meters and landing.

from __future__ import print_function
import os
import sys
import rospy
import mavros
import threading
import time
import mavros_msgs
from std_msgs.msg import String
from mavros_msgs.srv import SetMode, CommandBool,  CommandTOL

class Drone:
	def __init__(self):
		self.rate = 1
		self.connected = False
	
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
	time.sleep(10)
	v.arm()
	time.sleep(5)
	v.takeoff()
	time.sleep(10)
	v.land()
	time.sleep(10)
	
if __name__ == "__main__":
	main(sys.argv) 
