import cv2
import face_recognition
# Load your face image(s)
known_image1 = face_recognition.load_image_file("faces\wilson.jpg")
known_image2 = face_recognition.load_image_file("dr dele chatbot\\faces\wilson2.jpg")  # Add more as needed
known_face_encoding1 = face_recognition.face_encodings(known_image1)[0]
known_face_encoding2 = face_recognition.face_encodings(known_image2)[0]  # Add more as needed
# Create lists for encodings and names
known_face_encodings = [known_face_encoding1, known_face_encoding2]  # Add more as needed
known_face_names = ["You", "You (Side)"]  # Add more as needed
face_cap = cv2.CascadeClassifier("C:/Users/ADMIN/programming/C#/.conda/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml") 
video_cap = cv2.VideoCapture(0)
process_this_frame = True
while True:
    ret, frame = video_cap.read()
    if not ret:
        break
    # Detect faces (no need for grayscale conversion)
    faces = face_cap.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if process_this_frame:
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            match = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5) # Adjust tolerance 
            name = "Unknown"
            if True in match:
                first_match_index = match.index(True)
                name = known_face_names[first_match_index]
            face_names.append(name)
    process_this_frame = not process_this_frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_cap.release()
cv2.destroyAllWindows()