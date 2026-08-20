// frontend/src/App.jsx
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
  const [status, setStatus] = useState('Esperando...');
  const [prediction, setPrediction] = useState(null);
  const [confidence, setConfidence] = useState(0);
  const [landmarks, setLandmarks] = useState(null);
  const [debugInfo, setDebugInfo] = useState('Esperando...');
  
  const wsUrl = `ws://localhost:8000/ws/${clientId}`;
  const { isConnected, lastMessage, sendMessage } = useWebSocket(wsUrl);

  // ✅ Manejar mensajes del WebSocket
  useEffect(() => {
    if (lastMessage) {
      console.log('📩 Mensaje recibido:', lastMessage);
      
      const { type, data } = lastMessage;
      
      if (type === 'result' && data) {
        if (data.landmarks) {
          setLandmarks(data.landmarks);
        } else if (data.has_landmarks === false) {
          setLandmarks(null);
        }
        
        // ✅ Actualizar repeticiones
        if (data.repetition_count !== undefined) {
          setReps(data.repetition_count);
        }
        
        // ✅ Actualizar predicción
        if (data.prediction) {
          const pred = data.prediction;
          console.log('🧠 Predicción:', pred);
          setPrediction(pred.class);
          setConfidence(pred.confidence || 0);
          
          if (pred.class === 'correct') {
            setStatus('✅ Correcto');
            if (data.repetition_completed) {
              setCorrectReps(prev => prev + 1);
            }
          } else if (pred.class === 'incomplete_range') {
            setStatus('⚠️ Mejorable');
          } else if (pred.class === 'no_detection') {
            setStatus('👤 No se detecta cuerpo');
          } else {
            setStatus('❓ Desconocido');
          }
          
          if (pred.probabilities) {
            const probCorrect = pred.probabilities.correct || 0;
            setTechniqueScore(Math.round(probCorrect * 100));
          }
        }
        
        // ✅ Actualizar estado de landmarks
        if (data.has_landmarks !== undefined) {
          setDebugInfo(data.has_landmarks ? '🟢 Landmarks detectados' : '🟡 Sin landmarks');
        }
      }
      
      if (type === 'counter_reset') {
        console.log('🔄 Contador reiniciado');
        setDebugInfo('🔄 Contador reiniciado');
      }
    }
  }, [lastMessage]);

  // ✅ Manejar frames desde la cámara
  const handleFrame = useCallback((frameData) => {
    if (isConnected) {
      sendMessage({
        type: 'frame',
        data: frameData
      });
    }
  }, [isActive, isConnected, sendMessage]);

  // ✅ Iniciar entrenamiento
  const handleStart = () => {
    console.log("▶️ Iniciando entrenamiento...");
    setIsActive(true);
    setLandmarks(null);
    setDebugInfo('🟡 Esperando frames...');
    sendMessage({
      type: 'start_training',
      exercise: exercise
    });
  };

  // ✅ Detener entrenamiento
  const handleStop = () => {
    console.log("⏹ Deteniendo entrenamiento...");
    setIsActive(false);
  };

  // ✅ Reiniciar
  const handleReset = () => {
    console.log("🔄 Reiniciando...");
    setReps(0);
    setCorrectReps(0);
    setTechniqueScore(0);
    setStatus('Esperando...');
    setPrediction(null);
    setConfidence(0);
    setLandmarks(null);
    setDebugInfo('🔄 Reiniciado');
    
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
            {isConnected ? '🟢 Conectado' : '🔴 Desconectado'}
          </p>
          <p style={{ color: '#4b5563', fontSize: '12px', marginTop: '4px' }}>ID: {clientId}</p>
          <p style={{ color: '#6b7280', fontSize: '12px', marginTop: '4px' }}>📊 {debugInfo}</p>
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
              ⚠️ Conectando al servidor... Asegúrate de que el backend esté corriendo
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
            error={!isConnected ? 'No conectado al servidor' : null}
          />
        </div>

        <div style={{ textAlign: 'center', fontSize: '14px', color: '#6b7280' }}>
          <p style={{ margin: 0 }}>
            {isConnected ? '🟢 Conectado al servidor' : '🔴 Conectando al servidor...'}
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;