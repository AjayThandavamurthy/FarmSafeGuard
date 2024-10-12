import cv2
import cvzone
import math
from ultralytics import YOLO
import threading
import winsound
import imutils
import pyttsx3 as a
from twilio.rest import Client


sid = '********************'
token = '********************'
number1 = '+182******'
number2 = '+91733*******'

client = Client(sid, token)

def message(msg):
    message = client.messages.create(
        body= f"{msg} detected!!",
        from_=number1,
        to=number2
    )

# Function to speak using text-to-speech
def speak(aa):
    engine = a.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(aa)
    engine.runAndWait()

# Initialize YOLO model
model = YOLO('yolov8s.pt')

# Load class names
classnames = []
with open('classes.txt', 'r') as f:
    classnames = f.read().splitlines()

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize motion detection variables
_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=1000)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)
alarm = False
alarm_mode = False
alarm_counter = 0

# Function for motion detection alarm
def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("ALARM")
        winsound.Beep(2500, 1000)
    alarm = False

# Main loop
while True:
    # Read frame from camera
    ret, frame = cap.read()
    if not ret:
        break
    
    # Resize frame
    frame = cv2.resize(frame, (1580, 780))

    # Detect objects using YOLO
    results = model(frame)

    # Process YOLO results
    for info in results:
        parameters = info.boxes
        for box in parameters:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            confidence = box.conf[0]
            class_detect = box.cls[0]
            class_detect = int(class_detect)
            class_detect = classnames[class_detect]
            conf = math.ceil(confidence * 100)

            # Implement fall detection using the coordinates x1,y1,x2
            height = y2 - y1
            width = x2 - x1
            threshold  = height - width

            # Draw rectangle around detected objects
            if conf > 80 and class_detect in ['person', 'bird', 'elephant', 'bear', 'horse' ,'sheep', 'cow', 'zebra' ,'giraffe']:
                cvzone.cornerRect(frame, [x1, y1, width, height], l=30, rt=6)
                cvzone.putTextRect(frame, f'{class_detect}', [x1 + 8, y1 - 12], thickness=2, scale=2)
                
                if threshold < 0 and class_detect=='person':
                    cvzone.putTextRect(frame, 'Fall Detected', [height, width], thickness=2, scale=2)
                    speak("Fall Detected")
                
                if class_detect in ['bird', 'elephant', 'bear', 'horse' ,'sheep', 'cow', 'zebra' ,'giraffe']:
                    speak(f'{class_detect} detected')  # Call speak function
                    # message(class_detect)

    # Show frame
    cv2.imshow('frame', frame)

    # Motion detection
    _, frame = cap.read()
    frame = imutils.resize(frame, width=1000)
    
    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)
        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw
        
        if threshold.sum() > 3000000:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1
    #     cv2.imshow("Cam", threshold)
    # else:
    #     cv2.imshow("Cam", frame)
    
    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()
    
    # Keyboard input handling
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('t'):
        alarm_mode = not alarm_mode
        alarm_counter = 0

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()
