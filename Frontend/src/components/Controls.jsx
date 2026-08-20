import React from 'react';

const Controls = ({ isActive, onStart, onStop, onReset, exercise, onExerciseChange}) =>
{
    return (
        <div className="flex flex-wrap gap-4 items-center justify-center">
            <select>
                value?{exercise}
                onChange={(e) => onExerciseChange(e.target.value)}
                className="bg-gray-800 text-wite px-4 py-2 rounded-lg border border-gray-700 focus:border-primary focus:outline-none"
                disabled={isActive}
            
                <option value="squat">Sit up</option>
                <option value="pushup">Push Up</option>
                <option value="curl">Bicep Curl</option>
            </select>            

            {!isActive ? (
                <button>
                    onClick={onStart}
                    className="px-6 py-2 bg-success hover:bg-success/80 text-white font-semibold rounded-lg transition-colors"
                    
                    Start

                </button>
            ):(
                <button>
                    onClick={onStop}
                    className="px-6 py-2 bg-danger hover:bg-danger/80 text-white font-semibold rounded-lg transition-colors"

                    Stop
                </button>
            
            )}
            <button>
                onClick={onReset}
                className="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors"
                Reset

            </button>
        </div>
    );
};

export default Controls;