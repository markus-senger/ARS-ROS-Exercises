#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
import statistics
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import threading

mean_values = []
variance_values = []
std_deviation_values = []

def laser_scan_callback(data):
    ranges = np.array(data.ranges) 
    ranges[np.isinf(ranges)] = 0
    cleaned_ranges = ranges.tolist()

    mean_values.append(statistics.mean(cleaned_ranges))
    variance_values.append(statistics.variance(cleaned_ranges))
    std_deviation_values.append(statistics.stdev(cleaned_ranges))

def play_rosbag(bag_file_path):
    subprocess.call(['rosbag', 'play', bag_file_path])
    
    plt.figure(figsize=(10, 6))
    plt.plot(mean_values, label='mean')
    plt.plot(variance_values, label='variance')
    plt.plot(std_deviation_values, label='standard deviation')
    plt.legend()
    plt.title('statistics for laserscan')
    plt.ylabel('values')
    plt.xlabel('scan number')
    plt.grid(True)
    plt.show()

rospy.init_node('laser_scan_listener_for_statistics')
rospy.Subscriber('/scan', LaserScan, laser_scan_callback)

bag_file_path = 'src/exercise-001/laser-scanner-statistics-1-1/bagfiles/laserdata_simulation.bag' 

play_thread = threading.Thread(target=lambda: play_rosbag(bag_file_path))
play_thread.start()

rospy.spin()


