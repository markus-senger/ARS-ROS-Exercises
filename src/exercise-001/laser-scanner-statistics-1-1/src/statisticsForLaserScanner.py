#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
import statistics
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import threading

values = {}

def laser_scan_callback(data):
    ranges = np.array(data.ranges) 
    ranges[np.isinf(ranges)] = 0
    cleaned_ranges = ranges.tolist()

    i = 0
    for x in cleaned_ranges:
        if i in values:
            values[i].append(x)
        else:
            values[i] = [x]
        i += 1

def play_rosbag(bag_file_path):
    subprocess.call(['rosbag', 'play', bag_file_path])
    mean = []
    var = []
    stdev = []
    for i in range(360):
        mean.append(statistics.mean(values[i]))
        var.append(statistics.variance(values[i]))
        stdev.append(statistics.stdev(values[i]))

    plt.figure(figsize=(10, 6))
    plt.plot(mean, label='mean')
    plt.plot(var, label='variance')
    plt.plot(stdev, label='standard deviation')
    plt.legend()
    plt.title('statistics for laserscan')
    plt.ylabel('values')
    plt.xlabel('scan number')
    plt.grid(True)
    plt.show()

rospy.init_node('laser_scan_listener_for_statistics')
rospy.Subscriber('/scan', LaserScan, laser_scan_callback)

bag_file_path = 'src/laser-scanner-statistics-1-1/bagfiles/laserdata_real.bag' 

play_thread = threading.Thread(target=lambda: play_rosbag(bag_file_path))
play_thread.start()

rospy.spin()


