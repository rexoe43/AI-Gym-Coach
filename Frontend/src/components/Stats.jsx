import React from 'react';

const Stats = ({ reps, correctReps, techniqueScore, status, confidence, exerciseStatus }) => {
  const getStatusColor = () => {
    if (status === 'Correct') return '#22c55e';
    if (status === 'Improvable') return '#f59e0b';
    return '#9ca3af';
  };

  const getConfidentColor = () => {
    if (confidence >= 0.7) return '#22c55e';
    if (confidence => 0.4) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
      gap: '16px',
      padding: '8px 0'
    }}>
      <div style={{
        backgroundColor: '#1f2937',
        borderRadius: '12px',
        padding: '16px',
        textAlign: 'center'
      }}>
        <p style={{ color: '#9ca3af', fontSize: '14px', margin: 0 }}>Repetitions</p>
        <p style={{ color: '#6366f1', fontSize: '32px', fontWeight: 'bold', margin: '4px 0 0 0' }}>
          {reps}
        </p>
      </div>

      <div style={{
        backgroundColor: '#1f2937',
        borderRadius: '12px',
        padding: '16px',
        textAlign: 'center'
      }}>
        <p style={{ color: '#9ca3af', fontSize: '14px', margin: 0 }}>Corrects</p>
        <p style={{ color: '#22c55e', fontSize: '32px', fontWeight: 'bold', margin: '4px 0 0 0' }}>
          {correctReps}
        </p>
      </div>

      <div style={{
        backgroundColor: '#1f2937',
        borderRadius: '12px',
        padding: '16px',
        textAlign: 'center'
      }}>
        <p style={{ color: '#9ca3af', fontSize: '14px', margin: 0 }}>Puntation</p>
        <p style={{ color: '#f59e0b', fontSize: '32px', fontWeight: 'bold', margin: '4px 0 0 0' }}>
          {techniqueScore}%
        </p>
      </div>
      <div style={{
        backgroundColor: '#1f2937',
        borderRadius: '12px',
        padding: '16px',
        textAlign: 'center'
      }}>
        <p style={{ color: ' #9ca3af', fontSize: '14px', margin: 0}}>Confidence</p>
        <p style={{
          color: getConfidenceColor(),
          fontSize: '32px',
          fontWeight: 'bold',
          margin: '4px 0 0 0'
        }}>
          {Math.round((confidence || 0) * 100)}%
        </p>
      </div>

      <div style={{
        backgroundColor: '#1f2937',
        borderRadius: '12px',
        padding: '16px',
        textAlign: 'center'
      }}>
        <p style={{ color: '#9ca3af', fontSize: '14px', margin: 0 }}>Status</p>
        <p style={{
          color: getStatusColor(),
          fontSize: '18px',
          fontWeight: 'bold',
          margin: '4px 0 0 0'
        }}>
          {status || 'Waiting...'}
        </p>
      </div>

      <div style={{
        backgroundColor: '#1f2937',
        borderRadius: '12px',
        padding: '16px',
        textAlign: 'center'
      }}>
        <p style={{ color: '#9ca3af', fontSize: '14px', margin: 0}}>Exercise Status</p>
        <p style={{
          color: exerciseStatus === 'Doing Exercise' ? '#22c55e' : '#6b7280',
          fontSize: '18px',
          fontWeight: 'bold',
          margin: '4px 0 0 0'
        }}>
          {exerciseStatus || 'Resting'}
        </p>
      </div>
    </div>
    
  );
};

export default Stats;