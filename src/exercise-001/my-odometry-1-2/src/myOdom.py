#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist, Pose
from sensor_msgs.msg import JointState

last_time = None
th = 0
x = 0
y = 0

def euler_to_quaternion(roll, pitch, yaw):
    qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
    qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
    qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    return qx, qy, qz, qw

def callback(data):
    deltaTime = 0
    currentTime = data.header.stamp

    vl = data.velocity[0] * 0.033
    vr = data.velocity[1] * 0.033
    b = 0.1577

    v = (vl + vr) / 2.0
    dth = (vr - vl)/ b

    global last_time
    if last_time is not None:
        deltaTime = currentTime - last_time 
    
    last_time = currentTime

    global x
    global y
    global th
    x = x + (v * deltaTime.to_sec() * math.cos(th))
    y = y + (v * deltaTime.to_sec() * math.sin(th))
    th = th + dth * deltaTime.to_sec() 

    pose = Pose()
    pose.position.x = x
    pose.position.y = y
    qx, qy, qz, qw = euler_to_quaternion(0, 0, th)
    pose.orientation.x = qx
    pose.orientation.y = qy
    pose.orientation.z = qz
    pose.orientation.w = qw

    pose_pub.publish(pose)


rospy.init_node('turtlebot_pose_calculator')
pose_pub = rospy.Publisher('my_odom', Pose, queue_size=10)
joint_sub = rospy.Subscriber('joint_states', JointState, callback)

rospy.spin()