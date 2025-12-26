import cv2
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error!")
    exit()
    
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error! Failed to capture frame")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, scaleFactor= 1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in face:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f'People count: {len(face)}', (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA) #smooth edges of text #1 is font size
        cv2.imshow("People Count - Press q to quit", frame)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()