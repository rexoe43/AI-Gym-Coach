import React from 'react';

const Controls = ({ isActive, onStart, onStop, onReset, exercise, onExerciseChange}) =>
{
    return (
        <div style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '16px',
            alignItems: 'center',
            justifyContent: 'center',
            pedding: '16px 0'
        }}>
            <select
                value={exercise}
                onChange={(e) => onExerciseChange(e.target.value)}
                disabled={isActive}
                style={{
                    backgroundColor: '#1f2937',
                    color: 'white',
                    padding: '10px 20px',
                    borderRadius: '8px',
                    border: '1px solid #374151',
                    fontSize: '16px',
                    cursor: isActive ? 'not-allowed' : 'pointer',
                    opacity: isActive ? 0.6 : 1
                }}
                >
                <option value="squat">Squat</option>
                <option value="pushup">PushUp</option>
                <option value="curl">Bicep Curl</option>
            </select>

            {!isActive ? (
                <button
                    onCLick={onStart}
                    style={{
                        padding: '10px 30px',
                        backgroundColor: '#22c55e',
                        color: 'white',
                        fontWeight: 'bold',
                        borderRadius: '8px',
                        border: 'none',
                        fontSize: '16px',
                        cursor: 'pointer',
                        transition: 'background-color 0.3s',
                        boxShadow: '0 4px 6px rgba(34, 197, 94, 0.3)'
                    }}
                    onMouseEnter={(e) => e.target.style.backgroundColor = '#16a34a'}
                    onMouseLeave={(e) => e.target.style.backgroundColor = '#22c55e'}
                    >
                        Start
                </button>
            ):(
                <button
                    onClick={onStop}
                    style={{
                        padding: '10px 30px',
                        backgroundColor: '#ef4444',
                        color: 'white',
                        fontWeight: 'bold',
                        borderRadius: '8px',
                        border: 'none',
                        fontSize: '16px',
                        cursor: 'pointer',
                        transition: 'background-color 0.3s',
                        boxShadow: '0 4px 6px rgba(239, 68, 68, 0.3)'
                    }}
                    onMouseEnter={(e) => e.target.style.backgroundColor = '#dc2626'}
                    onMouseLeave={(e) => e.target.style.backgroundCOlor = '#ef4444'}
                    >
                        Stop
                    </button>
            )}

            <button 
                onClick={onReset}
                style={{
                    padding: '10px 30px',
                    backgroundColor: '#4b5563',
                    color: 'white',
                    fontWeight: 'bold',
                    borderRadius: '8px',
                    border: 'none',
                    fontSize: '16px',
                    cursor: 'pointer',
                    transition: 'background-color 0.3s',
                    boxShadow: '0 4px 6px rgba(75, 85, 99, 0.3)'
                }}
                onMouseEnter={(e) => e.target.style.backgroundColor = '#6b7280'}
                onMouseLeave={(e) => e.target.style.backgroundCOlor = '#4b5563'}
                >
                    Reset
                </button>
        </div>
    );
};

export default Controls;