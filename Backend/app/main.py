from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import base64

from .websocket_manager import websocket_manager
from .model_loader import model_loader

app = FastAPI(title="AI Gym Coach")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "AI GYm Coach", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": model_loader.model is not None}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket_manager.connect(websocket, client_id)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get('type') == 'frame':
                frame_data = message.get('data')
                results = await websocket_manager.process_frame(frame_data, client_id)

                await websocket.send_json({
                    'type': 'result',
                    'data': results
                })

            elif message.get('type') == 'start_training':
                exercise = message.get('exercise', 'squat')
                websocket_manager.training_sessions[client_id] = {
                    'exercise': exercise,
                    'repetition_counter': 0,
                    'started': True
                }
                await websocket.send_json({
                    'type': 'training_started',
                    'exercise': exercise
                })

            elif message.get('type') == 'reset_counter':
                from .repetition_counter import repetition_counter
                repetition_counter.reset()
                await websocket.send_json({
                    'type': 'counter_rest',
                    'count': 0
                })

    except WebSocketDisconnect:
        await websocket_manager.disconnect(websocket, client_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
