#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
# from gazebo_msgs.msg import ModelState
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
import numpy as np


###########################################################################################################################################

class micro_mouse:

    def __init__(self):

        self.x = 0
        self.y = 0

        rospy.init_node("speed_controller", anonymous=True)

        self.sub = rospy.Subscriber("/odom", Odometry, self.newOdom)
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

        self.speed = Twist()

        self.r = rospy.Rate(4)

        self.goal = Point()

    def newOdom(self, msg):

        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        rot_q = msg.pose.pose.orientation
        (roll, pitch, self.theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

        # print(self.x, self.y)

    def controller(self):
        inc_x = self.goal.x - self.x
        inc_y = self.goal.y - self.y
        print(inc_x, inc_y)
        angle_to_goal = atan2(inc_y, inc_x)

        del_theta = abs(angle_to_goal - self.theta)

        if inc_x < 0.1 and inc_y < 0.1:  # Reached position
            self.speed.linear.x = 0
            self.speed.angular.z = 0
            self.pub.publish(self.speed)
            self.r.sleep()

        else:
            if del_theta > 0.1:
                self.speed.linear.x = 0.0
                self.speed.angular.z = 0.3
            else:
                self.speed.linear.x = 0.5 * inc_x
                self.speed.angular.z = 0.0

            self.pub.publish(self.speed)
            self.r.sleep()
            self.controller()





###########################################################################################################################################

if __name__ == '__main__':
    try:
        # points = np.load('/home/sourav/catkin_ws/src/trans/scripts/shortest_path.npy')
        points = np.array([[5, 5], [7, 8], [1, 1]])
        mm = micro_mouse()

        rospy.sleep(1)
        for i in range(np.shape(points)[0]):
            mm.goal.x = points[i][0]
            mm.goal.y = points[i][1]
            print(mm.goal.x, mm.goal.y)

            mm.controller()

            print("Reached point  :", i + 1)
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
