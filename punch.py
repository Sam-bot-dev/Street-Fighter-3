import cv2
import mediapipe as mp
import pyautogui
import time

# -----------------------------
# SETTINGS
# -----------------------------
PUNCH_KEY = "q"          # game punch key
COOLDOWN = 0.50          # seconds (increase if spamming)
THRESHOLD = 0.06         # how much higher elbow must be than shoulder

# Prevent pyautogui failsafe issues
pyautogui.FAILSAFE = False

# -----------------------------
# MEDIAPIPE SETUP
# -----------------------------
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_punch_time = 0

with mp_pose.Pose(
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
) as pose:

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Camera not working")
            break

        # Mirror camera
        frame = cv2.flip(frame, 1)

        # Convert BGR -> RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect pose
        result = pose.process(rgb)

        action_text = "NONE"

        if result.pose_landmarks:
            # Draw skeleton
            mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            lm = result.pose_landmarks.landmark

            # Get landmarks (RIGHT side)
            right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = lm[mp_pose.PoseLandmark.RIGHT_ELBOW]

            # IMPORTANT:
            # Smaller Y = higher on screen
            punch_detected = right_elbow.y < (right_shoulder.y - THRESHOLD)

            if punch_detected:
                action_text = "PUNCH 🔥"

                # Cooldown check
                current_time = time.time()
                if current_time - last_punch_time > COOLDOWN:
                    pyautogui.press(PUNCH_KEY)
                    last_punch_time = current_time

        # Show action on screen
        cv2.putText(frame, f"ACTION: {action_text}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(frame, f"KEY: {PUNCH_KEY.upper()}  |  Cooldown: {COOLDOWN}s", (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Punch Controller (Right Hand)", frame)

        # Quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
