# Human State Detection System

This repository contains a set of scripts for training and running a real-time human state detection system (awake or sleepy) using the YOLOv5 model. When the system detects the "sleepy" state, it triggers an alarm melody to alert the user.

## Repository Structure

- `main.py`: The main script to run the real-time detection system.
- `take_pictures.py`: Script to collect images from a webcam.
- `label_photos.py`: Tool for labeling collected images and converting them into YOLO format.
- `custom_train.py`: Script for training the model based on labeled data.
- `requirements.txt`: A file listing dependencies for installation.

## Setup and Installation

To get started, clone the repository and install the required dependencies:

```bash
git clone https://github.com/thebmf/SleepyStateDetection
cd SleepyStateDetection
pip install -r requirements.txt
```

## Data Collection

Run take_pictures.py to collect images. This script will activate the webcam and automatically take 40 snapshots for each of the two states: awake and sleepy.

```bash
python take_pictures.py
```

## Data Labeling

To label the collected images, use the label_photos.py script. It will open a tkinter-based interface where you can label the images. After labeling, this script will also convert the images into the YOLO format, preparing them for model training.

```bash
python label_photos.py
```

## Model Training

After labeling and converting the images, run custom_train.py to train the model. It is recommended to use more than 100 epochs for the best results, but fewer can also be sufficient.

```bash
python custom_train.py
```

## Running the Detection System

To run the system in real-time, execute main.py. The system will activate the webcam and start detecting the state. When the sleepy state is detected, an alarm melody will start playing.

```bash
python main.py
```
