import os
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv    
import pyttsx3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import cv2
import face_recognition

load_dotenv()

API_KEY=os.getenv('gemini_api_key')

genai.configure(api_key=API_KEY)


def Speech_to_Text():
    r=sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = r.listen(source)
            my_text = r.recognize_google(audio)
            print("Wilson: " + my_text + "\n")
        except sr.UnknownValueError:
            print("Could not understand audio\n\n")
        except sr.RequestError as e:
            print("Error: {0}\n".format(e))


    
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    chat = model.start_chat(history=[])

    while(True):
        # language= 'en'
        if(my_text.strip()==''):
            break
        else:
            response = chat.send_message(my_text)
            gemini_text=response.text
            print("Shannon: " + gemini_text + "\n____________________________________________________________________________________________________________________________________") 
            engine=pyttsx3.init()
            engine.setProperty('rate', 200)
            voices = engine.getProperty('voices')       #getting details of current voice
            engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
            engine.say(gemini_text)
            engine.runAndWait()
            
            break

def recognize_me():
        
    # Load your face image(s)
    known_image1 = face_recognition.load_image_file("faces\wilson.jpg")
    known_image2 = face_recognition.load_image_file("dr dele chatbot\\faces\wilson2.jpg")  # Add more as needed
    known_face_encoding1 = face_recognition.face_encodings(known_image1)[0]
    known_face_encoding2 = face_recognition.face_encodings(known_image2)[0]  # Add more as needed
    # Create lists for encodings and names
    known_face_encodings = [known_face_encoding1, known_face_encoding2]  # Add more as needed
    known_face_names = ["Wilson", "Wilson (Side)"]  # Add more as needed
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

def main():
    app = QApplication([])
    window= QWidget()
    window.setGeometry(100, 100, 400, 300)
    window.setWindowTitle("My Chatbot")

     
    layout = QVBoxLayout()
    
    label = QLabel("Press the buttons below to speak!")
    button= QPushButton("Camera")
    button2=QPushButton("Converse!")
    button.clicked.connect(recognize_me)
    button2.clicked.connect(Speech_to_Text)
    button.setMinimumWidth(100) 
    button.setMinimumHeight(70) 
    button2.setMinimumWidth(100) 
    button2.setMinimumHeight(70)  
    layout.addWidget(label)
    layout.addWidget(button)
    layout.addWidget(button2)
    label.move(50,100)
    window.setLayout(layout)
    window.show()
    app.exec_()
if __name__== '__main__':
    main()

    # if name=="Unknown":
    #     button.setEnabled(False)
    # elif name=="Wilson":
    #     button.setEnabled(True)
    # elif name=="Wilson (Side)":
    #     button.setEnabled(True)
    # else:
    #     button.setEnabled(False)