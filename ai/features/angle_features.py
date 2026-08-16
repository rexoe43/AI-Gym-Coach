import numpy as np

def calculate_angle(p1, p2, p3):

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

    return np.degrees(angle)

def extract_joint_angles(landmarks):
    """
    Extracts key joint angles

    MediaPipe indices:
    11-12: Shoulders
    13-14: Elbows
    15-16: Wrists
    23-24: Hips
    25-26: Knees
    27-28: Ankles
    """

    angles = {}

    angles['knee_angle_right'] = calculate_angle(
        landmarks[23],
        landmarks[25],
        landmarks[27]
    )

    angles['knee_angle_left'] = calculate_angle(
        landmarks[24],
        landmarks[26],
        landmarks[28]
    )

    angles['hip_angle_right'] = calculate_angle(
        landmarks[11],
        landmarks[23],
        landmarks[25]
    )

    angles['hip_angle_left'] = calculate_angle(
        landmarks[12],
        landmarks[24],
        landmarks[26]
    )

    angles['elbow_angle_right'] = calculate_angle(
        landmarks[11],
        landmarks[13],
        landmarks[15]
    )

    angles['elbow_angle_left'] = calculate_angle(
        landmarks[12],
        landmarks[14],
        landmarks[16]
    )

    angles['shoulder_angle_right'] = calculate_angle(
        landmarks[23],
        landmarks[11],
        landmarks[13]
    )

    angles['shoulder_angle_left'] = calculate_angle(
        landmarks[24],
        landmarks[12],
        landmarks[14]
    )

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
    angles['torso_length'] = np.degrees(np.arccos(dot))

    shoulder_dist = np.linalg.norm(shoulder_center - hip_center)
    angles['torso_length'] = shoulder_dist

    return angles