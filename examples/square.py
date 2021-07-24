# Script square.py is used to takeoff to 10 meters and then to make a square in the air.

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
from geometry_msgs.msg import Twist
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import SetMode
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import CommandTOL
from mavros_msgs.srv import *

latitude =0.0
longitude=0.0


def globalPositionCallback(globalPositionCallback):
    global latitude
    global longitude
    latitude = globalPositionCallback.latitude
    longitude = globalPositionCallback.longitude

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
			
	def square(self):
		pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)
		vel = TwistStamped()

		vel.twist.linear.x=0;
		vel.twist.linear.y=0;
		pub.publish(vel);
		rospy.sleep(5);		
		
		vel.twist.linear.x=0;
		vel.twist.linear.y=-5;
		pub.publish(vel);
		rospy.sleep(5);
		
		vel.twist.linear.x=0;
		vel.twist.linear.y=0;
		pub.publish(vel);
		rospy.sleep(5);
		
		vel.twist.linear.x=5;
		vel.twist.linear.y=0;
		pub.publish(vel);
		rospy.sleep(5);

		vel.twist.linear.x=0;
		vel.twist.linear.y=0;
		pub.publish(vel);
		rospy.sleep(5);		
		
		vel.twist.linear.x=0;
		vel.twist.linear.y=5;
		pub.publish(vel);
		rospy.sleep(5);
		
		vel.twist.linear.x=0;
		vel.twist.linear.y=0;
		pub.publish(vel);
		rospy.sleep(5);
		
		vel.twist.linear.x=-5;
		vel.twist.linear.y=0;
		pub.publish(vel);
		rospy.sleep(5);
		
		
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
	v.square()
	time.sleep(10)
	v.land()
	time.sleep(10)
	
if __name__ == "__main__":
	main(sys.argv)
