import cv2
import mediapipe as mp
import pyautogui
import time
import math

pyautogui.FAILSAFE = False

# ----------------------------
# SETTINGS (TUNE THESE)
# ----------------------------
COOLDOWN = 0.25            # time gap between punches
MOVE_THRESHOLD = 0.030     # minimum movement required
STABILITY_THRESHOLD = 0.010  # ignore tiny jitter
ALPHA = 0.6                # smoothing (0.0 = no smooth, 0.9 = heavy smooth)

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

prev_left = None
prev_right = None

smooth_left = None
smooth_right = None

last_left_punch = 0
last_right_punch = 0

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def smooth_point(prev, new, alpha=0.6):
    if prev is None:
        return new
    return (alpha * prev[0] + (1 - alpha) * new[0],
            alpha * prev[1] + (1 - alpha) * new[1])

with mp_pose.Pose(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    model_complexity=0
) as pose:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = pose.process(rgb)

        action_text = "NONE"

        if result.pose_landmarks:
            lm = result.pose_landmarks.landmark

            lw = lm[mp_pose.PoseLandmark.LEFT_WRIST]
            rw = lm[mp_pose.PoseLandmark.RIGHT_WRIST]

            # Raw points (normalized)
            left_pos = (lw.x, lw.y)
            right_pos = (rw.x, rw.y)

            # Smooth points (reduces jitter)
            smooth_left = smooth_point(smooth_left, left_pos, ALPHA)
            smooth_right = smooth_point(smooth_right, right_pos, ALPHA)

            now = time.time()

            # Movement amount between frames
            left_move = dist(smooth_left, prev_left) if prev_left else 0
            right_move = dist(smooth_right, prev_right) if prev_right else 0

            # Update previous
            prev_left = smooth_left
            prev_right = smooth_right

            # Ignore tiny jitter movement
            if left_move < STABILITY_THRESHOLD:
                left_move = 0
            if right_move < STABILITY_THRESHOLD:
                right_move = 0

            # ----------------------------
            # IMPORTANT: Frame is flipped
            # MediaPipe RIGHT hand = screen LEFT
            # MediaPipe LEFT hand  = screen RIGHT
            # ----------------------------

            # Trigger only if movement is big enough + cooldown passed
            # Screen LEFT -> press A (MediaPipe RIGHT)
            if right_move > MOVE_THRESHOLD and (now - last_left_punch > COOLDOWN):
                pyautogui.press("a")
                last_left_punch = now
                action_text = f"LEFT PUNCH (A)  move={right_move:.3f}"

            # Screen RIGHT -> press Q (MediaPipe LEFT)
            elif left_move > MOVE_THRESHOLD and (now - last_right_punch > COOLDOWN):
                pyautogui.press("q")
                last_right_punch = now
                action_text = f"RIGHT PUNCH (Q) move={left_move:.3f}"

        cv2.putText(frame, action_text, (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("PoseFighter - Stable Stance Mode", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
import cv2
import mediapipe as mp
import pyautogui
import time
import math

pyautogui.FAILSAFE = False

# ----------------------------
# SETTINGS (TUNE THESE)
# ----------------------------
COOLDOWN = 0.25            # time gap between punches
MOVE_THRESHOLD = 0.030     # minimum movement required
STABILITY_THRESHOLD = 0.010  # ignore tiny jitter
ALPHA = 0.6                # smoothing (0.0 = no smooth, 0.9 = heavy smooth)

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

prev_left = None
prev_right = None

smooth_left = None
smooth_right = None

last_left_punch = 0
last_right_punch = 0

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def smooth_point(prev, new, alpha=0.6):
    if prev is None:
        return new
    return (alpha * prev[0] + (1 - alpha) * new[0],
            alpha * prev[1] + (1 - alpha) * new[1])

with mp_pose.Pose(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    model_complexity=0
) as pose:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = pose.process(rgb)

        action_text = "NONE"

        if result.pose_landmarks:
            lm = result.pose_landmarks.landmark

            lw = lm[mp_pose.PoseLandmark.LEFT_WRIST]
            rw = lm[mp_pose.PoseLandmark.RIGHT_WRIST]

            # Raw points (normalized)
            left_pos = (lw.x, lw.y)
            right_pos = (rw.x, rw.y)

            # Smooth points (reduces jitter)
            smooth_left = smooth_point(smooth_left, left_pos, ALPHA)
            smooth_right = smooth_point(smooth_right, right_pos, ALPHA)

            now = time.time()

            # Movement amount between frames
            left_move = dist(smooth_left, prev_left) if prev_left else 0
            right_move = dist(smooth_right, prev_right) if prev_right else 0

            # Update previous
            prev_left = smooth_left
            prev_right = smooth_right

            # Ignore tiny jitter movement
            if left_move < STABILITY_THRESHOLD:
                left_move = 0
            if right_move < STABILITY_THRESHOLD:
                right_move = 0

            # ----------------------------
            # IMPORTANT: Frame is flipped
            # MediaPipe RIGHT hand = screen LEFT
            # MediaPipe LEFT hand  = screen RIGHT
            # ----------------------------

            # Trigger only if movement is big enough + cooldown passed
            # Screen LEFT -> press A (MediaPipe RIGHT)
            if right_move > MOVE_THRESHOLD and (now - last_left_punch > COOLDOWN):
                pyautogui.press("a")
                last_left_punch = now
                action_text = f"LEFT PUNCH (A)  move={right_move:.3f}"

            # Screen RIGHT -> press Q (MediaPipe LEFT)
            elif left_move > MOVE_THRESHOLD and (now - last_right_punch > COOLDOWN):
                pyautogui.press("q")
                last_right_punch = now
                action_text = f"RIGHT PUNCH (Q) move={left_move:.3f}"

        cv2.putText(frame, action_text, (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("PoseFighter - Stable Stance Mode", frame)

        if cv2.waitKey(1) & 0xFF == ord("w"):
            break

cap.release()
cv2.destroyAllWindows()
