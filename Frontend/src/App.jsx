import React, { useState, useEffect } from 'react';
import { useWebSocket } from './hooks/useWebSocket';
import Camera from './components/Camera';
import Stats from './components/Stats';
import Feedback from './components/Feedback';
import Controls from './components/Controls';

function App() {
  const [clientId] = useState(`user_${Date.now()}`);
  const [isActive, setIsActive] = useState(false);
  const [exercise, setExercise] = useState('squat');
  const [reps, setReps] = useState(0);
  const [correctReps, setCorrectReps] = useState(0);
  const [techniqueScore, setTechniqueScore] = useState(0);
  const [status, setStatus] = useState('Esperando...');
  const [prediction, setPrediction] = useState(null);
  const [confidence, setConfidence] = useState(0);  
  const [annotatedFrame, setAnnotatedFrame] = useState(null);

  const wsUrl = `ws://localhost:8000/ws/${clientId}`;
  const { isConnected, lastMessage, sendMessage } = useWebSocket(wsUrl);

  useEffect(() => {
    if (lastMessage) {
      const { type, data } = lastMessage;
      
      if (type === 'result' && data) {
        if (data.frame) {
          setAnnotatedFrame(data.frame);
        }
        
        if (data.prediction) {
          const pred = data.prediction;
          setPrediction(pred.class);
          setConfidence(pred.confidence || 0);
          
          if (pred.class === 'correct') {
            setStatus('Correct');
            if (data.repetition_completed) {
              setCorrectReps(prev => prev + 1);
            }
          } else if (pred.class === 'incomplete_range') {
            setStatus('Improvable');
          } else {
            setStatus('Unknown');
          }
          
          if (pred.probabilities) {
            const probCorrect = pred.probabilities.correct || 0;
            setTechniqueScore(Math.round(probCorrect * 100));
          }
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
    console.log("Starting training..");
    setIsActive(true);
    sendMessage({
      type: 'start_training',
      exercise: exercise
    });
  };

  const handleStop = () => {
    console.log("Stopping training...")
    setIsActive(false);
  };

  const handleReset = () => {
    console.log("Restarting counter..")
    setReps(0);
    setCorrectReps(0);
    setTechniqueScore(0);
    setStatus('Esperando...');
    setPrediction(null);
    setConfidence(0);
    sendMessage({
      type: 'reset_counter'
    });
  };

 return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#111827',
      color: 'white',
      padding: '16px'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {/* Header */}
        <header style={{ textAlign: 'center', marginBottom: '32px' }}>
          <h1 style={{
            fontSize: '48px',
            fontWeight: 'bold',
            background: 'linear-gradient(to right, #6366f1, #a855f7)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            margin: 0
          }}>
            AI GYM COACH
          </h1>
          <p style={{ color: '#9ca3af', marginTop: '8px' }}>
            {isConnected ? 'Connected' : 'Desconnected'}
          </p>
          <p style={{ color: '#4b5563', fontSize: '12px', marginTop: '4px' }}>ID: {clientId}</p>
        </header>

        <div style={{ marginBottom: '24px'}}>
            <Camera
                onFrame={handleFrame}
                iSActive={isActive}
                annotatedFrame={annotatedFrame}
            />
        </div>

        {/* Connection status alert */}
        {!isConnected && (
          <div style={{
            backgroundColor: 'rgba(234, 179, 8, 0.1)',
            border: '1px solid rgba(234, 179, 8, 0.5)',
            borderRadius: '12px',
            padding: '16px',
            marginBottom: '16px',
            textAlign: 'center'
          }}>
            <p style={{ color: '#f59e0b', margin: 0 }}>
              Connecting to the server, please verify if the backend is running
            </p>
          </div>
        )}

        {/* Camera */}
        <div style={{ marginBottom: '24px' }}>
          <Camera 
            onFrame={handleFrame}
            isActive={isActive}
          />
        </div>

        {/* Controls */}
        <div style={{ marginBottom: '24px' }}>
          <Controls
            isActive={isActive}
            onStart={handleStart}
            onStop={handleStop}
            onReset={handleReset}
            exercise={exercise}
            onExerciseChange={setExercise}
          />
        </div>

        {/* Stats */}
        <div style={{ marginBottom: '24px' }}>
          <Stats
            reps={reps}
            correctReps={correctReps}
            techniqueScore={techniqueScore}
            status={status}
          />
        </div>

        {/* Feedback */}
        <div style={{ marginBottom: '24px' }}>
          <Feedback
            prediction={prediction}
            confidence={confidence}
            error={!isConnected ? 'Didnt connect to the server' : null}
          />
        </div>

        {/* Connection status */}
        <div style={{ textAlign: 'center', fontSize: '14px', color: '#6b7280' }}>
          <p style={{ margin: 0 }}>
            {isConnected ? (
              'Connected to the server'
            ) : (
              ' Connecting to the server...'
            )}
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;