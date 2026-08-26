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
  const [status, setStatus] = useState('Waiting...');
  // 'neutral' | 'correct' | 'improvable' — driven ONLY by whether a completed
  // repetition was valid, not by noisy per-frame predictions.
  const [techniqueStatus, setTechniqueStatus] = useState('neutral');
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

      // Repetitions already only counts VALID reps on the backend side.
      if (data.repetition_count !== undefined) {
        setReps(data.repetition_count);
      }

      // Technique reflects the outcome of the last COMPLETED repetition,
      // not the class of a single passing frame.
      if (data.repetition_completed) {
        setTechniqueStatus(data.repetition_is_correct ? 'correct' : 'improvable');
      }

      // Status is about detection/session state, separate from technique.
      const pred = data.prediction;
      if (pred && pred.class === 'no_detection') {
        setStatus('No body detected');
      } else if (isActive) {
        setStatus('Training');
      } else {
        setStatus('Waiting...');
      }
    }
  }, [lastMessage, isActive]);

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
    setStatus('Training');
    sendMessage({
      type: 'start_training',
      exercise: exercise
    });
  };

  const handleStop = () => {
    setIsActive(false);
    setLandmarks(null);
    setStatus('Waiting...');
  };

  const handleReset = () => {
    setReps(0);
    setStatus('Waiting...');
    setTechniqueStatus('neutral');
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
            status={status}
          />
        </div>

        <div style={{ marginBottom: '24px' }}>
          <Feedback
            techniqueStatus={techniqueStatus}
            error={!isConnected ? 'Didnt connect to the server' : null}
          />
        </div>
      </div>
    </div>
  );
}

export default App;