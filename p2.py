import cv2
from ultralytics import YOLO
import torch
import serial
import time
import random
from pynput import keyboard

# Initialize serial communication with Arduino
arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to initialize

# Load the YOLO model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = YOLO('best.pt').to(device)

# Initialize the webcam
cap = cv2.VideoCapture(0)  # 0 is the default camera

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

desired_width = 1920
desired_height = 1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

window_name = 'YOLOv8 Webcam'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# Resize the window (e.g., 1280x720)
output_width = 1280
output_height = 720
cv2.resizeWindow(window_name, output_width, output_height)

# P controller gain
Kp = 0.02

def map_control_signal(control_signal, min_output, max_output):
    # Ensure the control signal is within the valid range
    control_signal = max(min(control_signal, max_output), min_output)
    # Map the control signal to the range for continuous servos (0-180, with 90 being stop)
    mapped_signal = int((control_signal - min_output) / (max_output - min_output) * 180)
    # Shift the signal to make 90 the stop position
    return mapped_signal + 90

# Loop to continuously get frames from the webcam
while True:
    ret, frame = cap.read()

    # If frame is read correctly, ret is True
    if not ret:
        print("Error: Could not read frame.")
        break

    # Run YOLOv8 on the frame
    results = model(frame)

    # Draw the results on the frame
    annotated_frame = results[0].plot()

    # Get frame dimensions
    frame_height, frame_width, _ = frame.shape
    frame_center_x = frame_width // 2
    frame_center_y = frame_height // 2

    # Assume the first detected object for simplicity
    if results[0].boxes:
        box = results[0].boxes[0]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        object_center_x = (x1 + x2) // 2
        object_center_y = (y1 + y2) // 2

        # Calculate errors
        error_x = frame_center_x - object_center_x
        error_y = frame_center_y - object_center_y

        # Calculate control signals
        control_signal_x = Kp * error_x
        control_signal_y = Kp * error_y

        # Map control signals to servo range (0-180, with 90 being stop)
        # servo_signal_x = map_control_signal(control_signal_x, -frame_center_x, frame_center_x)
        # servo_signal_y = map_control_signal(control_signal_y, -frame_center_y, frame_center_y)
        servo_signal_x =((control_signal_x+100)/200*180)
        servo_signal_y = abs(180-((control_signal_y+100)/200*180))

        # Send the control signals to the Arduino
        arduino.write(f'{servo_signal_y},{servo_signal_x}\n'.encode())

        # Print control signals for debugging
        print(f'Control signals - X: {control_signal_x}, Y: {control_signal_y}')
        print(f'Servo signals - X: {servo_signal_x}, Y: {servo_signal_y}')

        # Optionally, you can draw lines indicating the center
        cv2.line(annotated_frame, (frame_center_x, 0), (frame_center_x, frame_height), (0, 255, 0), 2)
        cv2.line(annotated_frame, (0, frame_center_y), (frame_width, frame_center_y), (0, 255, 0), 2)
        cv2.circle(annotated_frame, (object_center_x, object_center_y), 5, (0, 0, 255), -1)

    # Display the frame with the detections
    cv2.imshow(window_name, annotated_frame)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
