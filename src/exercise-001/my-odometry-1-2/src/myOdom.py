#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist, Pose

def euler_to_quaternion(roll, pitch, yaw):
    qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
    qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
    qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    return qx, qy, qz, qw

def cmd_vel_callback(data):
    global current_x
    global current_y
    global current_theta
    global last_time

    current_time = rospy.Time.now()
    dt = (current_time - last_time).to_sec()
    linear_speed = data.linear.x
    angular_speed = data.angular.z

    current_x += linear_speed * dt * math.cos(current_theta)
    current_y += linear_speed * dt * math.sin(current_theta)
    current_theta += angular_speed * dt

    pose = Pose()
    pose.position.x = current_x
    pose.position.y = current_y
    qx, qy, qz, qw = euler_to_quaternion(0, 0, current_theta)
    pose.orientation.x = qx
    pose.orientation.y = qy
    pose.orientation.z = qz
    pose.orientation.w = qw

    pose_pub.publish(pose)
    last_time = current_time

rospy.init_node('turtlebot_pose_calculator')
pose_pub = rospy.Publisher('my_odom', Pose, queue_size=10)
cmd_sub = rospy.Subscriber('cmd_vel', Twist, cmd_vel_callback)
current_x = 0.0
current_y = 0.0
current_theta = 0.0
last_time = rospy.Time.now()

rospy.spin()