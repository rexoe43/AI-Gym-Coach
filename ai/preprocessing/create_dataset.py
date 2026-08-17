# ai/preprocessing/create_dataset.py
import pickle
import pandas as pd
import json
import os
import numpy as np

class DatasetCreator:
    def __init__(self):
        self.dataset_rows = []  
        self.metadata = {
            'exercises': ['squat'],
            'labels': ['correct', 'incomplete_range'],
            'total_samples': 0,
            'total_repetitions': 0,
            'features': []
        }
        print("✅ Dataset creator initialized")

    def segment_repetitions(self, features_sequence, min_frames=5):
        """
        Segments a sequence of frames into individual repetitions
        Based on the right knee angle
        """
        repetitions = []
        
        if len(features_sequence) < 10:
            return repetitions
        
        knee_angles = []
        for f in features_sequence:
            if 'knee_angle_right' in f:
                knee_angles.append(f['knee_angle_right'])
        
        if not knee_angles:
            return repetitions
        
        angle_min = np.percentile(knee_angles, 5)   
        angle_max = np.percentile(knee_angles, 95)  
        threshold = angle_min + (angle_max - angle_min) * 0.3  
        
        print(f"   Umbral detected: {threshold:.2f}°")
        print(f"    Range of the angles: {angle_min:.2f}° - {angle_max:.2f}°")
        
        current_rep = []
        in_rep = False
        
        for features in features_sequence:
            if 'knee_angle_right' not in features:
                continue
                
            knee_angle = features['knee_angle_right']
            
            if knee_angle < threshold and not in_rep:
                in_rep = True
                current_rep = [features]
            
            elif in_rep:
                current_rep.append(features)
                
                if knee_angle > threshold and len(current_rep) > min_frames:
                    
                    rep_angles = [f.get('knee_angle_right', 0) for f in current_rep]
                    if min(rep_angles) < threshold - 10:  
                        repetitions.append(current_rep)
                    in_rep = False
                    current_rep = []
        
        if in_rep and len(current_rep) > min_frames:
            repetitions.append(current_rep)
        
        return repetitions

    def add_features_to_dataset(self, features_pkl, label, exercise='squat'):
        """
        Added the caracteristic of the dataset
        """
        with open(features_pkl, 'rb') as f:
            data = pickle.load(f)

        features_sequence = data['features_sequence']
        video_name = data['video_name']
        total_frames = data['total_frames']

        print(f"\n Processing: {video_name}")
        print(f"   Total frames: {len(features_sequence)}")

        # Segmentar en repeticiones
        repetitions = self.segment_repetitions(features_sequence)
        print(f"   Reps detected: {len(repetitions)}")

        if not repetitions:
            print("  Reps undetected")
            return

        for rep_idx, rep in enumerate(repetitions):
            if len(rep) > 5:
                parts = video_name.split('_')
                video_num = parts[2] if len(parts) > 2 else '001'
                sample_id = f"{exercise}_{label}_{video_num}_{rep_idx:03d}"

                for frame_idx, features in enumerate(rep):
                    row = {
                        'sample_id': sample_id,  
                        'exercise': exercise,
                        'label': label,
                        'frame_sequence': frame_idx + 1,
                        'total_frames': len(rep)
                    }

                    # Añadir todas las características
                    for key, value in features.items():
                        if key not in ['frame']:
                            if isinstance(value, (int, float, np.number)):
                                row[key] = float(value)
                            else:
                                row[key] = value

                            if key not in self.metadata['features']:
                                self.metadata['features'].append(key)

                    self.dataset_rows.append(row)

        print(f"    {len(repetitions)} added repetitions in dataset")
        print("   " + "-" * 40)

    def create_dataset(self):
        """
        Creating the final dataset
        """
        print("=" * 60)
        print("CREATING FINAL DATASET")
        print("=" * 60)

        features_folder = 'dataset/processed/features/'
        if not os.path.exists(features_folder):
            print("Folder of features not found")
            print("  Execute first: features/feature_extractor.py")
            return None

        feature_files = [f for f in os.listdir(features_folder) if f.endswith('_features.pkl')]

        if not feature_files:
            print("Files not found in dataset", features_folder)
            print("  Execute first: features/feature_extractor.py")
            return None

        print(f"\n Folders of features not found: {len(feature_files)}")
        print("=" * 60)

        for feature_file in feature_files:
            file_path = os.path.join(features_folder, feature_file)

            if 'correct' in feature_file.lower():
                label = 'correct'
            elif 'incomplete' in feature_file.lower():
                label = 'incomplete_range'
            else:
                label = 'unknown'

            print(f"\n Processing: {feature_file}")
            print(f"   Label: {label}")

            self.add_features_to_dataset(file_path, label)

        if not self.dataset_rows:  
            print("\n Rows no generated for dataset")
            print("\n  Diagnostic:")
            print("   - Verify the video")
            print("   - Stay sure for mediapipe detection")
            return None

        df = pd.DataFrame(self.dataset_rows)

        # Ordenar columnas
        base_columns = ['sample_id', 'exercise', 'label', 'frame_sequence', 'total_frames']
        feature_columns = [col for col in df.columns if col not in base_columns]
        df = df[base_columns + feature_columns]

        os.makedirs('dataset/datasets', exist_ok=True)
        output_path = 'dataset/datasets/exercise_dataset.csv'
        df.to_csv(output_path, index=False)

        print("\n" + "=" * 60)
        print("DATASET CREATED SUCCESFULL")
        print("=" * 60)
        print(f" Folder: {output_path}")
        print(f"   Total of rows: {len(df)}")
        print(f"   Total of repetitions: {df['sample_id'].nunique()}")
        print(f"   Total of caracteristics: {len(feature_columns)}")

        print("\n Class distribution:")
        class_counts = df.groupby(['exercise', 'label']).size().reset_index(name='count')
        for _, row in class_counts.iterrows():
            print(f"   - {row['exercise']} / {row['label']}: {row['count']} frames")

        print("\n Repetitions for class:")
        rep_counts = df.groupby(['exercise', 'label'])['sample_id'].nunique().reset_index(name='reps')
        for _, row in rep_counts.iterrows():
            print(f"   - {row['exercise']} / {row['label']}: {row['reps']} repetitions")

        self.metadata['total_samples'] = len(df)
        self.metadata['total_repetitions'] = df['sample_id'].nunique()
        self.metadata['frame_columns'] = feature_columns

        os.makedirs('dataset/metadata', exist_ok=True)  
        with open('dataset/metadata/dataset_info.json', 'w') as f:
            json.dump(self.metadata, f, indent=2)
        print(f"\n Metadatos saved: dataset/metadata/dataset_info.json")

        print("\n Preview view of dataset:")
        print(df.head(10))

        print("\n  Basic estadistic:")
        print(df.describe())

        return df

if __name__ == "__main__":
    creator = DatasetCreator()
    df = creator.create_dataset()

    if df is not None:
        print("\n ¡Dataset ready for training!")
        print("   python training/train_model.py")