class RepetitionCounter:
    def __init__(self, exercise_type='squat', top_angle=155, bottom_angle=120):
        self.exercise_type = exercise_type
        # More lenient defaults: a 2D camera angle rarely sees a "textbook"
        # 150/100 range because depth/perspective flattens the real angle.
        self.top_angle = top_angle       # standing/"idle" threshold
        self.bottom_angle = bottom_angle  # squat-depth threshold
        self.count = 0          # counts EVERY completed repetition (original behavior)
        self.phase = 'idle'
        self.is_in_rep = False
        self.rep_landmarks = []
        self.rep_predictions = []

    def reset(self):
        self.count = 0
        self.phase = 'idle'
        self.is_in_rep = False
        self.rep_landmarks = []
        self.rep_predictions = []

    def update(self, landmarks, knee_angle, prediction=None):
        """
        prediction: dict from predict_exercise for THIS frame, e.g.
                    {'class': 'correct', 'confidence': 0.8, ...}
        Returns a dict: {'completed': bool, 'is_correct': bool|None}

        'count' (self.count) increments on EVERY completed repetition,
        regardless of correctness — this is what drives the "Repetitions"
        stat, so it never gets stuck at 0 waiting on the model.

        'is_correct' is a SEPARATE judgment (majority vote of this rep's
        predictions) used only to color the "Technique" card green/red —
        it never blocks the count itself.
        """
        result = {'completed': False, 'is_correct': None}

        if landmarks is None:
            return result

        if self.exercise_type == 'squat':
            if knee_angle > self.top_angle and self.phase == 'idle':
                self.phase = 'descending'
                self.rep_landmarks = []
                self.rep_predictions = []

            elif self.phase in ('descending', 'ascending') and knee_angle < self.bottom_angle:
                self.phase = 'ascending'
                self.rep_landmarks.append(landmarks)
                if prediction is not None:
                    self.rep_predictions.append(prediction)

            elif self.phase == 'ascending' and knee_angle > self.top_angle:
                self.phase = 'idle'
                self.count += 1
                result['completed'] = True

                # Correctness is informational only (feeds Technique color),
                # it does NOT gate whether the rep counted above.
                is_correct = False
                if self.rep_predictions:
                    correct_votes = sum(
                        1 for p in self.rep_predictions if p.get('class') == 'correct'
                    )
                    is_correct = correct_votes >= (len(self.rep_predictions) * 0.4)

                result['is_correct'] = is_correct

                self.rep_landmarks = []
                self.rep_predictions = []

        return result

repetition_counter = RepetitionCounter()