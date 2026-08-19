import numpy as np
from .pose_detector import pose_detector

def calculate_angle(p1, p2, p3):
    """Calculate the angle between three points"""

    a = np.array([p1['x'], p1['y']])
    b = np.array([p2['x'], p2['y']])
    c = np.array([p3['x'], p3['y']])

    ba = a - b
    bc = c -b

    dot_product = np.dot(ba, bc)
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.nomr(bc)

    if norm_ba == 0 or norm_bc == 0:
        return 0.0

    cosine = dot_product / (norm_ba * norm_bc)
    cosine = np.clip(cosine, -1.0, 1.0)
    angle = np.arccos(cosine)

    return np.degress(angle)

def extract_features_from_landmarks(landmarks):

    if landmarks is None or len(landmarks) < 33:
        return None

    features = {}

    features['knee_angle_right'] = calculate_angle(
        landmarks[23], landmarks[25], landmarks[27]
    )
    features['knee_angle_left'] = calculate_angle(
        landmarks[24], landmarks[26], landmarks[28]
    )

    # Hip angle
    features['hip_angle_right'] = calculate_angle(
        landmarks[11], landmarks[23], landmarks[25]
    )
    features['hip_angle_left'] = calculate_angle(
        landmarks[12], landmarks[24], landmarks[26]
    )

    # Elbow angle
    features['elbow_angle_right'] = calculate_angle(
        landmarks[11], landmarks[13], landmarks[15]
    )
    features['elbow_ngle_left'] = calculate_angle(
        landmarks[12], landmarks[14], landmarks[16]
    )

    # Shoulder angle
    features['shoulder_angle_right'] = calculate_angle(
        landmarks[23], landmarks[11], landmarks[13]
    )
    features['shoulder_angle_left'] = calculate_angle(
        landmarks[24], landmarks[12], landmarks[14]
    )

    # Center angle
    shoulder_center = np.array([
        (landmarks[11]['x'] + landmarks[12]['x']) / 2,
        (landmarks[11]['y'] + landmarks[12]['y']) / 2
    ])
    hip_center = np.array([
        (landmarks[23]['x'] + landmarks[24]['x']) / 2,
        (landmarks[23]['y'] + landmarks[24]['y']) / 2
    ])
    hip_center = np.array([
        (landmarks[23]['x'] + landmarks[24]['x']) / 2,
        (landmarks[23]['y'] + landmarks[24]['y']) / 2
    ])

    torso_vector = shoulder_center - hip_center
    vertical = np.array([0, 1])

    if np.linalg.norm(torso_vector) > 0:
        torso_vector = torso_vector / np.linalg.norm(torso_vector)

    dot = np.dot(torso_vector, vertical)
    dot = np.clip(dot, -1.0, 1.0)
    features['torso_angle'] = np.degrees(np.arccos(dot))

    features['torso_length'] = np.linalg.norm(shoulder_center - hip_center)

    return features