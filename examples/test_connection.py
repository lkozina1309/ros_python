# Script for testing connection

#!/usr/bin/env python3
import rospy
from mavros_msgs.msg import State

class Drone:
    def __init__(self):
        self.state = State()
        self.connected = False


    def connect(self):
        rospy.init_node('flying', anonymous=True)
        self.connected=True 
        rospy.loginfo("Connected...")

def main():
    v=Drone()
    v.connect()    

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
