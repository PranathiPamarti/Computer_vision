class DynamicGestureTracker:
    def __init__(self, max_history=5):
        self.history = []
        self.max_history = max_history

    def update(self, x):
        self.history.append(x)
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def detect_swipe(self, threshold=0.12):
        if len(self.history) < self.max_history:
            return None

        move = self.history[-1] - self.history[0]

        if move > threshold:
            return "SWIPE_RIGHT"
        elif move < -threshold:
            return "SWIPE_LEFT"

        return None
