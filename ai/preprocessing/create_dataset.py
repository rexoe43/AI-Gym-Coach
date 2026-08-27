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
            'exercises': [],
            'labels': [],
            'total_samples': 0,
            'total_repetitions': 0,
            'features': []
        }
        print("✅ Dataset Creator initialized")
    
    def segment_repetitions(self, features_sequence, exercise='squat', min_frames=5):
        """
        Detecta repeticiones según el ejercicio:
        - squat: usa knee_angle_right
        - pushup: usa elbow_angle_right
        - curl: usa elbow_angle_right
        """
        repetitions = []
        
        if len(features_sequence) < 10:
            return repetitions
        
        # ✅ Elegir ángulo según ejercicio
        if exercise == 'pushup' or exercise == 'curl':
            angle_key = 'elbow_angle_right'
        else:
            angle_key = 'knee_angle_right'
        
        # ✅ Extraer ángulos
        angles = []
        for f in features_sequence:
            if angle_key in f:
                angles.append(f[angle_key])
        
        if not angles:
            print(f"   ⚠️ No se encontró '{angle_key}' en los frames")
            return repetitions
        
        angle_min = np.percentile(angles, 5)
        angle_max = np.percentile(angles, 95)
        threshold = angle_min + (angle_max - angle_min) * 0.3
        
        print(f"   📊 Ángulo usado: {angle_key}")
        print(f"   📊 Rango: {angle_min:.2f}° - {angle_max:.2f}°, Umbral: {threshold:.2f}°")
        
        current_rep = []
        in_rep = False
        
        for features in features_sequence:
            if angle_key not in features:
                continue
                
            angle = features[angle_key]
            
            if angle < threshold and not in_rep:
                in_rep = True
                current_rep = [features]
            
            elif in_rep:
                current_rep.append(features)
                
                if angle > threshold and len(current_rep) > min_frames:
                    rep_angles = [f.get(angle_key, 0) for f in current_rep]
                    if min(rep_angles) < threshold - 10:
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

        print(f"\n📊 Procesando: {video_name}")
        print(f"   Total frames: {len(features_sequence)}")
        print(f"   Ejercicio detectado: {exercise}")
        print(f"   Label: {label}")

        # ✅ PASAR EL EJERCICIO A segment_repetitions
        repetitions = self.segment_repetitions(features_sequence, exercise=exercise)
        print(f"   Repeticiones detectadas: {len(repetitions)}")

        if not repetitions:
            print("   ⚠️ No se detectaron repeticiones")
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

                    for key, value in features.items():
                        if key not in ['frame']:
                            if isinstance(value, (int, float, np.number)):
                                row[key] = float(value)
                            else:
                                row[key] = value

                            if key not in self.metadata['features']:
                                self.metadata['features'].append(key)

                    self.dataset_rows.append(row)

        if exercise not in self.metadata['exercises']:
            self.metadata['exercises'].append(exercise)
        if label not in self.metadata['labels']:
            self.metadata['labels'].append(label)

        print(f"   ✅ {len(repetitions)} repeticiones agregadas al dataset")
        print("   " + "-" * 40)

    def create_dataset(self):
        print("=" * 60)
        print("📊 CREANDO DATASET FINAL")
        print("=" * 60)

        features_folder = 'dataset/processed/features/'
        if not os.path.exists(features_folder):
            print("❌ No se encuentra la carpeta de features")
            return None

        feature_files = [f for f in os.listdir(features_folder) if f.endswith('_features.pkl')]

        if not feature_files:
            print("⚠️ No se encontraron archivos de features")
            return None

        print(f"\n📂 Archivos de features encontrados: {len(feature_files)}")
        print("=" * 60)

        for feature_file in feature_files:
            file_path = os.path.join(features_folder, feature_file)

            if 'squat' in feature_file.lower():
                exercise = 'squat'
            elif 'pushup' in feature_file.lower():
                exercise = 'pushup'
            elif 'curl' in feature_file.lower():
                exercise = 'curl'
            else:
                exercise = 'unknown'

            if 'correct' in feature_file.lower():
                label = 'correct'
            elif 'incomplete' in feature_file.lower():
                label = 'incomplete_range'
            else:
                label = 'unknown'

            print(f"\n📊 Procesando: {feature_file}")
            print(f"   Ejercicio: {exercise}")
            print(f"   Label: {label}")

            self.add_features_to_dataset(file_path, label, exercise)

        if not self.dataset_rows:
            print("\n❌ No se generaron filas para el dataset")
            return None

        df = pd.DataFrame(self.dataset_rows)

        base_columns = ['sample_id', 'exercise', 'label', 'frame_sequence', 'total_frames']
        feature_columns = [col for col in df.columns if col not in base_columns]
        df = df[base_columns + feature_columns]

        os.makedirs('dataset/datasets', exist_ok=True)

        general_path = 'dataset/datasets/exercise_dataset.csv'
        df.to_csv(general_path, index=False)
        print(f"\n📁 Dataset general guardado: {general_path}")

        for exercise in df['exercise'].unique():
            df_exercise = df[df['exercise'] == exercise]
            exercise_path = f'dataset/datasets/{exercise}_dataset.csv'
            df_exercise.to_csv(exercise_path, index=False)
            print(f"📁 Dataset de {exercise} guardado: {exercise_path} ({len(df_exercise)} filas)")

        print("\n" + "=" * 60)
        print("✅ DATASET CREADO EXITOSAMENTE")
        print("=" * 60)
        print(f"   Total de filas: {len(df)}")
        print(f"   Total de repeticiones: {df['sample_id'].nunique()}")
        print(f"   Ejercicios: {df['exercise'].unique()}")
        print(f"   Clases: {df['label'].unique()}")

        print("\n📊 Distribución por ejercicio y clase:")
        print(df.groupby(['exercise', 'label']).size())

        self.metadata['total_samples'] = len(df)
        self.metadata['total_repetitions'] = df['sample_id'].nunique()
        self.metadata['frame_columns'] = feature_columns

        os.makedirs('dataset/metadata', exist_ok=True)
        with open('dataset/metadata/dataset_info.json', 'w') as f:
            json.dump(self.metadata, f, indent=2)

        print(f"\n📝 Metadatos guardados: dataset/metadata/dataset_info.json")

        return df

if __name__ == "__main__":
    creator = DatasetCreator()
    df = creator.create_dataset()

    if df is not None:
        print("\n🎉 ¡Dataset listo para entrenamiento!")
        print("\n📁 Archivos generados:")
        for exercise in df['exercise'].unique():
            print(f"   - dataset/datasets/{exercise}_dataset.csv")