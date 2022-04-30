# Script takeoff_and_land.py is used for simple takeoff to 10 meters and landing.

#!/usr/bin/env python3
import rospy
import mavros_msgs
from mavros_msgs.msg import State
from mavros_msgs.srv import SetMode, CommandBool,  CommandTOL

class Drone:
    def __init__(self):
        self.state = State()
        self.connected = False


    def connect(self):
        rospy.init_node('flying', anonymous=True)
        self.state.connected==True 
        rospy.loginfo("Connected...")

    def arm_and_takeoff(self):
        rospy.loginfo("Arming...")
        rospy.wait_for_service('/mavros/cmd/arming')
        try:
            armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
            armService(True)
            rospy.loginfo("Drone armed")
        except rospy.ServiceException as e:
            rospy.loginfo("Arming failed")

        rospy.wait_for_service('/mavros/cmd/takeoff')
        try:
            takeoff = rospy.ServiceProxy('/mavros/cmd/takeoff', CommandTOL)
            response = takeoff(altitude = 10, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
            rospy.loginfo("Takeoff ...")
        except rospy.ServiceException as e:
            rospy.loginfo("Takeoff failed")

    def land(self):
        rospy.wait_for_service('/mavros/cmd/land')
        try:
            landing = rospy.ServiceProxy('/mavros/cmd/land', CommandTOL)
            response = landing(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
            rospy.loginfo("Landing... ")
        except rospy.ServiceException as e:
            rospy.loginfo("Landing failed")


def main():
    v=Drone()
    v.connect()
    rospy.sleep(3)
    rospy.wait_for_service('/mavros/set_mode')
    change_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
    response = change_mode(custom_mode="GUIDED")
    v.arm_and_takeoff()
    rospy.sleep(10)
    v.land()    

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
