import cv2
import easyocr
import numpy as np

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Open the camera
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)  # Lower resolution for speed
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

if not cap.isOpened():
    print("Error: Couldn't open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Crop only the necessary text region (400x100 px)
    crop_x_start = int((frame.shape[1] - 400) / 2)  # Center horizontally
    crop_y_start = int(frame.shape[0] * 0.5)  # Middle section
    cropped_frame = frame[crop_y_start:crop_y_start + 100, crop_x_start:crop_x_start + 400]

    # Convert to grayscale before OCR (boosts speed!)
    gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

    # Scale down image slightly to make OCR process faster
    resized_gray = cv2.resize(gray, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    # Run OCR only on optimized image with reduced complexity
    results = reader.readtext(resized_gray, detail=0, paragraph=False, batch_size=1)

    for text in results:
        text = text.replace(" ", "")  # Clean OCR result
        if text and text[0] in ("r", "u", "0") and text[1:].isnumeric():  # Validate expected format
            cv2.putText(cropped_frame, f"Detected: {text}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show only cropped 400x100 px window
    cv2.imshow('Optimized OCR - 400x100 px', cropped_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
