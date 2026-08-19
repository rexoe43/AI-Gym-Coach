import React from 'react';

const Stats = ({ reps, correctReps, techniqueScore, status}) => {
    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-800 rounded-xl p-4 text-center">
                <p className="text-gray-400 text-sm">Repetitions</p>
                <p className="text-3xl font-bold text-primary">{reps}</p>
            </div>
            <div className="bg-gray-800 rounded-xl p-4 text-center">
                <p className="text-gray-400 text-sm">Corrects</p>
                <p className="text-3xl font-bold text-success">{correctReps}</p>
            </div>
            <div className="bg-gray-800 rounded-xl p-4 text-center">
                <p className="text-gray-400 text-sm">Puntation</p>
                <p className="text-3xl font-bold text-warning">{techniqueScore}%</p>
            </div>
            <div className="bg-gray-800 rounded-xl p-4 text-center">
                <p className="text-gray-400 text-sm">Status</p>
                <p className={`text-lg font-semibold ${
                    status === 'correct' ? 'text-success':
                    status === 'incorrect' ? 'text-danger':
                    'text-gray-400'
                }`}>
                    {status || 'Waiting...'}
                </p>
            </div>
        </div>
    );
};

export default Stats;