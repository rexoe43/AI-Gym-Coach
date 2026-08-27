# backend/app/predictor.py
from .model_loader import model_loader
from .feature_extractor import build_repetition_feature_vector

MIN_FRAMES_FOR_PREDICTION = 3


def _fallback_repetition_score(raw_series, exercise_type):
    """
    Used only if the exercise's model isn't loaded. Simple geometric
    heuristic over the whole repetition instead of a flat 0.0 confidence.
    """
    if exercise_type == 'pushup':
        depth_values = raw_series.get('elbow_angle_right', [])
        depth_min = min(depth_values) if depth_values else 180.0
        good_depth = depth_min <= 100  # elbow bent enough at the bottom
    else:  # squat (default)
        depth_values = raw_series.get('knee_angle_right', [])
        depth_min = min(depth_values) if depth_values else 180.0
        good_depth = depth_min <= 100

    torso_values = raw_series.get('torso_angle', [])
    torso_mean = (sum(torso_values) / len(torso_values)) if torso_values else 0.0
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
    vector the exercise-specific model was trained on. Picks the right
    model (squat vs pushup) via model_loader.get(exercise_type).
    """
    default_result = {
        'class': 'unknown',
        'confidence': 0.0,
        'probabilities': {'correct': 0.0, 'incomplete_range': 0.0},
        'error': None,
    }

    primary_joint = 'elbow_angle_right' if exercise_type == 'pushup' else 'knee_angle_right'

    if not raw_series or len(raw_series.get(primary_joint, [])) < MIN_FRAMES_FOR_PREDICTION:
        default_result['error'] = 'Repeticion demasiado corta para clasificar'
        return default_result

    try:
        model = model_loader.get(exercise_type)

        if model is None or not model.is_loaded:
            return _fallback_repetition_score(raw_series, exercise_type)

        feature_vector = build_repetition_feature_vector(raw_series, exercise_type)
        result = model.predict(feature_vector)

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
        print(f"[MODEL:{exercise_type}] repetition result -> {result}")

        return result

    except Exception as e:
        print(f" Error in predict_repetition ({exercise_type}): {e}")
        default_result['class'] = 'error'
        default_result['error'] = str(e)
        return default_result