import cv2
import mediapipe as mp
import numpy as np

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        print("Pose Detector Initialized")

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        landmarks = None
        annotated_frame = frame.copy()

        if results.pose_landmarks:
            landmarks = []
            for landmark in results.pose_landmarks.landmar:
                landmarks.append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z,
                    'visibility': landmark.visibility
                })

            self.mp_drawing.draw_landmarks(
                annotated_frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )

        return landmarks, annotated_frame

    def get_landmars_array(self, landmarks):
        if landmarks is None:
            return None

        landmark_array = []
        for lm in landmarks:
            landmark_array.extend([lm['x'], lm['y'], lm['z']])

        return np.array(landmark_array)

pose_detector = PoseDetector()
