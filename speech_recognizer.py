import os
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv  
from pyttsx3 import *
load_dotenv()

API_KEY=os.getenv('gemini_api_key')

genai.configure(api_key=API_KEY)

r=sr.Recognizer()

def record_text():
 while(1):
    try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio = r.listen(source)
                    my_text = r.recognize_google(audio)
                    return my_text
    except sr.UnknownValueError:
                    print("Could not understand audio\n\n")
    except sr.RequestError as e:
                    print("Error: {0}\n".format(e))

    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    chat = model.start_chat(history=[])

        # language= 'en'
    if(my_text.strip()==''):
            break
    else:
            response = chat.send_message(my_text)
            # speech = BytesIO()
            gemini_text=response.text
            return gemini_text 
            engine=pyttsx3.init()
            engine.setProperty('rate', 200)
            voices = engine.getProperty('voices')       #getting details of current voice
            engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
            engine.say(gemini_text)
            engine.runAndWait()
            # out_speech = gTTS(text=gemini_text, lang=language, tld='us')
            # out_audio = 'speech.mp3'
            # out_speech.save(out_audio)
            # out_speech.write_to_fp(speech)
            # playsound("speech.mp3")
            
            break
 

def output_text(text):
        f = open("output.txt", "a")
        f.write(text)
        f.write("\n")
        f.close()
        return

while(1):
        text = record_text()
        output_text(text)

        print("wrote text")