import React, {useState, useEffect, useRef } from 'react';
import { useWebSocket } from './hooks/useWebSocket';
import Camera from './components/Camera';
import Stats from './components/Stats';
import Feedback from './components/Feedback';
import Controls from './components/Controls';

function App(){
    const [clientId] = useState(`user_${Date.now()}`);
    const [isActive, setIsActive] = useState(false);
    const [exercise, setExercise] = useState('squat');
    const [reps, setReps] = useState(0);
    const [correctReps, setCorrectReps] = useState(0);
    const [techniqueScore, setTechniqueScore] = useState(0);
    const [status, setStatus] = useState('Waiting..');
    const [prediction, setPrediction] = useState(null);
    const [confidence, setConfidence] = useState(0);
    const [feedback, setFeedback] = useState(null);

    const wsUrl = `ws://localhost:8000/ws/${clientId}`;
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
                    } else if (pred.class === 'incomplete_range') {
                        setStatus('Improvable')
                    } else {
                        setStatus('Unknown');
                    }

                    if (pred.probabilities) {
                        const probCorrect = pred.probabilities.correct || 0;
                        setTechniqueScore(Math.round(probCorrect * 100));
                    }
                }

                if (data.feedback) {
                    setFeedback(data.feedback);
                }
            }
        }
    }, [lastMessage]);

    const handleFrame = (frameData) => {
        if (isActive && isConnected) {
            sendMessage({
                type: 'frame',
                data: frameData
            });
        }
    };

    const handleStart = () => {
        setIsActive(true);
        sendMessage({
            type: 'start_training',
            exercise: exercise
        });
    };

    const handleStop = () => {
        setIsActive(false);
        sendMessage({
            type: 'stop_training'
        });
    };

    const handleReset = () => {
         setReps(0);
         setCorrectReps(0);
         setTechniqueScore(0);
         setStatus('Waiting...');
         setPrediction(null);
         setConfidence(0);
         sendMessage({
            type: 'reset_counter'
         });

    };

    return (
        <div className="min-h-screen bg-gray-900 text-white p-4 md:p-8">
            <div className="max-w-6x1 mx-auto">
                {/*Header*/}
                <header className="text-center mb-8">
                    <h1 className="text-4x1 font-bold bg-gradient-to-r from-primary to-purple-500 bg-clip-text text-transparent">
                        AI GYM COACH
                        </h1>
                        <p className="text-gray-400 mt-2">
                            {isConnected ? 'Conected' : 'Desconected'}
                        </p>
                        <p className="text-xs text-gray-600 mt-1">ID: {clientId}</p>
                </header>

                {/*Camera Section*/}
                <div className="mb-6">
                    <Camera>
                        onFrame={handleFrame}
                        isActive={isActive}
                    </Camera>
                </div>

                {/* Controls*/}
                <div className="mb-6">
                    <Controls>
                        isActive={isActive}
                        onStart={handleStart}
                        onStop={handleStop}
                        onReset={handleReset}
                        exercise={exercise}
                        onExerciseCHange={setExercise}
                    </Controls>
                </div>

                {/*Stats*/}
                <div className="mb-6">
                    <Stats>
                        reps={reps}
                        correctReps={correctReps}
                        techniqueScore={techniqueScore}
                        status={status}
                    </Stats>
                </div>

                {/*Feedback*/}
                <div className="mb-6">
                    <Feedback>
                        prediction={prediction}
                        confidence={confidence}
                        error={!isConnected ? 'No connected to the server' : null}
                    </Feedback>
                </div>

                {/*Connection Status*/}
                <div className="text-center text-sm text-gray-500">
                    <p>
                        {isConnected ? (
                            'Connected to the server'
                        ): (
                            'Connecting to the server...'
                        )}
                    </p>
                </div>
            </div>
        </div>
    );

}

export default App;