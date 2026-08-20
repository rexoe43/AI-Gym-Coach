// frontend/src/components/Camera.jsx
import React, { useRef, useState, useEffect } from 'react';

const Camera = ({ onFrame, isActive, annotatedFrame }) => {
  const videoRef = useRef(null);
  const [isCameraReady, setIsCameraReady] = useState(false);
  const [error, setError] = useState(null);
  const intervalRef = useRef(null);
  const streamRef = useRef(null);

  // ✅ Capturar frames SIEMPRE (incluso cuando no está activo)
  useEffect(() => {
    // Siempre capturar frames para mostrar los landmarks
    intervalRef.current = setInterval(() => {
      if (videoRef.current && videoRef.current.readyState === 4) {
        const canvas = document.createElement('canvas');
        canvas.width = videoRef.current.videoWidth || 640;
        canvas.height = videoRef.current.videoHeight || 480;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoRef.current, 0, 0);
        const frameData = canvas.toDataURL('image/jpeg').split(',')[1];
        onFrame(frameData);
      }
    }, 100); // 10 fps

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [onFrame]);

  // Iniciar cámara
  useEffect(() => {
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { width: 640, height: 480, facingMode: 'user' }
        });
        
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          streamRef.current = stream;
          setIsCameraReady(true);
          setError(null);
        }
      } catch (err) {
        console.error('Error de cámara:', err);
        setError('No se pudo acceder a la cámara. Verifica los permisos.');
      }
    };

    startCamera();

    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
        streamRef.current = null;
      }
    };
  }, []);

  // ✅ SIEMPRE mostrar el frame anotado si existe (incluso sin Start)
  const showAnnotatedFrame = annotatedFrame !== null && annotatedFrame !== undefined;

  return (
    <div style={{
      position: 'relative',
      width: '100%',
      maxWidth: '640px',
      margin: '0 auto',
      backgroundColor: '#1f2937',
      borderRadius: '12px',
      overflow: 'hidden',
      aspectRatio: '4/3'
    }}>
      {error ? (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
          padding: '20px',
          textAlign: 'center',
          color: '#ef4444'
        }}>
          <p>⚠️ {error}</p>
        </div>
      ) : (
        <>
          {/* ✅ Video: visible cuando NO hay frame anotado */}
          {!showAnnotatedFrame && (
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover'
              }}
            />
          )}

          {/* ✅ Frame anotado: SIEMPRE se muestra cuando llega del backend */}
          {showAnnotatedFrame && (
            <img
              src={`data:image/jpeg;base64,${annotatedFrame}`}
              alt="Análisis en tiempo real"
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                pointerEvents: 'none',
                zIndex: 10
              }}
            />
          )}

          {/* ✅ Indicador de estado de la cámara */}
          <div style={{
            position: 'absolute',
            bottom: '10px',
            left: '10px',
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            color: isCameraReady ? '#22c55e' : '#f59e0b',
            padding: '4px 12px',
            borderRadius: '20px',
            fontSize: '12px',
            fontWeight: 'bold',
            zIndex: 30
          }}>
            {isCameraReady ? '🟢 Cámara activa' : '🟡 Iniciando...'}
          </div>

          {/* ✅ Indicador de análisis (solo cuando está activo) */}
          {isActive && (
            <div style={{
              position: 'absolute',
              top: '10px',
              right: '10px',
              backgroundColor: 'rgba(34, 197, 94, 0.9)',
              color: 'white',
              padding: '4px 12px',
              borderRadius: '20px',
              fontSize: '12px',
              fontWeight: 'bold',
              zIndex: 30
            }}>
              🟢 ANALIZANDO
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Camera;