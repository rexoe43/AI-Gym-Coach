from .feature_extractor import RAW_SERIES_KEYS

EXERCISE_CONFIG = {
    'squat':  {'joint': 'knee_angle_right',  'top': 155, 'bottom': 120},
    'pushup': {'joint': 'elbow_angle_right', 'top': 160, 'bottom': 90},
}


class RepetitionCounter:
   

    def __init__(self, exercise_type='squat', min_frames=5):
        self.exercise_type = exercise_type
        # A real repetition takes several frames of real movement. One
        self.min_frames = min_frames
        self.count = 0          # counts EVERY completed repetition
        self.stage = 'up'
        self.rep_series = self._empty_series()

    def _empty_series(self):
        return {key: [] for key in RAW_SERIES_KEYS}

    def _config(self):
        return EXERCISE_CONFIG.get(self.exercise_type)

    def reset(self):
        self.count = 0
        self.stage = 'up'
        self.rep_series = self._empty_series()

    def update(self, landmarks, raw_angles=None):
        
        result = {'completed': False, 'raw_series': None}

        config = self._config()
        if landmarks is None or config is None or raw_angles is None:
            
            return result

        angle = raw_angles.get(config['joint'])
        if angle is None:
            return result

        top_angle = config['top']
        bottom_angle = config['bottom']

        # Entering the "down"/flexed phase: start a fresh buffer for this rep.
        if angle < bottom_angle and self.stage == 'up':
            self.stage = 'down'
            self.rep_series = self._empty_series()

        # While in the down phase (flexing or extending back), keep it
        if self.stage == 'down':
            for key in RAW_SERIES_KEYS:
                if key in raw_angles:
                    self.rep_series[key].append(raw_angles[key])

        # Back to "up"/extended: repetition complete IF it actually had
        # enough frames of real movement.
        if angle > top_angle and self.stage == 'down':
            self.stage = 'up'
            frames_collected = len(self.rep_series.get(config['joint'], []))

            if frames_collected >= self.min_frames:
                self.count += 1
                result['completed'] = True
                result['raw_series'] = self.rep_series

            self.rep_series = self._empty_series()

        return result


repetition_counter = RepetitionCounter()