import numpy as np

def calculate_angle(p1, p2, p3):
    """Calculate the angle between three points"""

    a = np.array([p1['x'], p1['y']])
    b = np.array([p2['x'], p2['y']])
    c = np.array([p3['x'], p3['y']])

    ba = a - b
    bc = c -b

    dot_product = np.dot(ba, bc)
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)

    if norm_ba == 0 or norm_bc == 0:
        return 0.0

    cosine = dot_product / (norm_ba * norm_bc)
    cosine = np.clip(cosine, -1.0, 1.0)
    angle = np.arccos(cosine)

    return float(np.degrees(angle))


def pose_confidence(landmarks):
    if not landmarks or len(landmarks) < 29:
        return 0.0
    key_points = [11, 12, 23, 24, 25, 26, 27, 28]
    visibilities = [float(landmarks[i].get('visibility', 0.0)) for i in key_points]
    return float(sum(visibilities) / len(visibilities))


def active_knee_angle(features, landmarks=None):
    left = float(features.get('knee_angle_left', 180))
    right = float(features.get('knee_angle_right', 180))
    if landmarks and len(landmarks) > 26:
        left_vis = float(landmarks[25].get('visibility', 0))
        right_vis = float(landmarks[26].get('visibility', 0))
        if left_vis > 0.5 and right_vis > 0.5:
            return min(left, right)
        return left if left_vis >= right_vis else right
    return min(left, right)


def score_squat_technique(features, landmarks=None):
    knee = active_knee_angle(features, landmarks)
    torso = float(features.get('torso_angle', 0))
    confidence = pose_confidence(landmarks) if landmarks else 0.5

    if knee >= 150:
        depth_score = 60.0
        status = 'Ready'
    elif knee >= 110:
        depth_score = 70.0 + (150 - knee) / 40 * 15
        status = 'Descending'
    else:
        depth_score = max(0.0, 100.0 - abs(knee - 90) * 1.5)
        status = 'Bottom'

    torso_score = max(0.0, 100.0 - max(0.0, torso - 20) * 2.5)
    technique_score = max(0, min(100, 0.65 * depth_score + 0.35 * torso_score))

    good_torso = torso < 40
    if status == 'Bottom':
        label = 'correct' if knee <= 100 and good_torso else 'incomplete_range'
        status = 'Correct' if label == 'correct' else 'Improvable'
    elif status == 'Descending':
        label = 'correct' if good_torso else 'incomplete_range'
    else:
        label = 'correct' if good_torso else 'incomplete_range'

    return {
        'class': label,
        'label': label,
        'confidence': round(confidence, 3),
        'probabilities': {
            'correct': round(technique_score / 100.0, 3),
            'incomplete_range': round(1 - technique_score / 100.0, 3),
        },
        'technique_score': int(round(technique_score)),
        'status': status,
        'knee_angle': round(knee, 2),
        'torso_angle': round(torso, 2),
        'error': None,
    }


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
    features['elbow_angle_left'] = calculate_angle(
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

    torso_vector = shoulder_center - hip_center
    vertical = np.array([0, 1])

    if np.linalg.norm(torso_vector) > 0:
        torso_vector = torso_vector / np.linalg.norm(torso_vector)

    dot = np.dot(torso_vector, vertical)
    dot = np.clip(dot, -1.0, 1.0)
    features['torso_angle'] = float(np.degrees(np.arccos(dot)))
    features['torso_length'] = float(np.linalg.norm(shoulder_center - hip_center))

    return features