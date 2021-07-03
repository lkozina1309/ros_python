from __future__ import print_function
import os
import sys
import rospy
import mavros
import threading
import time
from std_msgs.msg import String

class Drone:
	def __init__(self):
		self.rate = 1
		self.connected = False
	
	def connect(self, node: str, rate: int):
    		rospy.init_node(node, anonymous=True)
    		self.rate = rospy.Rate(rate)
    		self.connected = True
    		rospy.loginfo("Connected...")
    		rospy.spin()
	
def main(args):
	v=Drone()
	v.connect("drone",rate=10)
	
if __name__ == "__main__":
	main(sys.argv)
