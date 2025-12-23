import cv2
from colorama import Fore, init

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print(Fore.GREEN +"Error occured!")
    exit()
    
while True:
    ret, frame = cap.read()
    if not ret:  #if it cannot capture frame
        print(Fore.GREEN +"Error occured! Failed to capture frame")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) #2 is thickness of rectangle #x and y are starting points
        cv2.imshow('Face Detection Press q to quit', frame)
        
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
        
cap.release() #turns of the camera
cv2.destroyAllWindows()