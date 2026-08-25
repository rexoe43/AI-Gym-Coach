import React, { useState, useEffect, useCallback } from 'react';
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
  const [status, setStatus] = useState('Waiting...');
  const [prediction, setPrediction] = useState(null);
  const [confidence, setConfidence] = useState(0);
  const [landmarks, setLandmarks] = useState(null);

  const wsUrl = `ws://localhost:8000/ws/${clientId}`;
  const { isConnected, lastMessage, sendMessage } = useWebSocket(wsUrl);

  useEffect(() => {
    if (!lastMessage) return;

    const { type, data } = lastMessage;

    if (type === 'result' && data) {
      if (data.landmarks) {
        setLandmarks(data.landmarks);
      } else if (data.has_landmarks === false) {
        setLandmarks(null);
      }

      if (data.repetition_count !== undefined) {
        setReps(data.repetition_count);
      }
      if (data.correct_rep_count !== undefined) {
        setCorrectReps(data.correct_rep_count);
      }
      if (data.technique_score !== undefined) {
        setTechniqueScore(data.technique_score);
      }
      if (data.status) {
        setStatus(data.status);
      }

      if (data.prediction) {
        const pred = data.prediction;
        const label = pred.label || pred.class;
        setPrediction(label);
        setConfidence(typeof pred.confidence === 'number' ? pred.confidence : 0);
        if (!data.status && pred.status) {
          setStatus(pred.status);
        }
        if (data.technique_score === undefined && pred.technique_score !== undefined) {
          setTechniqueScore(pred.technique_score);
        }
      }
    }
  }, [lastMessage]);

  const handleFrame = useCallback((frameData) => {
    if (isActive && isConnected) {
      sendMessage({
        type: 'frame',
        data: frameData
      });
    }
  }, [isActive, isConnected, sendMessage]);

  const handleStart = () => {
    setIsActive(true);
    setLandmarks(null);
    sendMessage({
      type: 'start_training',
      exercise: exercise
    });
  };

  const handleStop = () => {
    setIsActive(false);
    setLandmarks(null);
  };

  const handleReset = () => {
    setReps(0);
    setCorrectReps(0);
    setTechniqueScore(0);
    setStatus('Waiting...');
    setPrediction(null);
    setConfidence(0);
    setLandmarks(null);

    if (isActive) {
      setIsActive(false);
    }

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
            {isConnected ? 'Connected' : 'Disconnected'}
          </p>
          <p style={{ color: '#4b5563', fontSize: '12px', marginTop: '4px' }}>ID: {clientId}</p>
        </header>

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

        <div style={{ marginBottom: '24px' }}>
          <Camera
            onFrame={handleFrame}
            isActive={isActive}
            landmarks={landmarks}
          />
        </div>

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

        <div style={{ marginBottom: '24px' }}>
          <Stats
            reps={reps}
            correctReps={correctReps}
            techniqueScore={techniqueScore}
            status={status}
          />
        </div>

        <div style={{ marginBottom: '24px' }}>
          <Feedback
            prediction={prediction}
            confidence={confidence}
            error={!isConnected ? 'Didnt connect to the server' : null}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
