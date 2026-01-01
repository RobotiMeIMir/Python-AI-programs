import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands #accessing hand solutions in mp
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils #drawing utilities/landmarks
cap = cv2.VideoCapture(0) #accessing webcam
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()
    
print("Press 'q' to quit.")

def detect_gestures(hand_landmarks):
    landmarks = hand_landmarks.landmark
    tip_ids = [4, 8, 12, 16, 20]
    pip_id = [2, 6, 10, 14, 18]
    extended = 0
    
    if abs(landmarks[tip_ids[0]].x - landmarks[pip_id[0]].x) > 0.04:
            extended += 1
            
    for i in range(1, 5):
        if landmarks[tip_ids[i]].y < landmarks[pip_id[i]].y:
            extended += 1
            
    if extended >= 4:
        return "Open Palm"
    elif extended == 0:
        return "Closed"
    else:
        return "Partial"
    
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    gesture = "No Hands"
    
    if result.multi_hand_landmarks and result.multi_handedness: #identifies left/right hand
        for idex, hand_landmarks in enumerate(result.multi_hand_landmarks):
            hand_label = result.multi_handedness[idex].classification[0].label          
            gesture = detect_gestures(hand_landmarks)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            finger_tip_id = [4, 8, 12, 16, 20]
            for tip_id in finger_tip_id:
                lm = hand_landmarks.landmark[tip_id]
                x, y = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (x, y), 10, (255, 0, 0), cv2.FILLED)
                cv2.putText(frame, str(tip_id), (x - 5, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

            wrist = hand_landmarks.landmark[0]
            wrist_x, wrist_y = int(wrist.x * w), int(wrist.y * h)
            cv2.putText(frame, f"{hand_label}Hand, ", (wrist_x - 40, wrist_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            status_color = (0, 255, 0) if gesture in ["Open Palm", "Closed"] else (0, 165, 255)
            cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
            cv2.imshow("Hand Gesture Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
cap.release()
cv2.destroyAllWindows()          