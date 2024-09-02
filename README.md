# Aimbot

This repository contains an Arduino-based project that controls two servos based on object detection using a YOLO model. The system uses a webcam to detect objects in real-time and adjusts the servo positions to aim at the detected object. The control signals are sent to the servos via an Arduino through serial communication.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
  - [Python Code](#python-code)
  - [Arduino Code](#arduino-code)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

This project demonstrates how to use a YOLO (You Only Look Once) model for real-time object detection, combined with an Arduino to control servos. The goal is to create an automated aiming system, or "aimbot," that keeps an object centered in the camera's view by adjusting the position of the servos.

## Features

- **Real-time Object Detection**: Uses the YOLO model to detect objects in real-time through a webcam.
- **Servo Control**: Adjusts the position of two servos based on the detected object's location.
- **Arduino Integration**: Communicates with an Arduino to send control signals to the servos.
- **Proportional Control**: Implements a simple proportional control algorithm to maintain the object at the center of the camera's view.

## Hardware Requirements

- Arduino (e.g., Arduino Uno)
- 2x Servo Motors
- Webcam
- Computer with Python and necessary libraries installed
- Jumper wires and a breadboard

## Software Requirements

- Python 3.x
- OpenCV (`cv2`)
- PyTorch
- Ultralytics YOLOv8
- Arduino IDE

## Setup and Installation

### Python Environment

1. Clone the repository:
    ```bash
    git clone https://github.com/Nitish05/AimBot.git
    cd AimBot
    ```

2. Install the required Python libraries:

3. Connect the webcam and ensure it is working properly.

### Arduino Setup

1. Open the `aimbot.ino` file in the Arduino IDE.
2. Connect your Arduino to your computer.
3. Upload the code to your Arduino.

### Wiring

- Connect the servos to pins 9 and 10 on the Arduino.
- Ensure your power supply to the servos is adequate and that ground is common between the Arduino and the servos.

## Usage

1. Run the Python script to start object detection:
    ```bash
    python aimbot.py
    ```

2. The servos will automatically adjust based on the position of the detected object.

3. Press `q` in the Python script window to quit.

## Code Explanation

### Python Code

The Python script captures frames from the webcam, detects objects using a YOLO model, and calculates the error between the object's position and the center of the frame. Based on this error, it generates control signals that are sent to the Arduino to adjust the servos.

### Arduino Code

The Arduino code receives the control signals from the Python script via serial communication, parses them, and adjusts the servos accordingly. The servos aim to keep the detected object centered in the frame.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Ultralytics YOLOv8](https://github.com/ultralytics/yolov8) for the object detection model.
- The Arduino community for providing great resources and support.
