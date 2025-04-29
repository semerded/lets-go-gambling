import cv2
import numpy as np
import os

# Initialize the face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

# Directory for storing face data
data_path = "src/database/face-data"
if not os.path.exists(data_path):
    os.makedirs(data_path)

# Function to collect face samples when 's' is pressed
def collect_faces():
    print("Press 's' to start collecting face data...")
    
    cap = cv2.VideoCapture(1)
    face_id = input("Enter unique ID for this face: ")  # Assign an ID to the person
    face_data = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            if len(face_data) < 5:
                face_roi = gray[y:y+h, x:x+w]  # Extract face region
                
                # Resize face sample to fixed size (e.g., 100x100 pixels)
                resized_face = cv2.resize(face_roi, (100, 100))
                
                face_data.append(resized_face.flatten())  # Convert to numerical data
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.imshow("Collecting Faces", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            print("Starting face data collection...")
        if key == ord('q'):
            break
        if len(face_data) >= 5:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save numeric face data properly
    face_data_array = np.array(face_data, dtype=np.float32)  # Ensure consistent datatype
    np.save(f"{data_path}/user_{face_id}.npy", face_data_array)
    
    print(f"Stored numeric face data for user {face_id}")

# Start face data collection when 's' is pressed
# collect_faces()


# Load stored face data
stored_faces = {}
for file in os.listdir(data_path):
    if file.endswith(".npy"):
        user_id = file.split("_")[1].split(".")[0]  # Extract user ID
        stored_faces[user_id] = np.load(os.path.join(data_path, file))

# Function to recognize faces
def recognize_faces():
    cap = cv2.VideoCapture(1)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            face_roi = cv2.resize(gray[y:y+h, x:x+w], (100, 100)).flatten()  # Normalize size

            recognized = "Unknown"
            min_distance = float("inf")

            # Compare captured face with stored faces
            for user_id, samples in stored_faces.items():
                distances = [np.linalg.norm(sample - face_roi) for sample in samples]
                avg_distance = np.mean(distances)

                if avg_distance < min_distance and avg_distance < 5000:  # Recognition threshold
                    min_distance = avg_distance
                    recognized = f"User {user_id}"

            # Display recognition result
            color = (0, 255, 0) if recognized != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, recognized, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Face Recognition", frame)

        # Press 'q' to exit recognition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Start real-time face recognition
recognize_faces()
