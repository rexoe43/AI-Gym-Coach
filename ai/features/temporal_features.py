import numpy as np

def calculate_temporal_features(features_sequence):

    if len(features_sequence) < 2:
        return {}

    current = features_sequence[-1]
    previous = features_sequence[-2]

    temporal_features = {}

    angle_keys = ['knee_angle_right', 'knee_angle_left', 'hip_angle_right', 
                  'hip_angle_left', 'torso_angle', 'elbow_angle_right', 
                  'elbow_angle_left', 'shoulder_angle_right', 'shoulder_angle_left']

    for key in angle_keys:
        if key in current and key in previous:
            velocity = current[key] - previous[key]
            temporal_features[f'{key}_velocity'] = velocity

    if len(features_sequence) >= 3:
        prev_prev = features_sequence[-3]
        for key in ['knee_angle_right', 'knee_angle_left', 'hip_angle_right', 'hip_angle_left']:
            if key in current and key in previous and key in prev_prev:
                v_current = current[key] - previous[key]
                v_previous = previous[key] - prev_prev[key]
                acceleration = v_current - v_previous
                temporal_features[f'{key}_acceleration'] = acceleration

            return temporal_features