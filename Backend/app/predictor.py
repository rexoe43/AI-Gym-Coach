from .feature_extractor import extract_features_from_landmarks, score_squat_technique
from .model_loader import model_loader


def _model_usable():
    if not getattr(model_loader, 'is_loaded', False):
        return False
    names = model_loader.feature_names or []
    if any(str(name).endswith(('_mean', '_std', '_min', '_max', '_range')) for name in names):
        return False
    return True


def predict_exercise(landmarks, exercise_type='squat'):
    default_result = {
        'class': 'unknown',
        'label': 'unknown',
        'confidence': 0.0,
        'probabilities': {'correct': 0.0, 'incomplete_range': 0.0},
        'technique_score': 0,
        'status': 'Waiting...',
        'error': None,
    }

    if landmarks is None:
        default_result['class'] = 'no_landmarks'
        default_result['label'] = 'no_landmarks'
        default_result['status'] = 'No body detected'
        default_result['error'] = 'No se detectaron landmarks'
        return default_result

    try:
        features = extract_features_from_landmarks(landmarks)
        if features is None:
            default_result['class'] = 'no_features'
            default_result['label'] = 'no_features'
            default_result['status'] = 'No features'
            default_result['error'] = 'Error extracting characteristics'
            return default_result

        heuristic = score_squat_technique(features, landmarks)

        if _model_usable():
            model_result = model_loader.predict(features)
            if isinstance(model_result, dict) and model_result.get('class') not in (None, 'no_model'):
                heuristic['class'] = str(model_result.get('class', heuristic['class']))
                heuristic['label'] = heuristic['class']
                if model_result.get('confidence') is not None:
                    heuristic['confidence'] = float(model_result['confidence'])
                if model_result.get('probabilities'):
                    heuristic['probabilities'] = model_result['probabilities']
                    correct_prob = float(model_result['probabilities'].get('correct', 0) or 0)
                    heuristic['technique_score'] = int(round(correct_prob * 100))

        return heuristic

    except Exception as e:
        print(f'Error in predict_exercise: {e}')
        default_result['class'] = 'error'
        default_result['label'] = 'error'
        default_result['status'] = 'Error'
        default_result['error'] = str(e)
        return default_result
