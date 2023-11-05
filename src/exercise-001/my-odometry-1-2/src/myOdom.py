#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler


def cmd_vel_callback(data):
    current_time = rospy.Time.now()
    dt = (current_time - last_time).to_sec()
    linear_speed = data.linear.x
    angular_speed = data.angular.z

    current_x += linear_speed * dt * math.cos(current_theta)
    current_y += linear_speed * dt * math.sin(current_theta)
    current_theta += angular_speed * dt

    odom = Odometry()
    odom.header.stamp = current_time
    odom.header.frame_id = 'odom'
    odom.child_frame_id = 'base_link'
    odom.pose.pose.position.x = current_x
    odom.pose.pose.position.y = current_y
    q = quaternion_from_euler(0, 0, current_theta)
    odom.pose.pose.orientation.x = q[0]
    odom.pose.pose.orientation.y = q[1]
    odom.pose.pose.orientation.z = q[2]
    odom.pose.pose.orientation.w = q[3]

    odom_pub.publish(odom)
    last_time = current_time

rospy.init_node('turtlebot_odometry_calculator')
odom_pub = rospy.Publisher('my_odom', Odometry, queue_size=10)
cmd_sub = rospy.Subscriber('cmd_vel', Twist, cmd_vel_callback)
current_x = 0.0
current_y = 0.0
current_theta = 0.0
last_time = rospy.Time.now()