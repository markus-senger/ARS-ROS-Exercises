#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry

def odometry_publisher():
    rospy.init_node('odometry_publisher', anonymous=True)
    pub = rospy.Publisher('odometry_data', Odometry, queue_size=10)
    pub2 = rospy.Publisher('odometry_data2', Odometry, queue_size=10)
    
    rate = rospy.Rate(10) 

    with open('/home/vm/ARS-ROS-Exercises/src/exercise-001/my-odometry-1-2/trajectoryTextfiles/trajectory_odom_backup.txt', 'r') as file: 
        for line in file:
            parts = line.strip().split() 
            odometry_msg = Odometry()
            odometry_msg.header.frame_id = "base_link"
            odometry_msg.pose.pose.position.x = float(parts[0]) - -13.9995842055
            odometry_msg.pose.pose.position.y = float(parts[1]) - -9.99990960784
            odometry_msg.pose.pose.position.z = float(parts[2]) - -0.00100207609696
            odometry_msg.pose.pose.orientation.x = float(parts[3])
            odometry_msg.pose.pose.orientation.y = float(parts[4])
            odometry_msg.pose.pose.orientation.z = float(parts[5])
            odometry_msg.pose.pose.orientation.w = float(parts[6])
            pub2.publish(odometry_msg)
            rate.sleep()

    with open('/home/vm/ARS-ROS-Exercises/src/exercise-001/my-odometry-1-2/trajectoryTextfiles/trajectory_my_odom_backup.txt', 'r') as file:
        for line in file:
            parts = line.strip().split() 
            odometry_msg = Odometry()
            odometry_msg.header.frame_id = "base_link"
            odometry_msg.pose.pose.position.x = float(parts[0]) - 12.7121
            odometry_msg.pose.pose.position.y = float(parts[1])
            odometry_msg.pose.pose.position.z = float(parts[2])
            odometry_msg.pose.pose.orientation.x = float(parts[3])
            odometry_msg.pose.pose.orientation.y = float(parts[4])
            odometry_msg.pose.pose.orientation.z = float(parts[5])
            odometry_msg.pose.pose.orientation.w = float(parts[6])

            pub.publish(odometry_msg)
            rate.sleep()

odometry_publisher()