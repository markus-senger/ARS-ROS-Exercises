#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math

class NavigationNode:
    def __init__(self):
        rospy.init_node('navigation_node')

        self.velocity_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/scan', LaserScan, self.laser_callback)

        self.d_min = 0.2
        self.d_max = 1.0
        self.v_max = 0.5

    def calc_weight(self, angle, distance):
        w_ori = math.cos(angle / 1.2) 
        w_dist = 1.0 / (1.0 + math.exp(-(distance - 1.5) / 0.20))
        w_dist = 1.0 if distance > 3.5 else w_dist
        return w_ori * w_dist

    def laser_callback(self, laser_data):
        range1 = range(330, 360)
        range2 = range(0, 31)
        desired_range = list(range1) + list(range2)

        filtered_ranges = [1.0 if math.isinf(val) or val == 0 else val for i, val in enumerate(laser_data.ranges)]
        min_distance = min(val for i, val in enumerate(filtered_ranges) if i in desired_range)

        v = 0.0
        if min_distance > self.d_min:
            if min_distance < self.d_max:
                v = self.v_max * min_distance / self.d_max
            else:
                v = self.v_max
        
        range1 = range(270, 360, 3)
        range2 = range(0, 91, 3)
        desired_range = list(range1) + list(range2)

        weights = []
        angle = 0
        for (i, d) in enumerate(filtered_ranges):
            if i in desired_range:
                weights.append((angle, self.calc_weight(math.radians(angle), d)))
                angle += 3
                if angle > 90:
                    angle = -90

        alpha = math.atan2( sum(math.sin(math.radians(angle)) * w for i,(angle,w) in enumerate(weights)),
                            sum(math.cos(math.radians(angle)) * w for i,(angle,w) in enumerate(weights)))

        twist_msg = Twist()
        twist_msg.linear.x = v
        twist_msg.angular.z = alpha
        self.velocity_pub.publish(twist_msg)

if __name__ == '__main__':
    try:
        nav_node = NavigationNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass