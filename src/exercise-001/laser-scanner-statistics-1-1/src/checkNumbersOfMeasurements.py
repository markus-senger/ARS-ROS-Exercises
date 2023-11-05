#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

def laser_scan_callback(data):
    rospy.loginfo("Anzahl der Messwerte in 'ranges': %d" % len(data.ranges))

rospy.init_node('laser_scan_listener')
rospy.Subscriber('/scan', LaserScan, laser_scan_callback)
rospy.spin()