from .feature_extractor import RAW_SERIES_KEYS


class RepetitionCounter:
    """
    Tracks squat phase using knee angle and accumulates the RAW per-frame
    signals (angles + torso_length) across the WHOLE repetition — from the
    moment the person starts descending until they're back up — so the
    caller can later build the 90-feature vector the trained model expects
    (see feature_extractor.build_repetition_feature_vector).

    This class stays model-agnostic: it never classifies correctness itself,
    it just hands back the raw series for the caller (predictor.py) to
    classify once the repetition is complete.
    """

    def __init__(self, exercise_type='squat', top_angle=155, bottom_angle=120):
        self.exercise_type = exercise_type
        self.top_angle = top_angle       # standing / "up" threshold
        self.bottom_angle = bottom_angle  # squat-depth / "down" threshold
        self.count = 0          # counts EVERY completed repetition
        self.stage = 'up'
        self.rep_series = self._empty_series()

    def _empty_series(self):
        return {key: [] for key in RAW_SERIES_KEYS}

    def reset(self):
        self.count = 0
        self.stage = 'up'
        self.rep_series = self._empty_series()

    def update(self, landmarks, knee_angle, raw_angles=None):
        """
        raw_angles: dict from feature_extractor.extract_raw_angles(landmarks)
                    for THIS frame.

        Returns: {'completed': bool, 'raw_series': dict|None}
        'raw_series' is only populated when 'completed' is True, and holds
        every frame's values collected during that repetition — ready to
        pass into build_repetition_feature_vector().
        """
        result = {'completed': False, 'raw_series': None}

        if landmarks is None or self.exercise_type != 'squat':
            return result

        # Entering the down phase: start a fresh buffer for this rep.
        if knee_angle < self.bottom_angle and self.stage == 'up':
            self.stage = 'down'
            self.rep_series = self._empty_series()

        # While in the down phase (going down or coming back up), keep
        # recording every frame so the buffer covers the whole movement.
        if self.stage == 'down' and raw_angles is not None:
            for key in RAW_SERIES_KEYS:
                if key in raw_angles:
                    self.rep_series[key].append(raw_angles[key])

        # Back up top: repetition complete.
        if knee_angle > self.top_angle and self.stage == 'down':
            self.stage = 'up'
            self.count += 1
            result['completed'] = True
            result['raw_series'] = self.rep_series
            self.rep_series = self._empty_series()

        return result


repetition_counter = RepetitionCounter()