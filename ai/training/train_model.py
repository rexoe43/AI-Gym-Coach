import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
import os
import json
import matplotlib.pyplot as plt 
import seaborn as sns

class ModelTrainer:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.metrics = {}
        print("Model Trainer initialized")

    def load_dataset(self, csv_path='dataset/datasets/exercise_dataset.csv'):
        print(f"\n Loading dataset: {csv_path}")
        df = pd.read_csv(csv_path)
        print(f"    Filas: {len(df)}")
        print(f"    Columnas: {len(df.columns)}")
        print(f"    Class: {df['label'].unique()}")
        print(f"    Distribution: \n{df['label'].value_counts}")

    def prepare_features(self, df):

        exclude_cols = ['sample_id', 'exercise', 'label', 'frame_sequence', 'total_frames']
        feature_cols = [col for col in df.columns if col not in exclude_cols]

        print(f"\n Caracteristics found: {len(feature_cols)}")
        print("\n Adding caracteristic for repetition..")

        agg_features = []
        labels = []

        for sample_id in df['sampl_id'].unique():
            sample_data = df[df['sample_id'] == sample_id]
            label = sample_data['label'].iloc[0]

            features = {}
            for col in feature_cols:
                values = sample_data[col].values
                features[f'{col}_mean'] = np.mean(values)
                features[f'{col}_std'] = np.std(values)
                features[f'{col}_min'] = np.min(values)
                features[f'{col}_max'] = np.max(values)
                features[f'{col}_range'] = np.max(values) - np.min(values)

            agg_features.append(features)
            labels.append(label)

        x = pd.DataFrame(agg_features)
        y = np.array(labels)

        print(f"    Processed repetitions: {len(x)}")
        print(f"    Caracteristics generated: {len(x.columns)}")

        return x, y, list(x.columns)

def train_model(self, x, y, feauter_names):


    print("\n Model training..")

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"    Training: {len(x_train)} samples")
    print(f"    Sample: {len(x_test)} samples")

    self.scaler = StandardScaler()
    x_train_scaled = self.scaler.fit_transform(x_train)
    x_test_scaled = self.scaler.transform(x_test)

    self.model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=1
    )
    self.model.fit(x_train_scaled, y_train)

    y_pred = self.model.predict(x_test_scaled)

    self.metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'classification_report': classification_report(y_test, y_pred, output_dict=True),
        'confussion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }

    print(f"\n Accuracy: {self.metrics['accuracy']:.4f}")
    print("\n Classification report:")
    print(classification_report(y_test, y_pred))

    self.feature_names = feauter_names

    return x_train, x_test, y_train, y_test, y_pred

def analyze_feature_importance(self):
    if self.model is None:
        print("Model no trained")
        return

    importances = self.model.feature_importances_
    feature_importance = pd.DataFrame({
        'feature': self.feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False)

    print("\n Top 10 caracteristics more important:")
    print(feature_importance.head(10))

    return feature_importance

def save_model(self, model_path='models/saved/best_model.pkl'):
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    model_data = {
        'model': self.model,
        'scaler': self.scaler,
        'feature_names': self.feature_names,
        'metrics': self.metrics
    }

    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)

    print(f"\n Model saved: {model_path}")

    metrics_path = model_path.replace('.pkl', '_metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(self.metrics, f, indent=2)
    print(f" Metrics saved: {metrics_path}")

    return model_path

def main():
    print("=" *60)
    print("Training of model")
    print("=" * 60)

    trainer = ModelTrainer()

    df = trainer.load_dataset()

    x, y, feature_names = trainer.prepare_features(df)

    x_train, x_test, y_train, y_test, y_pred = trainer.train_model(x, y, feature_names)

    feature_importance = trainer.analyzer_feature_importance()

    trainer.save_model()

    print("\n" + "=" * 60)
    print("Training Complete")
    print("\n Model summary:")
    print(f"    Accuracy: {trainer.metrics['accuracy']:.4f}")
    print(f"    Caracteristics: {len(feature_names)}")
    print(f"    Samples of training: {len(x_train)}")
    print(f"    Samples of testing: {len(x_test)}")

if __name__ == "__main__":
    main()