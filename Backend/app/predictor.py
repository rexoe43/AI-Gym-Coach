# backend/app/predictor.py
from .model_loader import model_loader
from .feature_extractor import extract_features_from_landmarks, score_squat_technique

def predict_exercise(landmarks, exercise_type='squat'):
    default_result = {
        'class': 'unknown',
        'confidence': 0.0,
        'probabilities': {'correct': 0.0, 'incomplete_range': 0.0},
        'error': None
    }
    
    if landmarks is None:
        default_result['class'] = 'no_landmarks'
        default_result['error'] = 'No se detectaron landmarks'
        return default_result
    
    try:
        features = extract_features_from_landmarks(landmarks)
        
        if features is None:
            default_result['class'] = 'no_features'
            default_result['error'] = 'Error extracting caracteristics'
            return default_result
        
        # Fallback: if the trained model isn't loaded (no best_model.pkl found),
        # use the geometric heuristic in feature_extractor.py instead of
        # returning a flat 'no_model' / 0.0 confidence every time.
        if model_loader is None or not model_loader.is_loaded:
            return score_squat_technique(features, landmarks)
        
        result = model_loader.predict(features)
        
        if not isinstance(result, dict):
            default_result['error'] = f'Inespered Result: {type(result)}'
            return default_result
        
        if 'class' not in result:
            result['class'] = 'unknown'
        if 'confidence' not in result:
            result['confidence'] = 0.0
        if 'probabilities' not in result:
            result['probabilities'] = {'correct': 0.0, 'incomplete_range': 0.0}
        
        return result
        
    except Exception as e:
        print(f" Error in predict_exercise: {e}")
        default_result['class'] = 'error'
        default_result['error'] = str(e)
        return default_result