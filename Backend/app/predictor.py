# backend/app/predictor.py
from .model_loader import model_loader
from .feature_extractor import build_repetition_feature_vector

MIN_FRAMES_FOR_PREDICTION = 3


def _fallback_repetition_score(raw_series):
    """
    Used only if best_model.pkl isn't loaded. Simple geometric heuristic
    over the whole repetition instead of a flat 0.0 confidence.
    """
    knee_values = raw_series.get('knee_angle_right', [])
    torso_values = raw_series.get('torso_angle', [])

    knee_min = min(knee_values) if knee_values else 180.0
    torso_mean = (sum(torso_values) / len(torso_values)) if torso_values else 0.0

    good_depth = knee_min <= 100
    good_torso = torso_mean < 40
    is_correct = good_depth and good_torso

    return {
        'class': 'correct' if is_correct else 'incomplete_range',
        'confidence': 0.5,
        'probabilities': {
            'correct': 1.0 if is_correct else 0.0,
            'incomplete_range': 0.0 if is_correct else 1.0,
        },
        'error': None,
    }


def predict_repetition(raw_series, exercise_type='squat'):
    """
    Classifies ONE COMPLETE repetition using the aggregated 90-feature
    vector the model was actually trained on (see training_model.py).
    This replaces the old per-frame predict_exercise() for correctness
    judgments — a single frame never carried enough information for this
    model to work with.
    """
    default_result = {
        'class': 'unknown',
        'confidence': 0.0,
        'probabilities': {'correct': 0.0, 'incomplete_range': 0.0},
        'error': None,
    }

    if not raw_series or len(raw_series.get('knee_angle_right', [])) < MIN_FRAMES_FOR_PREDICTION:
        default_result['error'] = 'Repeticion demasiado corta para clasificar'
        return default_result

    try:
        if model_loader is None or not model_loader.is_loaded:
            return _fallback_repetition_score(raw_series)

        feature_vector = build_repetition_feature_vector(raw_series)
        result = model_loader.predict(feature_vector)

        if not isinstance(result, dict):
            default_result['error'] = f'Inespered Result: {type(result)}'
            return default_result

        if 'class' not in result:
            result['class'] = 'unknown'
        if 'confidence' not in result:
            result['confidence'] = 0.0
        if 'probabilities' not in result:
            result['probabilities'] = {'correct': 0.0, 'incomplete_range': 0.0}

        # TEMP DEBUG: confirm the real per-repetition classification.
        print(f"[MODEL] repetition result -> {result}")

        return result

    except Exception as e:
        print(f" Error in predict_repetition: {e}")
        default_result['class'] = 'error'
        default_result['error'] = str(e)
        return default_result