from .model_loader import model_loader
from .feature_extractor import extract_features_from_landmarks

def predict_exercise(landmarks, exercise_type='squat'):
    if landmarks is None:
        return {
            'class': 'unknown',
            'confidence': 0.0,
            'probabilities': {},
            'error': 'Landmarks undetected'
        }

    features = extract_features_from_landmarks(landmarks)

    if features is None:
        return {
            'class': 'unknown',
            'confidence': 0.0,
            'probabilities': {},
            'error': 'Error extracting caracteristics'
        }
    
    try:
        result = model_loader.predict(features)
        return result
    except Exception as e:
        return {
            'class': 'unknown',
            'confidence': 0.0,
            'probabilities': {},
            'error': str(e)
        }