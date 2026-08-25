class RepetitionCounter:
    def __init__(self, exercise_type='squat'):
        self.exercise_type = exercise_type
        self.count = 0
        self.phase = 'idle'
        self.is_in_rep = False
        self.rep_landmarks = []

    def reset(self):
        self.count = 0
        self.phase = 'idle'
        self.is_in_rep = False
        self.rep_landmarks = []

    def update(self, landmarks, knee_angle):
        if landmarks is None:
            return False
        completed = False

        if self.exercise_type == 'squat':
            if knee_angle > 150 and self.phase == 'idle':
                self.phase = 'descending'
                self.rep_landmarks = []

            elif self.phase == 'descending' and knee_angle < 100:
                self.phase = 'ascending'
                self.rep_landmarks.append(landmarks)

            elif self.phase == 'ascending' and knee_angle > 150:
                self.phase = 'idle'
                self.count += 1
                completed = True
                self.rep_landmarks = []

        return completed

repetition_counter = RepetitionCounter()