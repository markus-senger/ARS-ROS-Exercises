#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import threading

sum_values = []

def laser_scan_callback(data):
    ranges = np.array(data.ranges) 
    ranges[np.isinf(ranges)] = 0
    cleaned_ranges = ranges.tolist()

    sum_values.append(round(sum(cleaned_ranges), 1))

def play_rosbag(bag_file_path):
    subprocess.call(['rosbag', 'play', bag_file_path])

    plt.hist(sum_values, bins=len(sum_values), edgecolor='black') 

    plt.xlabel('values')
    plt.ylabel('frequency')
    plt.title('histogram summed values')
    plt.show()

rospy.init_node('sum_all_Values_from_laser_scan')
rospy.Subscriber('/scan', LaserScan, laser_scan_callback)

bag_file_path = 'src/exercise-001/laser-scanner-statistics-1-1/bagfiles/laserdata_simulation.bag' 

play_thread = threading.Thread(target=lambda: play_rosbag(bag_file_path))
play_thread.start()

rospy.spin()