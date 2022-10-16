#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from gazebo_msgs.msg import ModelState
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
import numpy as np

x = 0.0
y = 0.0
theta = 0.0

# data = np.load("/home/saurav/catkin_ws/src/trans/scripts/shortest_path.npy)
data = np.array([[5, 5], [1, 3], [0, 0]])


def newOdom(msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])


rospy.init_node("speed_controller", anonymous=True)

sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

speed = Twist()

r = rospy.Rate(4)

goal = Point()
i = -1

while not rospy.is_shutdown():
    i = i + 1
    if i < len(data):
        goal.x, goal.y = data[i][0], data[i][1]
        inc_x = goal.x - x
        inc_y = goal.y - y

        angle_to_goal = atan2(inc_y, inc_x)

        if abs(angle_to_goal - theta) > 0.1:
            speed.linear.x = 0.0
            speed.angular.z = 0.3
        else:
            speed.linear.x = 0.5
            speed.angular.z = 0.0
        if inc_x < 0.05 and inc_y < 0.05:
            speed.linear.x = 0.0
            speed.angular.z = 0.0
            print("goal reached")

        pub.publish(speed)
        r.sleep()
