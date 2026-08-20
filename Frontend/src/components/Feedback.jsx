import React from 'react';

const Feedback = ({ prediction, confidence, error }) => {
  if (!prediction && !error) {
    return (
      <div style={{
        backgroundColor: '#1f2937',
        borderRadius: '12px',
        padding: '24px',
        textAlign: 'center',
        color: '#9ca3af'
      }}>
        <p style={{ margin: 0 }}>Do exercise to get a feedback</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{
        backgroundColor: '#1f2937',
        borderRadius: '12px',
        padding: '24px',
        border: '2px solid #ef4444'
      }}>
        <p style={{ color: '#ef4444', margin: 0 }}>Error: {error}</p>
      </div>
    );
  }

  const isCorrect = prediction === 'correct';
  const confidencePercent = (confidence * 100).toFixed(1);
  const borderColor = isCorrect ? '#22c55e' : '#ef4444';

  return (
    <div style={{
      backgroundColor: '#1f2937',
      borderRadius: '12px',
      padding: '24px',
      border: `2px solid ${borderColor}`
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap'
      }}>
        <div>
          <p style={{ color: '#9ca3af', fontSize: '14px', margin: 0 }}>Technique</p>
          <p style={{
            fontSize: '24px',
            fontWeight: 'bold',
            color: isCorrect ? '#22c55e' : '#ef4444',
            margin: '4px 0 0 0'
          }}>
            {isCorrect ? 'Correct' : 'Improvable'}
          </p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <p style={{ color: '#9ca3af', fontSize: '14px', margin: 0 }}>Confidence</p>
          <p style={{
            fontSize: '24px',
            fontWeight: 'bold',
            color: '#6366f1',
            margin: '4px 0 0 0'
          }}>
            {confidencePercent}%
          </p>
        </div>
      </div>
      
      {!isCorrect && (
        <div style={{
          marginTop: '16px',
          padding: '12px',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          borderRadius: '8px',
          border: '1px solid rgba(239, 68, 68, 0.2)'
        }}>
          <p style={{ color: '#ef4444', fontSize: '14px', margin: 0 }}>
            Tip: Adjust your posture. Try to keep your back straight and lower yourself until your thighs are parallel to the floor.
          </p>
        </div>
      )}
      
      {isCorrect && (
        <div style={{
          marginTop: '16px',
          padding: '12px',
          backgroundColor: 'rgba(34, 197, 94, 0.1)',
          borderRadius: '8px',
          border: '1px solid rgba(34, 197, 94, 0.2)'
        }}>
          <p style={{ color: '#22c55e', fontSize: '14px', margin: 0 }}>
            Excelent, keep going.
          </p>
        </div>
      )}
    </div>
  );
};

export default Feedback;