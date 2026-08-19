import React from 'react';

const Feedback = ({ prediction, confidence, error}) => {
    if (!prediction && !error) {
        return (
            <div className="bg-gray-800 rounded-xl p-6 text-center text-gray-400">
                <p>Do any exercise to receive feedback</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-gray-800 rounded-xl p-6 border border-danger/30">
                <p className="text-danger">Error: {error}</p>
            </div>
        );
    }

    const isCorrect = prediction == 'correct';
    const confidencePercent = (confidence * 100).toFixed(1);

    return (
        <div className={`bg-gray-800 rounded-xl p-6 border ${
            isCorrect ? 'border-success/30': 'border-danger/30'
        }`}>
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-gray-400 text-sm">Technique</p>
                    <p className={`text-2xl font-bold ${
                        isCorrect ? 'text-success' : 'text-danger'
                    }`}>
                        {isCorrect ? 'Correct': 'Improvable'}
                    </p>
                </div>
                <div className="text-right">
                    <p className="text-gray-400 text-sm">Confidence</p>
                    <p className="text-2xl font-bol text-primary">{confidencePercent}%</p>
                </div>
            </div>
            {!isCorrect && (
                <div className="mt-4 p-3 bg-danger/10 rounded-lg border border-danger/20">
                    <p className="text-danger text-sm">
                        Tip: Adjust your posture. Try tp keep your back straight and lower yourself until your thighs are parallel to the floor
                    </p>
            </div>
            )}
            {isCorrect && (
                <div className="mt-4 p-3 bg-success/10 rounded-lg border border-success/20">
                    <p className="text-success text-sm">
                        Excelent keep going, your technique is good

                    </p>
                </div>
            )}
        </div>
    );
};

export default FeedBack;