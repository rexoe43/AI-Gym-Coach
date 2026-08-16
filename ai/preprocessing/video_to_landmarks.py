import cv2
import pickle
import os
import sys

try:
    import mediapipe as mp
    print(f" MediaPipe versión: {mp.__version__}")
except ImportError as e:
    print(f" Error importing MediaPipe: {e}")
    print(" Install MediaPipe: pip install mediapipe==0.10.8")
    sys.exit(1)

class LandmarkExtractor:
    def __init__(self):
        try:
            self.mp_pose = mp.solutions.pose
            self.pose = self.mp_pose.Pose(
                static_image_mode=False,
                model_complexity=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            self.mp_drawing = mp.solutions.drawing_utils
            print(" MediaPipe initialized correctly")
        except Exception as e:
            print(f" Error initializing MediaPipe: {e}")
            print(" Verify the packages: pip install mediapipe==0.10.8")
            sys.exit(1)

    def extract_from_video(self, video_path, output_path, save_visualization=False):
        if not os.path.exists(video_path):
            print(f" Error: Video no founded: {video_path}")
            return None
        
        cap = cv2.VideoCapture(video_path)
        all_landmarks = []
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = 0
        frames_with_landmarks = 0

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        vis_writer = None
        if save_visualization:
            vis_path = output_path.replace('.pkl', '_visualized.mp4')
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            vis_writer = cv2.VideoWriter(vis_path, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)

            if results.pose_landmarks:
                frames_with_landmarks += 1
                landmarks_data = []
                for landmark in results.pose_landmarks.landmark:
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

                if save_visualization and vis_writer:
                    vis_frame = frame.copy()
                    self.mp_drawing.draw_landmarks(
                        vis_frame,
                        results.pose_landmarks,
                        self.mp_pose.POSE_CONNECTIONS
                    )
                    vis_writer.write(vis_frame)
            else:
                all_landmarks.append({
                    'frame': frame_count,
                    'landmarks': None
                })
                
                if save_visualization and vis_writer:
                    vis_writer.write(frame)

        cap.release()
        if save_visualization and vis_writer:
            vis_writer.release()
            print(f"   Video visualized: {vis_path}")

        with open(output_path, 'wb') as f:
            pickle.dump({
                'video_name': os.path.basename(video_path),
                'total_frames': frame_count,
                'frames_with_landmarks': frames_with_landmarks,
                'fps': fps,
                'landmarks_data': all_landmarks
            }, f)

        print(f"   Landmarks: {frames_with_landmarks}/{frame_count} frames")
        print(f"   Saved: {output_path}")

        return all_landmarks

if __name__ == "__main__":
    print("=" * 60)
    print("LANDMARKS EXTRACTOR")
    print("=" * 60)
    
    extractor = LandmarkExtractor()
    
    os.makedirs('dataset/raw/videos', exist_ok=True)
    os.makedirs('dataset/processed/landmarks', exist_ok=True)

    video_folder = 'dataset/raw/videos/'
    video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    
    if not video_files:
        print("\n Videos no founded in dataset/raw/videos/")
        print(" Put the videos in that folder")
        print("   Example: squat_correct_1.mp4, squat_incomplete_1.mp4")
        exit()

    print(f"\n Videos founded: {len(video_files)}")
    print("=" * 60)

    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        output_name = video_file.replace('.mp4', '.pkl').replace('.avi', '.pkl')
        output_name = output_name.replace('.mov', '.pkl').replace('.mkv', '.pkl')
        output_path = f'dataset/processed/landmarks/{output_name}'
        
        print(f"\n Processing: {video_file}")
        
        try:
            extractor.extract_from_video(
                video_path, 
                output_path, 
                save_visualization=True
            )
        except Exception as e:
            print(f"  Error: {e}")
            continue
        
        print("-" * 40)

    print("\n¡Processing complete!")
    print("\n Verify the files:")
    print(f"   ls dataset/processed/landmarks/")