#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry

def odometry_publisher():
    rospy.init_node('odometry_publisher', anonymous=True)
    pub = rospy.Publisher('odometry_data', Odometry, queue_size=10)
    pub2 = rospy.Publisher('odometry_data2', Odometry, queue_size=10)
    
    rate = rospy.Rate(1) 

    with open('src/exercise-001/my-odometry-1-2/trajectoryTextfiles/trajectory_odom_real.txt', 'r') as file: 
        for line in file:
            parts = line.strip().split() 
            if len(parts) == 7:
                odometry_msg = Odometry()
                odometry_msg.header.frame_id = "base_link"
                odometry_msg.pose.pose.position.x = float(parts[0]) - 0.727819979191
                odometry_msg.pose.pose.position.y = float(parts[1]) - -0.142933622003
                odometry_msg.pose.pose.position.z = float(parts[2])
                odometry_msg.pose.pose.orientation.x = float(parts[3])
                odometry_msg.pose.pose.orientation.y = float(parts[4])
                odometry_msg.pose.pose.orientation.z = float(parts[5]) - 0.0376496426761
                odometry_msg.pose.pose.orientation.w = float(parts[6]) - 0.99929100275
                rospy.loginfo(odometry_msg)
                pub2.publish(odometry_msg)
            rate.sleep()
    with open('src/exercise-001/my-odometry-1-2/trajectoryTextfiles/trajectory_my_odom_real.txt', 'r') as file:
        for line in file:
            parts = line.strip().split() 
            if len(parts) == 7:
                odometry_msg = Odometry()
                odometry_msg.header.frame_id = "base_link"
                odometry_msg.pose.pose.position.x = float(parts[0]) 
                odometry_msg.pose.pose.position.y = float(parts[1])
                odometry_msg.pose.pose.position.z = float(parts[2])
                odometry_msg.pose.pose.orientation.x = float(parts[3])
                odometry_msg.pose.pose.orientation.y = float(parts[4])
                odometry_msg.pose.pose.orientation.z = float(parts[5])
                odometry_msg.pose.pose.orientation.w = float(parts[6])

                pub.publish(odometry_msg)
            rate.sleep()



odometry_publisher()