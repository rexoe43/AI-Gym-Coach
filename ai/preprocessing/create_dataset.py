import pickle
import pandas as pd
import json
import os
import numpy as np

class DatasetCreator:
    def __init__(self):
        self.datase_rows = []
        self.metadata = {
            'exercises': ['squat'],
            'labels': ['correct', 'incomplete_range'],
            'total_samples': 0,
            'total_repetitions': 0,
            'features': []
        }

        print("Dataset creator initialized")

    def segment_repetitions(self, features_sequence, min_frames=5):
        repetitions = []
        current_rep = []
        in_rep = False

        for features in features_sequence:
            if 'knee_angle_right' not in features:
                continue

            knee_angle = features['knee_angle_right']

        if knee_angle < 160 and not in_rep:
            in_rep = True
            current_rep = [features]

        elif in_rep:
            current_rep.append(features)

            if knee_angle > 160 and len(current_rep) > min_frames:
                repetitions.append(current_rep)
                in_rep = False
                current_rep = []

        if in_rep and len(current_rep) > min_frames:
            repetitions.append(current_rep)

        return repetitions

    def add_features_to_dataset(self, features_pkl, label, exercise='squat'):
        with open(features_pkl, 'rb') as f:
            data = pickle.load(f)

        features_sequence = data['features_sequence']
        video_name = data['video_name']
        total_frames = data['total_frames']

        print(f"Processing: {video_name}")
        print(f" Total frames: {len(features_sequence)}")

        repetitions = self.segment_repetitions(features_sequence)
        print(f"Repetitions detected: {len(repetitions)}")

        for rep_idx, rep in enumerate(repetitions):
            if len(rep) > 5:
                sample_id = f"{exercise}_{label}_{video_name.split('_')[2] if len(video_name.split('_')) > 2 else '001'}_{rep_idx:03d}"

                for frame_idx, features in enumerate(rep):
                    row = {
                        'sample-id': sample_id,
                        'exercise': exercise,
                        'label': label,
                        'frame_sequence': frame_idx + 1,
                        'total_frames': len(rep)
                    }

                    for key, value in features.items():
                        if key not in ['frame']:
                            if isinstance(value, (int, float, np.number)):
                                row[key] = float(value)
                            else:
                                row[key] = value

                                if key not in self.metadata['features']:
                                    self.metadata['features'].append(key)

                    self.dataset_rows.append(row)
                print(f" {len(repetitions)} repetitions added to dataset")
                print( " " + "-" * 40)

    def create_dataset(self):
        print("=" * 60)
        print("CREATING FINAL DATASET")
        print("=" * 60)

        features_folder = 'dataset/processed/features'
        if not os.path.exists(features_folder):
            print("Folder not found in features folder")
            print("Execute first: features/features_extractor.py")
            return None

        features_files = [f for f in os.listdir(features_folder) if f.endswith('_features.pkl')]

        if not features_files:
            print("Features files not founded in:", features_folder)
            print("Execute first: features/feature_extractor.py")
            return None

        print(f"\n Features file found: {len(features_files)}")
        print("=" * 60)

        for feature_file in features_files:
            file_path = os.path.join(features_folder, feature_file)

            if 'correct' in feature_file.lower():
                label = 'correct'
            elif 'incomplete' in feature_file.lower():
                label = 'incomplete_range'
            else:
                label = 'unknown'

            print(f"\n Processing: {feature_file}")
            print(f" Label: {label}")

            self.add_features_to_dataset(file_path, label)

        if not self.datase_rows:
            print(" No rows were generated for the dataset")
            return None

        df = pd.DataFrame(self.dataset_rows)

        base_columns = ['sample_id', 'exercise', 'label', 'frame_sequence', 'total_frames']
        feature_columns = [col for col in df.columns if col not in base_columns]
        df = df[base_columns + feature_columns]

        os.makedirs('dataset/datasets', exist_ok=True)
        output_path = 'dataset/datasets/exercise_dataset.csv'
        df.to_csv(output_path, index=False)

        print("\n" + "=" * 60)
        print("DATASET CREATED SUCCESSFULLY")
        print("=" * 60)
        print(f" File: {output_path}")
        print(f" Total files: {len(df)}")
        print(f" Total of repetitions: {df['sample_id'].nunique()}")
        print(f" Total of caracteristic: {len(feature_columns)}")

        print("\n Class distribution:")
        class_counts = df.groupby(['exercise', 'label']).size().reset_index(name='count')
        for _, row in class_counts.iterrows():
            print(f" - {row['exercise']} / {row['label']}: {row['count']} frames")

            print(f"\n Class repetitions")
            rep_counts = df.groupby(['exercise', 'label'])['sample_id'].nunique().reset_index(name='reps')
            for _, row in rep_counts.iterrows():
                print(f"  - {row['exercise']} / {row['label']}: {row['reps']} repetitions")

                self.metadata['total_samples'] = len(df)
                self.metadata['total_repetitions'] = df['sample_id'].nunique()
                self.metadata['frame_columns'] = feature_columns

                os.makedirs('dataset/metadata', exists_ok=True)
                with open('dataset/metadata/dataset_info.json', 'w') as f:
                    json.dump(self.metadata, f, indent=2)
                print(f"\n Metadata saved: dataset/metadata/dataset_info.json")

                print("\n Preview view of dataset:")
                print(df.head(10))

                print("\n Basic estadistic: ")
                print(df.describe())

                return df


if __name__ == "__main__":
    creator = DatasetCreator()
    df = creator.create_dataset()

    if df is not None:
        print("\n Dataset ready for the training")