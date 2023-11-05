#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose
import os

def odom_callback(data):
    global trajectory_file_odom
    pose = data.pose.pose
    write_to_file(trajectory_file_odom, pose)
    
def my_odom_callback(data):
    global trajectory_file_my_odom
    write_to_file(trajectory_file_my_odom, data)

def write_to_file(file, pose):
    x = pose.position.x
    y = pose.position.y
    z = pose.position.z
    qx = pose.orientation.x
    qy = pose.orientation.y
    qz = pose.orientation.z
    qw = pose.orientation.w
    file.write("{} {} {} {} {} {} {}\n".format(x, y, z, qx, qy, qz, qw))

rospy.init_node('my_trajectory_writer')

odom_topic = 'odom'
my_odom_topic = 'my_odom'

try:
    rospy.wait_for_message(odom_topic, Odometry, timeout=100) 
    rospy.wait_for_message(my_odom_topic, Pose, timeout=100) 
except rospy.ROSException:
    rospy.logerr("error")

odom1_sub = rospy.Subscriber(odom_topic, Odometry, odom_callback)
odom2_sub = rospy.Subscriber(my_odom_topic, Pose, my_odom_callback)
trajectory_file_odom = open(rospy.get_param('odom_file_path'), 'w+')
trajectory_file_my_odom = open(rospy.get_param('my_odom_file_path'), 'w+')

rospy.spin()