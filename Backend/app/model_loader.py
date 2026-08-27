import pickle
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]

# One filename per exercise. 'squat' keeps the original best_model.pkl name
# for backward compatibility; each new exercise gets its own file so
# training one never overwrites another.
MODEL_FILENAMES = {
    'squat': 'best_model.pkl',
    'pushup': 'best_model_pushup.pkl',
}


class SingleModel:
    """Holds one trained model (squat OR pushup) + its scaler/feature names."""

    def __init__(self, exercise, filename):
        self.exercise = exercise
        self.filename = filename
        self.model = None
        self.scaler = None
        self.feature_names = []
        self.classes = ['correct', 'incomplete_range']
        self.is_loaded = False
        self.model_path = None
        self.load_model()

    def _candidate_paths(self):
        yield REPO_ROOT / 'ai' / 'models' / 'saved' / self.filename
        yield REPO_ROOT / 'Backend' / 'models' / 'saved' / self.filename
        yield REPO_ROOT / 'models' / 'saved' / self.filename

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
                print(f"[{self.exercise}] Modelo no encontrado ({self.filename}) - "
                      f"predicciones desactivadas hasta que exista ese archivo")
                self.is_loaded = False
                return

            self.model_path = found
            print(f'[{self.exercise}] Cargando modelo desde: {found}')

            with open(found, 'rb') as f:
                data = pickle.load(f)

            self.model = data['model']
            self.scaler = data.get('scaler')
            self.feature_names = data.get('feature_names', [])
            if hasattr(self.model, 'classes_'):
                self.classes = [str(c) for c in self.model.classes_]
            self.is_loaded = True

            print(f'[{self.exercise}] Modelo cargado correctamente')
            print(f'   Clases: {self.classes}')
            print(f'   Caracteristicas: {len(self.feature_names)}')

        except Exception as e:
            print(f'[{self.exercise}] Error cargando modelo: {e}')
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
            print(f'[{self.exercise}] Error en predict: {e}')
            return self._unavailable_result(str(e))


class MultiExerciseModelLoader:
    """
    Loads one SingleModel per known exercise at startup. Kept under the
    same name/interface (`model_loader`) so existing imports still work —
    just call model_loader.get(exercise) to fetch the right one.
    """

    def __init__(self):
        self.models = {
            exercise: SingleModel(exercise, filename)
            for exercise, filename in MODEL_FILENAMES.items()
        }

    def get(self, exercise):
        return self.models.get(exercise)

    def is_loaded(self, exercise):
        model = self.models.get(exercise)
        return bool(model and model.is_loaded)

    # Backward-compat shims so old code checking model_loader.model /
    # model_loader.is_loaded (singular, squat-only) doesn't break.
    @property
    def model(self):
        squat = self.models.get('squat')
        return squat.model if squat else None


model_loader = MultiExerciseModelLoader()