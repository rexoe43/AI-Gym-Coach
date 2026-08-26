import React from 'react';

const Stats = ({ reps, status }) => {
  const getStatusColor = () => {
    if (status === 'Training') return '#22c55e';
    if (status === 'No body detected') return '#ef4444';
    return '#9ca3af';
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
    </div>
  );
};

export default Stats;