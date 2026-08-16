import pickle
import os
import sys
from pathlib import Path
from angle_features import extract_joint_angles
from temporal_features import calculate_temporal_features

class FeatureExtractor:
    def __init__(self):
        self.features_cache= []
        print("Feature Extractor initialized")

    def extract_from_landmarks(self, landmarks_data):

        if landmarks_data is None:
            return None

        angles = extract_joint_angles(landmarks_data)

        return angles

    def process_landmark_file(self, input_pkl, output_pkl):

        if not os.path.exists(input_pkl):
            print("Error: not found {input_pk1}")
            return None

        with open(input_pkl, 'rb') as f:
            data = pickle.load(f)

        lendmarks_sequence = data['landmarks_data']
        video_name = data['video_name']
        total_frames = data['total_frames']

        features_sequence = []

        for frame_data in landmarks_sequence:
            landmarks = frame_data['landmarks']

            if landmarks is not None:
                features = self.extract_from_landmarks(landmarks)

                if features is not None:

                    temporal = calculate_temporal_features(features_sequence + [features])

                    features.update(temporal)

                    features['frame'] = frame_data['frame']
                    features_sequence.append(features)

        output_data = {
            'video_name': video_name,
            'total_frames': len(features_sequence),
            'features_sequence': features_sequence
        }

        os.makedirs(os.path.dirname(output_pkl), exist_ok=True)

        with open(output_pkl, 'wb') as f:
            pickle.dump(output_data, f)

        print(f" Caracteristics: {len(features_sequence)} frames")
        print(f" Saved: {output_pkl}")

        return features_sequence


def main():
    print("=" * 60)
    print("CARACTERISTIC EXTRACTOR")
    print("=" * 60)

    extractor = FeatureExtractor()

    os.makedirs('dataset/processed/features', exist_ok=True)

    landmarks_folder = 'dataset/processed/landmarks/'
    if not os.path.exists(landmarks_folder):
        print("File not found with landmarks")
        print("Execute first: preprocessing/video_to_landmarks.py")
        return

    landmark_files = [f for f in os.listdir(landmarks_folder) if f.endswith('.pkl') and not f.endswith('_visualized.pkl')]

    if not landmark_files:
        print("ladmarks files not founded in:", landmarks_folder)
        print("Execute first: preporcessing/video_to_landmarks.py")
        return

    print(f"\n Files with landmarks founded: {len(landmark_files)}")
    print("=" * 60)

    for landmark_file in landmark_files:
        input_path = os.path.join(landmarks_folder, landmark_file)
        output_name = landmark_file.replace('.pkl', '_features.pkl')
        output_path = f'dataset/processed/features/{output_name}'

        print(f"\n Processing: {landmark_file}")

        try:
            extractor.process_landmark_file(input_path, output_path)
        except Exception as e:
            print(f" Error: {e}")
            import traceback
            traceback.print_exc()
            continue

        print("-" * 40)


    print("\n Extraction for carecteristics completed")

    print("\n Summary:")

    print("   - Caracteristics saved in: dataset/processed/features")

if __name__ == "__main__":
    main()