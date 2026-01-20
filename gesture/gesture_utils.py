# gesture/gesture_utils.py

FINGERTIPS = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky

def get_finger_states(lm):
    """
    lm is now a LIST of landmarks (MediaPipe Tasks API)
    Each landmark has .x and .y
    Returns list of 5 ints: 1 = finger up, 0 = finger down
    """

    fingers = []

    # Thumb (compare x positions)
    if lm[FINGERTIPS[0]].x < lm[FINGERTIPS[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers (compare y positions)
    for tip in FINGERTIPS[1:]:
        if lm[tip].y < lm[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

import math

def is_pinch(lm, threshold=0.04):
    """
    Detect pinch using distance between thumb tip (4)
    and index finger tip (8)
    """
    thumb = lm[4]
    index = lm[8]

    distance = math.sqrt(
        (thumb.x - index.x) ** 2 +
        (thumb.y - index.y) ** 2
    )

    return distance < threshold
