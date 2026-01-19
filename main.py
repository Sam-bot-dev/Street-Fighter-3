import cv2
import mediapipe as mp 

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# 4) Start Pose detection model
with mp_pose.Pose(
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
) as pose:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera not working")
            break
        # 5) Mirror the camera (so it feels natural)
        frame = cv2.flip(frame, 1)

        # 6) Convert BGR -> RGB (MediaPipe needs RGB)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 7) Run pose detection
        result = pose.process(rgb)

        # 8) If pose is detected, draw skeleton
        if result.pose_landmarks:
            mp_draw.draw_landmarks(
                frame,                      # image to draw on
                result.pose_landmarks,      # landmarks
                mp_pose.POSE_CONNECTIONS    # lines between landmarks
            )

        # 9) Show the output window
        cv2.imshow("Pose Skeleton", frame)

        # 10) Quit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
