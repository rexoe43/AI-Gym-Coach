import pickle
import os
import numpy as np

class ModelLoader:

    def __init__(self, model_path='models/saved/best_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.classes = None
        self.load_model()

    def load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model no found in: {self.model_path}")

        with open(self.model_path, 'rb') as f:
            data = pickle.load(f)

        self.model = data['model']
        self.scaler = data['scaler']
        self.feature_names = data['feature_names']
        self.classes = self.model.classes_

        print(f"Model loading correctly")
        print(f"    Class: {self.classes}")
        print(f"    Caracteristics: {len(self.feature_names)}")

        return self.model

    def predict(self, features):
        if self.model is None:
            raise ValueError("Model no charged")

        if isinstance(features, dict):
            feature_array = []
            for name in self.feature_names:
                feature_array.append(features.get(name, 0))
            features = np.array(feature_array).reshape(1, -1)
        elif isinstance(features, list):
            features = np.array(features).reshape(1, -1)

        features_scaled = self.scaler.transform(features)

        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]

        probs_dict = {}
        for i, class_name in enumerate(self.classes):
            probs_dict[class_name] = float(probabilities[i])

        return {
            'class': prediction,
            'probabilities:': probs_dict,
            'confidence': float(max(probabilities))
        }

model_loader = ModelLoader()