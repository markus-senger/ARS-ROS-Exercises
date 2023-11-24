#!/usr/bin/env python

import rospy
import numpy as np
import csv

def process_steps(probabilities, landmark_positions, landmark_detection_prob, no_landmark_detection_prob):
    csv_file = open('localization_results.csv', 'w+')
    csv_writer = csv.writer(csv_file, delimiter=';')
    num_cells = len(probabilities)
    
    csv_writer.writerow(['Step'] + ['Cell {}'.format(i+1) for i in range(num_cells)])

    steps = [
        {'landmark': True},
        {'move': -3},
        {'landmark': True},
        {'move': -4},
        {'landmark': False}
    ]

    for step_num, step in enumerate(steps, 1):
        if 'landmark' in step:
            if step['landmark']:
                probabilities = update_probabilities_landmark(probabilities, landmark_positions, landmark_detection_prob, no_landmark_detection_prob)
            else:
                probabilities = update_probabilities_landmark(probabilities, landmark_positions, 1-landmark_detection_prob, 1-no_landmark_detection_prob)
        elif 'move' in step:
            probabilities = update_probabilities_movement(probabilities, step['move'])
            
        csv_writer.writerow([step_num] + list(probabilities))
        rospy.loginfo('Current Probabilities: %s', probabilities)
        rospy.sleep(1)

    csv_file.close()

def update_probabilities_landmark(probabilities, landmark_positions, landmark_detection_prob, no_landmark_detection_prob):
    updated_probabilities = np.copy(probabilities)
    for i in range(len(probabilities)):
        if i + 1 in landmark_positions:
            updated_probabilities[i] *= landmark_detection_prob
        else:
            updated_probabilities[i] *= no_landmark_detection_prob

    return updated_probabilities / np.sum(updated_probabilities)  # normalize

def update_probabilities_movement(probabilities, steps):
    probabilities = np.roll(probabilities, -steps)
    return probabilities / np.sum(probabilities) # normalize


rospy.init_node('markov_localization_node')

num_cells = 10
initial_probabilities = np.ones(num_cells) / num_cells  # initially equally distributed
landmark_positions = [1, 4, 7]
landmark_detection_prob = 0.8
no_landmark_detection_prob = 0.3

process_steps(initial_probabilities, landmark_positions, landmark_detection_prob, no_landmark_detection_prob)
rospy.spin()
