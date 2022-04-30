# Script square.py is used to takeoff to 10 meters and then to make a square in the air.

#!/usr/bin/env python3
import rospy
import mavros_msgs
from mavros_msgs.msg import State
from mavros_msgs.srv import SetMode, CommandBool,  CommandTOL
from geometry_msgs.msg import TwistStamped

class Drone:
    def __init__(self):
        self.state = State()
        self.connected = False
        self.vel = TwistStamped() 

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
            response = takeoff(altitude = 2, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
            rospy.loginfo("Takeoff ...")
        except rospy.ServiceException as e:
            rospy.loginfo("Takeoff failed")

    def move(self,x,y):        
        pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)
        self.vel.twist.linear.x = x
        self.vel.twist.linear.y = y
        pub.publish(self.vel)
        rospy.loginfo(self.vel)

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
    pos = [[0, 0], [-5, 0], [0, -5], [5, 0], [0, 5]]
    i = 0
    while i < len (pos):
        x = pos [i] [0]
        y = pos [i] [1]
        v.move(x, y)
        i = i+1
        rospy.sleep(10)
    v.land()    

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
