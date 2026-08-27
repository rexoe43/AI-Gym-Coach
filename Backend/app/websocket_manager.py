from typing import Dict, List

import base64
import cv2
import numpy as np

from .feature_extractor import extract_raw_angles
from .pose_detector import pose_detector
from .predictor import predict_repetition
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

            results = {
                'has_landmarks': bool(landmarks),
                'landmarks': landmarks,
                'prediction': None,
                'repetition_count': repetition_counter.count,
                'exercise': 'squat',
            }

            if not landmarks:
                results['prediction'] = {
                    'class': 'no_detection',
                    'confidence': 0.0,
                    'probabilities': {},
                    'error': 'No se detecto el cuerpo',
                }
                return results

            try:
                raw_angles = extract_raw_angles(landmarks)

                if raw_angles:
                    session = self.training_sessions.get(client_id, {})
                    exercise_type = session.get('exercise', repetition_counter.exercise_type)

                    rep_result = repetition_counter.update(landmarks, raw_angles)
                    results['repetition_count'] = repetition_counter.count
                    results['exercise'] = exercise_type

                    if rep_result['completed']:
                        # Classify the WHOLE repetition now, using the 90
                        # aggregated features the exercise's model was
                        # trained on — not a single frame.
                        classification = predict_repetition(rep_result['raw_series'], exercise_type)
                        results['repetition_completed'] = True
                        results['repetition_is_correct'] = (
                            classification.get('class') == 'correct'
                        )
                        results['repetition_confidence'] = classification.get('confidence', 0.0)

            except Exception as e:
                print(f'Error en landmarks: {e}')
                results['prediction'] = {
                    'class': 'processing_error',
                    'confidence': 0.0,
                    'probabilities': {},
                    'error': str(e),
                }

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