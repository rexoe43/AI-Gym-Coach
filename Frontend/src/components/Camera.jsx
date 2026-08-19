import React, { useRef, useCallback, useState, useEffect } from 'react';
import Webcam from 'react-webcam';

const Camera = ({ onFrame, isActive }) => {
  const webcamRef = useRef(null);
  const [isCameraReady, setIsCameraReady] = useState(false);
  const [error, setError] = useState(null);
  const intervalRef = useRef(null);

  const captureFrame = useCallback(() => {
    if (webcamRef.current && isActive) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        const base64Data = imageSrc.split(',')[1];
        onFrame(base64Data);
      }
    }
  }, [isActive, onFrame]);

  useEffect(() => {
    if (isActive) {
      intervalRef.current = setInterval(captureFrame, 100);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [isActive, captureFrame]);

  const handleUserMedia = () => {
    console.log('Camera activated');
    setIsCameraReady(true);
    setError(null);
  };

  const handleError = (err) => {
    console.error('Error from camera:', err);
    setError('I cant access to camera make sure to the permissions are enabled');
    setIsCameraReady(false);
  };

  return (
    <div className="relative w-full max-w-2xl mx-auto bg-gray-800 rounded-xl overflow-hidden">
      {error ? (
        <div className="p-8 text-center text-red-400">
          <p className="text-xl">{error}</p>
          <p className="mt-2 text-sm text-gray-400">Make sure the camera is connected and the permissions are enabled.</p>
        </div>
      ) : (
        <>
          <Webcam
            ref={webcamRef}
            audio={false}
            screenshotFormat="image/jpeg"
            videoConstraints={{
              width: 640,
              height: 480,
              facingMode: "user"
            }}
            onUserMedia={handleUserMedia}
            onUserMediaError={handleError}
            className="w-full h-auto"
          />
          {!isCameraReady && (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-900/80">
              <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent mx-auto"></div>
                <p className="mt-4 text-gray-400">Starting camera...</p>
              </div>
            </div>
          )}
        </>
      )}
      {!isActive && isCameraReady && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-900/70">
          <p className="text-xl font-semibold text-gray-300">Press "Start" to begin</p>
        </div>
      )}
    </div>
  );
};

export default Camera;