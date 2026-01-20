def classify_static_gesture(fingers):
    """
    Takes finger states and returns:
    PALM / FIST / POINT / PEACE / None
    """
    if fingers == [1,1,1,1,1]:
        return "PALM"
    if fingers == [0,0,0,0,0]:
        return "FIST"
    if fingers == [0,1,0,0,0]:
        return "POINT"
    if fingers == [0,1,1,0,0]:
        return "PEACE"

    return None
