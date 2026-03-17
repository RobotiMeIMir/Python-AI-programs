import speech_recognition as sr
from gtts import gTTS
import os
import datetime
import argostranstale.package #for offline version of google translate
import argostranslate.translate 

install_languages = argostranslate.translate.get_installed_languages()
from_language = next(filter(lambda x: x.code == "en", install_languages))
to_language = next(filter(lambda x: x.code == "es", install_languages))
translation = from_language.get_translation(to_language)
recognizer = sr.Recognizer() #initialize the speech recognizer
mic = sr.Microphone() 
def p_query(query):
    query = query.lower()
    if "time" in query:
        now = datetime.datetime.now()
        response = f"The current time is {now.strftime('%H:%M:%S')}"
    elif "date" in query:
        today = datetime.date.today()
        response = f"Today's date is {today.strftime('%Y-%m-%d')}"
    else:
        response = query
    return response
    
def txt(text, language = "es"):
    translated = translation.translate(text)
    print(f"Translated: {translated}")
    tts = gTTS(translated, lang=language)
    tts.save("response.mp3")
    os.system("start response.mp3" if os.name == "nt" else "afplay response.mp3") #play the audio file (works on Windows and macOS);
    
print("Listening for commands... (say 'exit' to quit)")
while True:
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Say something...")
        audio = recognizer.listen(source, timeout=5)
        try:
            text =recognizer.recognize_sphix(audio)    
            print(f"You said: {text}")
            RESPONSE = p_query(text)
            txt(RESPONSE, language = "es")  
        except sr.UnckoenValueError:
                print("Sorry, I couldn't understand the audio. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results from the speech recognition service; {e}")
    if text.lower() == "exit":
        print("Goodbye!")
        break