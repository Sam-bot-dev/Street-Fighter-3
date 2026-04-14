import cv2
import mediapipe as mp
import pyautogui
import time
import math

pyautogui.FAILSAFE = False

# ----------------------------
# SETTINGS
# ----------------------------
COOLDOWN = 0.25
ALPHA = 0.7
STABILITY = 0.01

LIGHT = 0.03
MEDIUM = 0.05
HEAVY = 0.075

# ----------------------------
# INIT
# ----------------------------
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FPS, 60)

if not cap.isOpened():
    print("Camera failed")
    exit()

prev_left = prev_right = None
smooth_left = smooth_right = None

last_action = 0
frame_count = 0

# ----------------------------
# UTILS
# ----------------------------
def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def smooth(prev, new):
    if prev is None:
        return new
    return (
        ALPHA * prev[0] + (1 - ALPHA) * new[0],
        ALPHA * prev[1] + (1 - ALPHA) * new[1]
    )

def filtered_move(curr, prev):
    if prev is None:
        return 0
    d = dist(curr, prev)
    return 0 if d < STABILITY else d

# ----------------------------
# MAIN LOOP
# ----------------------------
with mp_pose.Pose(
    static_image_mode=False,
    model_complexity=0,
    smooth_landmarks=True,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose:

    try:
        while True:
            frame_count += 1

            # skip frames for speed
            if frame_count % 2 != 0:
                continue

            for _ in range(1):  # reduce buffer lag
                cap.grab()

            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (320, 240))

            rgb = frame[:, :, ::-1]

            result = pose.process(rgb)

            action = "NONE"

            if result.pose_landmarks:
                lm = result.pose_landmarks.landmark

                lw = lm[mp_pose.PoseLandmark.LEFT_WRIST]
                rw = lm[mp_pose.PoseLandmark.RIGHT_WRIST]

                left = smooth(smooth_left, (lw.x, lw.y))
                right = smooth(smooth_right, (rw.x, rw.y))

                smooth_left, smooth_right = left, right

                now = time.time()

                left_move = filtered_move(left, prev_left)
                right_move = filtered_move(right, prev_right)

                prev_left, prev_right = left, right

                # ----------------------------
                # RIGHT HAND → PUNCH (A Q S)
                # ----------------------------
                if right_move > LIGHT and now - last_action > COOLDOWN:

                    if right_move < MEDIUM:
                        pyautogui.press("a")
                        action = "LIGHT PUNCH (A)"

                    elif right_move < HEAVY:
                        pyautogui.press("q")
                        action = "MEDIUM PUNCH (Q)"

                    else:
                        pyautogui.press("s")
                        action = "HEAVY PUNCH (S)"

                    last_action = now

                # ----------------------------
                # LEFT HAND → KICK (Z W X)
                # ----------------------------
                elif left_move > LIGHT and now - last_action > COOLDOWN:

                    if left_move < MEDIUM:
                        pyautogui.press("z")
                        action = "LIGHT KICK (Z)"

                    elif left_move < HEAVY:
                        pyautogui.press("w")
                        action = "MEDIUM KICK (W)"

                    else:
                        pyautogui.press("x")
                        action = "HEAVY KICK (X)"

                    last_action = now

                # ----------------------------
                # VISUAL FEEDBACK (IMPORTANT)
                # ----------------------------
                if action != "NONE":
                    cv2.putText(frame, action, (20, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (0, 255, 0), 2)

                    # draw circles on hands
                    h, w, _ = frame.shape
                    cv2.circle(frame, (int(lw.x * w), int(lw.y * h)), 8, (255, 0, 0), -1)
                    cv2.circle(frame, (int(rw.x * w), int(rw.y * h)), 8, (0, 0, 255), -1)

            else:
                cv2.putText(frame, "NO POSE DETECTED", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 0, 255), 2)

            # FPS display
            cv2.putText(frame, f"FPS MODE", (200, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 1)

            cv2.imshow("PoseFighter PRO", frame)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                break

            time.sleep(0.005)

    except Exception as e:
        print("ERROR:", e)

cap.release()
cv2.destroyAllWindows()