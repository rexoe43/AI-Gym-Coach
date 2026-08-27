import React from 'react';

const Feedback = ({ techniqueStatus, error }) => {
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

  //  set only when a repetition actually completes.
  const config = {
    neutral: { label: '-', color: '#9ca3af', border: '#374151', tip: null },
    correct: {
      label: 'Correct',
      color: '#22c55e',
      border: '#22c55e',
      tip: { text: 'Excelent, keep going.', bg: 'rgba(34, 197, 94, 0.1)', fg: '#22c55e', borderColor: 'rgba(34, 197, 94, 0.2)' },
    },
    improvable: {
      label: 'Improvable',
      color: '#ef4444',
      border: '#ef4444',
      tip: {
        text: 'Tip: Adjust your posture. Try to keep your back straight and lower yourself until your thighs are parallel to the floor.',
        bg: 'rgba(239, 68, 68, 0.1)',
        fg: '#ef4444',
        borderColor: 'rgba(239, 68, 68, 0.2)',
      },
    },
  };

  const current = config[techniqueStatus] || config.neutral;

  return (
    <div style={{
      backgroundColor: '#1f2937',
      borderRadius: '12px',
      padding: '24px',
      border: `2px solid ${current.border}`
    }}>
      <div>
        <p style={{ color: '#9ca3af', fontSize: '14px', margin: 0 }}>Technique</p>
        <p style={{
          fontSize: '24px',
          fontWeight: 'bold',
          color: current.color,
          margin: '4px 0 0 0'
        }}>
          {current.label}
        </p>
      </div>

      {current.tip && (
        <div style={{
          marginTop: '16px',
          padding: '12px',
          backgroundColor: current.tip.bg,
          borderRadius: '8px',
          border: `1px solid ${current.tip.borderColor}`
        }}>
          <p style={{ color: current.tip.fg, fontSize: '14px', margin: 0 }}>
            {current.tip.text}
          </p>
        </div>
      )}
    </div>
  );
};

export default Feedback;