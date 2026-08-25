from typing import Dict, List

import base64
import cv2
import numpy as np

from .feature_extractor import extract_features_from_landmarks, active_knee_angle
from .pose_detector import pose_detector
from .predictor import predict_exercise
from .repetition_counter import repetition_counter


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, List] = {}
        self.training_sessions: Dict[str, Dict] = {}
        print('WebSocket Manager initialized')

    async def connect(self, websocket, client_id: str):
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)
        await websocket.accept()
        print(f'Client {client_id} connected')

    async def disconnect(self, websocket, client_id: str):
        if client_id in self.active_connections:
            if websocket in self.active_connections[client_id]:
                self.active_connections[client_id].remove(websocket)
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]
        print(f'Client {client_id} disconnected')

    async def process_frame(self, frame_data, client_id: str):
        try:
            frame_bytes = base64.b64decode(frame_data)
            nparr = np.frombuffer(frame_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is None:
                return {'error': 'No se pudo decodificar el frame'}

            landmarks = pose_detector.process_frame(frame)
            prediction = predict_exercise(landmarks)

            results = {
                'has_landmarks': bool(landmarks),
                'landmarks': landmarks,
                'prediction': prediction,
                'repetition_count': repetition_counter.count,
                'correct_rep_count': repetition_counter.correct_count,
                'technique_score': prediction.get('technique_score', 0),
                'status': prediction.get('status', 'Waiting...'),
                'exercise': 'squat',
            }

            if not landmarks:
                return results

            features = extract_features_from_landmarks(landmarks)
            if features:
                knee_angle = active_knee_angle(features, landmarks)
                torso_angle = features.get('torso_angle', 0)
                completed = repetition_counter.update(landmarks, knee_angle, torso_angle)
                results['repetition_count'] = repetition_counter.count
                results['correct_rep_count'] = repetition_counter.correct_count
                if completed:
                    results['repetition_completed'] = True
                    if repetition_counter.count > 0:
                        results['technique_score'] = repetition_counter.average_score
                elif repetition_counter.count > 0:
                    live = prediction.get('technique_score', 0)
                    results['technique_score'] = int(round(
                        0.6 * repetition_counter.average_score + 0.4 * live
                    ))

            if client_id not in self.training_sessions:
                self.training_sessions[client_id] = {
                    'landmarks_history': [],
                    'predictions_history': [],
                }
            history = self.training_sessions[client_id]['predictions_history']
            history.append(prediction)
            if len(history) > 120:
                del history[:-60]

            return results

        except Exception as e:
            print(f'Error: {e}')
            import traceback
            traceback.print_exc()
            return {'error': str(e)}

    async def broadcast(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            for connection in self.active_connections[client_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f'Error: {e}')


websocket_manager = WebSocketManager()
