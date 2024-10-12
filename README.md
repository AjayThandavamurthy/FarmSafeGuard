# **FarmSafeGuard: Wild Animal and Fall Detection with Auto Alerts**

**FarmSafeGuard** is an AI-powered system designed to protect farms from wild animals and detect human falls. Utilizing object detection, motion tracking, and real-time alerts, this system helps farmers prevent intrusions by wild animals and ensure human safety on the farm. The project leverages cutting-edge computer vision techniques, including the YOLO model for object detection, and integrates with an alerting system using Twilio for SMS notifications. It also supports text-to-speech functionality for enhanced awareness.

## **Features**
- **Wild Animal Detection**: Identifies animals like elephants, bears, horses, cows, and more that may enter the farm.
- **Human Fall Detection**: Detects when a person falls and raises an alert.
- **Auto Alert System**: Sends an automatic SMS alert using Twilio to notify the user in case of wild animal detection or human fall.
- **Text-to-Speech Alert**: Uses text-to-speech to announce detected objects (animals or falls) for immediate action.
- **Motion Detection with Alarms**: Detects abnormal movements in the farm and triggers a sound alarm for intrusions.

## **Technologies Used**
- **Python**: Core language for scripting the system.
- **OpenCV**: For handling video input and motion detection.
- **YOLOv8 (Ultralytics)**: Object detection model to identify animals and humans.
- **Twilio API**: For sending SMS alerts in case of a fall or wild animal intrusion.
- **pyttsx3**: Python library for text-to-speech functionality.
- **Winsound**: To trigger sound alarms for motion detection.
- **Imutils**: For image processing and resizing operations.

## **How It Works**
1. **Object Detection**: The system initializes a live video feed through a camera using OpenCV. The YOLOv8 model is used to detect objects, specifically targeting humans and wild animals.
2. **Fall Detection**: The system measures the dimensions of the detected person. If the difference between height and width crosses a certain threshold, it determines that a fall has occurred.
3. **Motion Detection**: The system continuously checks for significant movements in the video feed. If unusual motion is detected, it triggers an alarm.
4. **Alerting**: Upon detecting a fall or the presence of a wild animal, the system:
   - Plays an alarm sound.
   - Sends an SMS notification using Twilio.
   - Uses text-to-speech to announce the detected object.
