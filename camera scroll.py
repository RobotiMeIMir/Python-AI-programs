import cv2, time, pyautogui
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

scroll_speed = 300
scroll_delay = 1
cam_width, cam_height = 640, 480
def detect_gesture(landmarks, handiness): #tells us which hand
    fingers = []
    tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]
    for tip in tips:
        if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y:
            fingers.append(1) #store values
        
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP] #checking if its left or right hand
    thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP] #joint of the thumb
    if (handiness == "Right" and thumb_tip.x > thumb_ip.x) or (handiness == "Left" and thumb_tip.x < thumb_ip.x):
        fingers.append(1)
        
    return "Scroll up" if sum(fingers) == 1 else "Scroll down" if len(fingers) == 0 else "No Scroll"
cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)
lost_scroll = p_time = 0 #calculating fps
print("Scroll using hand gestures. Press 'q' to quit.")
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break
    
    image = cv2.flip(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), 1)
    results = hands.process(image)
    gesture, handiness = "No Scroll", "Unckown"
    
    if results.multi_hand_landmarks:
        for hand, handiness in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_label = handiness.classification[0].label
            gesture = detect_gesture(hand, handiness)
            mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)
            
            if (time.time() - lost_scroll) > scroll_delay:
                if gesture == "Scroll up":
                    pyautogui.scroll(scroll_speed)
                elif gesture == "Scroll down":
                    pyautogui.scroll(-scroll_speed)
                lost_scroll = time.time()
            
    fps = 1 / (time.time() - p_time) if(time.time() - p_time) > 0 else 0
    p_time = time.time()
    cv2.putText(image, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(image, f'Gesture: {gesture}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Camera Scroll', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()