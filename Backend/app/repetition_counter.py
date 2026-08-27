from .feature_extractor import RAW_SERIES_KEYS

# Per-exercise phase configuration:
#   joint  -> which raw angle drives the up/down phase machine
#   top    -> "extended/standing" threshold (rep boundary, start & end)
#   bottom -> "flexed/bottom" threshold (must be crossed to count as a rep)
EXERCISE_CONFIG = {
    'squat':  {'joint': 'knee_angle_right',  'top': 155, 'bottom': 120},
    'pushup': {'joint': 'elbow_angle_right', 'top': 160, 'bottom': 90},
}


class RepetitionCounter:
    """
    Tracks rep phase using the exercise's primary joint angle and
    accumulates the RAW per-frame signals (angles + torso_length) across
    the WHOLE repetition — from the moment the person starts the movement
    until they're back at the top — so the caller can later build the
    90-feature vector the trained model expects (see
    feature_extractor.build_repetition_feature_vector).

    This class stays model-agnostic: it never classifies correctness
    itself, it just hands back the raw series for the caller (predictor.py)
    to classify once the repetition is complete.
    """

    def __init__(self, exercise_type='squat', min_frames=5):
        self.exercise_type = exercise_type
        # A real repetition takes several frames of real movement. One
        # shorter than this is almost certainly landmark jitter (the joint
        # angle noisily crossing both thresholds without real movement),
        # not an actual repetition — so we discard it silently.
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
        """
        raw_angles: dict from feature_extractor.extract_raw_angles(landmarks)
                    for THIS frame.

        Returns: {'completed': bool, 'raw_series': dict|None}
        'raw_series' is only populated when 'completed' is True, and holds
        every frame's values collected during that repetition — ready to
        pass into build_repetition_feature_vector(raw_series, exercise_type).
        """
        result = {'completed': False, 'raw_series': None}

        config = self._config()
        if landmarks is None or config is None or raw_angles is None:
            # Unknown/unsupported exercise (e.g. 'curl' isn't wired up
            # yet) — do nothing rather than count using the wrong joint.
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

        # While in the down phase (flexing or extending back), keep
        # recording every frame so the buffer covers the whole movement.
        if self.stage == 'down':
            for key in RAW_SERIES_KEYS:
                if key in raw_angles:
                    self.rep_series[key].append(raw_angles[key])

        # Back to "up"/extended: repetition complete IF it actually had
        # enough frames of real movement. Otherwise it's noise — discard
        # it without counting, without classifying.
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