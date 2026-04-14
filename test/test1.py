import cv2
import mediapipe as mp
import pyautogui
import time
import math
from threading import Thread

pyautogui.FAILSAFE = False

# ----------------------------
# SETTINGS
# ----------------------------
COOLDOWN = 0.25
ALPHA = 0.75
STABILITY = 0.008

LIGHT = 0.025
MEDIUM = 0.045
HEAVY = 0.070

DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 720

# ----------------------------
# CAMERA THREAD
# ----------------------------
class Camera:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FPS, 60)

        self.ret, self.frame = self.cap.read()
        self.running = True

        Thread(target=self.update, daemon=True).start()

    def update(self):
        while self.running:
            self.ret, self.frame = self.cap.read()

    def read(self):
        return self.ret, self.frame

    def release(self):
        self.running = False
        self.cap.release()

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
# INIT
# ----------------------------
cam = Camera()
mp_pose = mp.solutions.pose

prev_left = prev_right = None
smooth_left = smooth_right = None
last_action = 0

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

    while True:
        ret, frame = cam.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)

        # PROCESS SMALL (FAST)
        small = cv2.resize(frame, (320, 240))
        rgb = small[:, :, ::-1]

        result = pose.process(rgb)

        action = "NONE"

        if result.pose_landmarks:
            lm = result.pose_landmarks.landmark

            lw = lm[mp_pose.PoseLandmark.LEFT_WRIST]
            rw = lm[mp_pose.PoseLandmark.RIGHT_WRIST]

            # scale back to original frame
            left = smooth(smooth_left, (lw.x, lw.y))
            right = smooth(smooth_right, (rw.x, rw.y))

            smooth_left, smooth_right = left, right

            now = time.time()

            left_move = filtered_move(left, prev_left)
            right_move = filtered_move(right, prev_right)

            prev_left, prev_right = left, right

            # ----------------------------
            # PUNCH (RIGHT HAND)
            # ----------------------------
            if right_move > LIGHT and now - last_action > COOLDOWN:

                if right_move < MEDIUM:
                    pyautogui.press("a")
                    action = "LIGHT PUNCH"

                elif right_move < HEAVY:
                    pyautogui.press("q")
                    action = "MEDIUM PUNCH"

                else:
                    pyautogui.press("s")
                    action = "HEAVY PUNCH"

                last_action = now

            # ----------------------------
            # KICK (LEFT HAND)
            # ----------------------------
            elif left_move > LIGHT and now - last_action > COOLDOWN:

                if left_move < MEDIUM:
                    pyautogui.press("z")
                    action = "LIGHT KICK"

                elif left_move < HEAVY:
                    pyautogui.press("w")
                    action = "MEDIUM KICK"

                else:
                    pyautogui.press("x")
                    action = "HEAVY KICK"

                last_action = now

            # ----------------------------
            # VISUALS (BIG SCREEN)
            # ----------------------------
            h, w, _ = frame.shape

            lx, ly = int(left[0] * w), int(left[1] * h)
            rx, ry = int(right[0] * w), int(right[1] * h)

            cv2.circle(frame, (lx, ly), 10, (255, 0, 0), -1)
            cv2.circle(frame, (rx, ry), 10, (0, 0, 255), -1)

            cv2.putText(frame, action, (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 3)

        else:
            cv2.putText(frame, "NO DETECTION", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 3)

        # BIG DISPLAY
        display = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        cv2.imshow("PoseFighter PRO MAX", display)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cam.release()
cv2.destroyAllWindows()