import React, { useRef, useState, useEffect } from 'react';

const POSE_CONNECTIONS = [
  [0, 1], [1, 2], [2, 3], [3, 7],
  [0, 4], [4, 5], [5, 6], [6, 8],
  [9, 10],
  [11, 12], [11, 13], [13, 15], [15, 17], [15, 19], [15, 21], [17, 19],
  [12, 14], [14, 16], [16, 18], [16, 20], [16, 22], [18, 20],
  [11, 23], [12, 24], [23, 24], [23, 25], [24, 26], [25, 27], [26, 28],
  [27, 29], [28, 30], [29, 31], [30, 32], [27, 31], [28, 32],
];

const mapLandmark = (lm, video, canvas) => {
  const vw = video.videoWidth || 640;
  const vh = video.videoHeight || 480;
  const cw = canvas.width;
  const ch = canvas.height;
  const scale = Math.max(cw / vw, ch / vh);
  const offsetX = (cw - vw * scale) / 2;
  const offsetY = (ch - vh * scale) / 2;
  return {
    x: lm.x * vw * scale + offsetX,
    y: lm.y * vh * scale + offsetY,
    visible: (lm.visibility ?? 1) > 0.5,
  };
};

const Camera = ({ onFrame, isActive, landmarks }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const [isCameraReady, setIsCameraReady] = useState(false);
  const [error, setError] = useState(null);
  const intervalRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    if (!isActive) {
      return undefined;
    }

    intervalRef.current = setInterval(() => {
      if (videoRef.current && videoRef.current.readyState === 4) {
        const canvas = document.createElement('canvas');
        canvas.width = videoRef.current.videoWidth || 640;
        canvas.height = videoRef.current.videoHeight || 480;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoRef.current, 0, 0);
        onFrame(canvas.toDataURL('image/jpeg').split(',')[1]);
      }
    }, 100);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [isActive, onFrame]);

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
        console.error('Error de camara:', err);
        setError('No se pudo acceder a la camara. Verifica los permisos.');
      }
    };

    startCamera();

    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
      }
    };
  }, []);

  useEffect(() => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const ctx = canvas.getContext('2d');
    const { width, height } = container.getBoundingClientRect();
    canvas.width = width;
    canvas.height = height;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!isActive || !landmarks?.length || !video) {
      return;
    }

    const points = landmarks.map((lm) => mapLandmark(lm, video, canvas));

    ctx.lineWidth = 3;
    ctx.strokeStyle = '#22c55e';
    ctx.fillStyle = '#6366f1';

    POSE_CONNECTIONS.forEach(([a, b]) => {
      const pa = points[a];
      const pb = points[b];
      if (!pa?.visible || !pb?.visible) return;
      ctx.beginPath();
      ctx.moveTo(pa.x, pa.y);
      ctx.lineTo(pb.x, pb.y);
      ctx.stroke();
    });

    points.forEach((p) => {
      if (!p.visible) return;
      ctx.beginPath();
      ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
      ctx.fill();
    });
  }, [landmarks, isActive]);

  return (
    <div
      ref={containerRef}
      style={{
        position: 'relative',
        width: '100%',
        maxWidth: '640px',
        margin: '0 auto',
        backgroundColor: '#1f2937',
        borderRadius: '12px',
        overflow: 'hidden',
        aspectRatio: '4/3'
      }}
    >
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
          <p>{error}</p>
        </div>
      ) : (
        <>
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              transform: 'scaleX(-1)',
              opacity: isActive ? 1 : 0.6
            }}
          />

          <canvas
            ref={canvasRef}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              pointerEvents: 'none',
              transform: 'scaleX(-1)',
              zIndex: 10
            }}
          />

          {!isActive && (
            <div style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: 'rgba(17, 24, 39, 0.7)',
              color: '#9ca3af',
              fontSize: '20px',
              fontWeight: 'bold',
              zIndex: 20
            }}>
              Press Start to begin
            </div>
          )}

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
            {isCameraReady ? 'Camera ready' : 'Starting...'}
          </div>

          {isActive && (
            <div style={{
              position: 'absolute',
              top: '10px',
              right: '10px',
              backgroundColor: landmarks?.length ? 'rgba(34, 197, 94, 0.9)' : 'rgba(234, 179, 8, 0.9)',
              color: 'white',
              padding: '4px 12px',
              borderRadius: '20px',
              fontSize: '12px',
              fontWeight: 'bold',
              zIndex: 30
            }}>
              {landmarks?.length ? 'ANALYZING' : 'WAITING...'}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Camera;
