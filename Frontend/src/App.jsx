import React, {useState, useEffect, useRef } from 'react';
import { useWebSocket } from './hooks/useWebSocket';
import Camera from './components/Camera';
import Stats from './components/Stats';
import Feedback from './components/Feedback';
import Controls from './components/Controls';

function App(){
    const [clientId] = useState(`user_${Date.now()}`);
    const [isActive, setIsActive] = userState(false);
    const [exercise, setExercise] = useState('squat');
    const [reps, setReps] = useState(0);
    const [correctReps, setCorrectReps] = useState(0);
    const [techniqueScore, setTechniqueScore] = useState(0);
    const [status, setStatus] = useState('Waiting..');
    const [prediction, setPrediction] = useState(null);
    const [confidence, setConfidence] = useState(0);
    const [feedback, setFeedback] = useState(null);

    const wsUrl = `ws://localhost:8000/ws${clientId}`;
    const { isConnected, lastMessage, sendMessage } = useWebSocket(wsUrl);

    useEffect(() => {
        if (lastMessage) {
            const { type, data } = lastMessage;

            if (type === 'result' && data) {
                if (data.repetition_count !== undefined) {
                    setReps(data.repetition_count);
                }

                if (data.prediction) {
                    const pred = data.prediction;
                    setPrediction(pred.class);
                    setConfidence(pred.confidence || 0);

                    if(pred.class === 'correct') {
                        setStatus('Correct');
                        if (data.repetition_completed) {
                            setCorrectReps(prev => prev + 1);
                        }
                    }
                }
            }
        }
    })
}