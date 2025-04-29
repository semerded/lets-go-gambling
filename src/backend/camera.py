import cv2
import easyocr
import numpy as np
import pygame

# Initialize Pygame
pygame.init()
surface = pygame.Surface((800, 600))  # Default surface size for text mode

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Open the camera
cap = cv2.VideoCapture(1)

# System mode: facial recognition or text recognition
use_facial_recognition = False  # Toggle to switch modes

# Function to check 5 consecutive samples
def check_samples(samples):
    return len(samples) >= 5 and all(s == samples[0] for s in samples)

# Facial recognition variables
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
face_samples = []

# Text recognition variables
text_samples = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if use_facial_recognition:
        # Set camera resolution for facial recognition (full frame)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)  
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        detected_faces = len(faces)

        # Store consecutive samples
        face_samples.append(detected_faces)
        if len(face_samples) > 5:
            face_samples.pop(0)

        # Check if 5 samples are the same
        if check_samples(face_samples):
            print(f"Face Detected: {detected_faces} faces")
            break  # Stop loop when 5 consecutive same samples are detected

        # Convert to Pygame surface (use full-frame for facial recognition)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))  # Rotate for correct orientation

    else:
        # Set camera resolution for text recognition (optimized for 400x100 px)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)  
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

        # Crop only the necessary text region (400x100 px)
        crop_x_start = int((frame.shape[1] - 400) / 2)  # Center horizontally
        crop_y_start = int(frame.shape[0] * 0.5)  # Middle section
        cropped_frame = frame[crop_y_start:crop_y_start + 100, crop_x_start:crop_x_start + 400]

        # Convert frame to grayscale for OCR
        gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

        # Scale down image slightly to make OCR process faster
        resized_gray = cv2.resize(gray, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

        # Run OCR only on the cropped region
        results = reader.readtext(resized_gray, detail=0, paragraph=False, batch_size=1)

        for text in results:
            text = text.replace(" ", "")  # Clean OCR result
            if text and text[0] in ("r", "u", "0") and text[1:].isnumeric():  # Validate format
                if text[0] == "0":
                    text = "r" + text[1:]  # Replace leading 0 with "r"

                text_samples.append(text)
                if len(text_samples) > 5:
                    text_samples.pop(0)

                # Check if 5 samples are the same
                if check_samples(text_samples):
                    print(f"Detected Text: {text}")
                    break  # Stop loop when 5 consecutive same samples are detected

        # Convert to Pygame surface (use cropped frame for text mode)
        frame_rgb = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)
        surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))  # Rotate for correct orientation

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
