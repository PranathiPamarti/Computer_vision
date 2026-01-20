import cv2
import time

from core.camera import Camera
from core.hand_tracker import HandTracker

from gesture.gesture_utils import get_finger_states
from gesture.static_gestures import classify_static_gesture
from gesture.dynamic_gestures import DynamicGestureTracker

from actions.slide_control import next_slide, previous_slide, start_presentation, exit_presentation

# Cooldowns
last_gesture_time = 0
GESTURE_COOLDOWN = 1.0    # 1 second cooldown
laser_mode = False
camera = Camera()
tracker = HandTracker()

dyn = DynamicGestureTracker()

palm_start_time = None
presentation_mode = False

print("GVPA Pro – Gesture + Slide Control Ready")

while True:
    frame = camera.get_frame()
    if frame is None:
        continue

    result = tracker.process(frame)
    gesture_text = ""

    if result.hand_landmarks:
        lm = result.hand_landmarks[0]
        #tracker.draw_landmarks(frame, lm)

        # -------- STATIC GESTURES --------
        fingers = get_finger_states(lm)
        static_gesture = classify_static_gesture(fingers)

        from gesture.gesture_utils import is_pinch
        if is_pinch(lm):
            laser_mode = True
        else:
            laser_mode=False

        # -------- LASER POINTER --------
        if laser_mode:
            h, w, _ = frame.shape

            # Use index finger tip for laser position
            x = int(lm[8].x * w)
            y = int(lm[8].y * h)

            # Draw red laser dot
            cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)

            cv2.putText(frame, "LASER MODE", (10, 190),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


        # -------- DYNAMIC GESTURES --------
        wrist_x = lm[0].x
        dyn.update(wrist_x)
        dynamic_gesture = dyn.detect_swipe()

        current_time = time.time()

        # =============================
        # NEXT SLIDE (PEACE SIGN)
        # =============================
        if static_gesture == "PEACE":
            if current_time - last_gesture_time > GESTURE_COOLDOWN:
                next_slide()
                gesture_text = "Next Slide"
                last_gesture_time = current_time

        # =============================
        # PREVIOUS SLIDE (POINT SIGN)
        # =============================
        elif static_gesture == "POINT":
            if current_time - last_gesture_time > GESTURE_COOLDOWN:
                previous_slide()
                gesture_text = "Previous Slide"
                last_gesture_time = current_time

        # =============================
        # PALM HOLD (START/STOP PRESENTATION)
        # =============================
        if static_gesture == "PALM":
            if palm_start_time is None:
                palm_start_time = time.time()
            elif time.time() - palm_start_time > 1.2:
                if not presentation_mode:
                    start_presentation()
                    presentation_mode = True
                    gesture_text = "Start Presentation"
                else:
                    exit_presentation()
                    presentation_mode = False
                    gesture_text = "Exit Presentation"
                palm_start_time = None
        else:
            palm_start_time = None

        # -------- DISPLAY TEXT --------
        if static_gesture:
            cv2.putText(frame, f"Static: {static_gesture}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        if dynamic_gesture:
            cv2.putText(frame, f"Dynamic: {dynamic_gesture}", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

        if gesture_text:
            cv2.putText(frame, gesture_text, (10, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)

    cv2.imshow("GVPA PRO - Gesture Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
