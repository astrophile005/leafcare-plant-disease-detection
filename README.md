# LeafCare – Plant Disease Detection Using CNN

## Overview

LeafCare is an AI-powered plant disease detection application that uses Convolutional Neural Networks (CNN)
to identify diseases in plant leaves.

Users can upload an image or capture a picture using their camera. The application analyzes the leaf image and predicts
the possible disease, helping users identify plant health issues at an early stage.

## Objectives

- Detect plant diseases using deep learning.
- Classify plant leaf images accurately.
- Provide useful information about detected diseases.
- Support early identification of plant diseases.

## Key Features

- Plant Disease Detection: Identify diseases from leaf images.
- Camera Scanning: Capture images using a camera.
- Disease Library: Explore information about different plant diseases.
- Scan History: View previously scanned results.
- Dashboard: Access application features from one place.
- CSV Export: Export scan records.

## Technologies Used

- Python
- TensorFlow
- Keras
- Convolutional Neural Network (CNN)
- Streamlit
- NumPy
- Pandas
- Pillow

## Model Information

- Model Architecture: Convolutional Neural Network (CNN)
- Input Image Size: 224 × 224 pixels
- Output: 38 plant disease classes
- Supported Crops: 14 different crops

## Model Performance

Reported validation accuracy: 94.64%


## Installation and Setup

Follow these steps to run LeafCare on your computer.

### Step 1: Clone the Repository

```bash
git clone https://github.com/astrophile005/leafcare-plant-disease-detection.git
```

### Step 2: Navigate to the Project Folder

```bash
cd leafcare-plant-disease-detection
```

### Step 3: Create a Virtual Environment

```bash
python -m venv leafenv
```

### Step 4: Activate the Virtual Environment

For Windows:

```bash
leafenv\Scripts\activate
```

### Step 5: Install Required Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your web browser.


## Future Enhancements

- Improve model accuracy.
- Support additional plant species.
- Provide more detailed disease prevention suggestions.
- Add multilingual support.

## Developer

Developed as an Artificial Intelligence and Data Science project.

Project Name: LeafCare

Domain: Artificial Intelligence and Deep Learning

Application: Plant Disease Detection
