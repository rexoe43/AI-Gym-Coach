class RepetitionCounter:
    def __init__(self, exercise_type='squat'):
        self.exercise_type = exercise_type
        self.count = 0
        self.correct_count = 0
        self.phase = 'idle'
        self.min_knee = 180.0
        self.max_torso = 0.0
        self.last_rep_score = 0
        self.score_sum = 0.0

    def reset(self):
        self.count = 0
        self.correct_count = 0
        self.phase = 'idle'
        self.min_knee = 180.0
        self.max_torso = 0.0
        self.last_rep_score = 0
        self.score_sum = 0.0

    @property
    def average_score(self):
        if self.count == 0:
            return 0
        return int(round(self.score_sum / self.count))

    def update(self, landmarks, knee_angle, torso_angle=0.0):
        if landmarks is None:
            return False

        completed = False
        knee = float(knee_angle)
        torso = float(torso_angle)

        if self.exercise_type != 'squat':
            return False

        if knee > 145 and self.phase == 'idle':
            self.phase = 'descending'
            self.min_knee = knee
            self.max_torso = torso

        elif self.phase == 'descending':
            self.min_knee = min(self.min_knee, knee)
            self.max_torso = max(self.max_torso, torso)
            if knee < 105:
                self.phase = 'ascending'

        elif self.phase == 'ascending':
            self.min_knee = min(self.min_knee, knee)
            self.max_torso = max(self.max_torso, torso)
            if knee > 145:
                self.phase = 'idle'
                self.count += 1
                completed = True

                depth_score = 100 if self.min_knee <= 95 else max(0, 100 - (self.min_knee - 95) * 4)
                torso_score = max(0, 100 - max(0, self.max_torso - 25) * 3)
                self.last_rep_score = int(round(0.7 * depth_score + 0.3 * torso_score))
                self.score_sum += self.last_rep_score

                if self.min_knee <= 105 and self.max_torso < 50:
                    self.correct_count += 1

                self.min_knee = 180.0
                self.max_torso = 0.0

        return completed


repetition_counter = RepetitionCounter()
