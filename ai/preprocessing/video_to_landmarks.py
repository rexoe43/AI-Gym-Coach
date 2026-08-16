import cv2
import mediapipe as mp
import pickle
import os
from pathlib import Path

class LandmarkExtractor:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def extract_from_video(self, video_path, output_path, save_visualization=False):
        """
        Extract the landmarks from a video and save into the .pkl

        Args:
        video_path: Route video
        output_path: Landmark route save
        save_visualization: Save a video with landmarks drawing
        """
        cap = cv2.VideoCapture(video_path)
        all_landmarks = []
        fps = int(cap.get(cv2.CAP_PROF_FPS))
        frame_count = 0

        if save_visualization:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(
                output_path.replace('.pkl', '_visualized.mp4'),
                fourcc, fps,
                (int(cap.get(3)), int(cap.get(4)))
            )

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = self.pose.process(rgb_frame)

            if results.pose_landmarks:
                landmarks_data = []
                for landmark in results.pose_landmakrs.landmark:
                    landmarks_data.append({
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z,
                        'visibility': landmark.visibility
                    })

                all_landmarks.append({
                    'frame': frame_count,
                    'landmarks': landmarks_data
                })

                if save_visualization:
                    self.mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        self.mp_pose.POSE_CONNECTIONS
                    )
                    out.write(frame)

                else:
                    all_landmarks.append({
                        'frame': frame_count,
                        'landmarks': None
                    })

            cap.release()
            if save_visualization:
                out.release()

            with open(output_path, 'wb') as f:
                pickle.dump({
                    'video_name': os.path.basename(video_path),
                    'total_frames': frame_count,
                    'landmarks_data': all_landmarks
                }, f)

            print(f"Landmarks extracted: {frame_count} frames")
            print(f"Saved in {output_path}")

            return all_landmarks

if __name__ == "__main__":
    extractor = LandmarkExtractor()

    videos = [
        ('ai/dataset/raw/videos/squat_correct_1.mp4', 'ai/dataset/processed/landmarks/squat_correct_1.pkl'),
        ('ai/dataset/raw/videos/squat_correct_2.mp4', 'ai/dataset/processed/landmarks/squat_correct_2.pkl'),
        ('ai/dataset/raw/videos/squat_incomplete_1.mp4', 'ai/dataset/processed/landmarks/squat_incomplete_1.pkl'),
        ('ai/dataset/raw/videos/squat_incomplete_2.mp4', 'ai/dataset/processed/landmarks/squat_incomplete_2.pkl'),
    ]

    for video_path, output_path in videos:
        print(f"\n Processing: {video_path}")
        extractor.extract_from_video(video_path, output_path, save_visualization=True)

print("\n All videos procesed")