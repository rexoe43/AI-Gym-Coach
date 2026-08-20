import pickle
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]


class ModelLoader:
    def __init__(self, model_path=None):
        self.model_path = Path(model_path) if model_path else None
        self.model = None
        self.scaler = None
        self.feature_names = []
        self.classes = ['correct', 'incomplete_range']
        self.is_loaded = False
        self.load_model()

    def _candidate_paths(self):
        if self.model_path:
            yield Path(self.model_path)
        yield REPO_ROOT / 'ai' / 'models' / 'saved' / 'best_model.pkl'
        yield REPO_ROOT / 'Backend' / 'models' / 'saved' / 'best_model.pkl'
        yield REPO_ROOT / 'models' / 'saved' / 'best_model.pkl'

    def _unavailable_result(self, error):
        return {
            'class': 'no_model',
            'confidence': 0.0,
            'probabilities': {'correct': 0.0, 'incomplete_range': 0.0},
            'error': error,
        }

    def load_model(self):
        try:
            found = None
            for path in self._candidate_paths():
                if path.exists():
                    found = path
                    break

            if found is None:
                print('Modelo no encontrado - predicciones desactivadas hasta que exista best_model.pkl')
                self.is_loaded = False
                return

            self.model_path = found
            print(f'Cargando modelo desde: {found}')

            with open(found, 'rb') as f:
                data = pickle.load(f)

            self.model = data['model']
            self.scaler = data.get('scaler')
            self.feature_names = data.get('feature_names', [])
            if hasattr(self.model, 'classes_'):
                self.classes = [str(c) for c in self.model.classes_]
            self.is_loaded = True

            print('Modelo cargado correctamente')
            print(f'   Clases: {self.classes}')
            print(f'   Caracteristicas: {len(self.feature_names)}')

        except Exception as e:
            print(f'Error cargando modelo: {e}')
            self.is_loaded = False

    def predict(self, features):
        if not self.is_loaded or self.model is None:
            return self._unavailable_result('Modelo no disponible')

        try:
            if isinstance(features, dict):
                if self.feature_names:
                    feature_array = [features.get(name, 0) for name in self.feature_names]
                else:
                    feature_array = list(features.values())
                features_array = np.array(feature_array, dtype=float).reshape(1, -1)
            elif isinstance(features, list):
                features_array = np.array(features, dtype=float).reshape(1, -1)
            elif isinstance(features, np.ndarray):
                features_array = features.reshape(1, -1) if features.ndim == 1 else features
            else:
                return self._unavailable_result(f'Tipo de features no soportado: {type(features)}')

            features_scaled = (
                self.scaler.transform(features_array)
                if self.scaler is not None
                else features_array
            )

            prediction = self.model.predict(features_scaled)[0]
            probabilities = self.model.predict_proba(features_scaled)[0]

            probs_dict = {
                str(class_name): float(probabilities[i])
                for i, class_name in enumerate(self.classes)
            }

            return {
                'class': str(prediction),
                'probabilities': probs_dict,
                'confidence': float(max(probabilities)),
                'error': None,
            }

        except Exception as e:
            print(f'Error en predict: {e}')
            return self._unavailable_result(str(e))


model_loader = ModelLoader()
