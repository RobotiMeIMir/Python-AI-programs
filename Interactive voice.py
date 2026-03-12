#import speech_recognition as sr
import pyttsx3
from googletrans import Translator
 
def speak(text, language = "en"):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voice = engine.getProperty('voices')
    if language == "en":
        engine.setProperty('voice', voice[0].id)  # English voice
    else:
        engine.setProperty('voice', voice[1].id)  # Every voice
    engine.say(text)
    engine.runAndWait()
def stt():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"You said: {text}")
        return text
    except Exception as e:
        print("Sorry, I couldn't understand. Please try again.")
        return None
def translate(text, dest_language = "es"):
    translator = Translator()
    translation = translator.translate(text, dest=dest_language)
    return translation.text
def display(): #show language options
    print("Available languages:")
    print("1. English (en)")
    print("2. Spanish (es)")
    print("3. French (fr)")
    print("4. German (de)")
    print("5. Italian (it)")
    print("6. Albanian (sq)")
    
    choice = input("Choose a language (1-6): ")
    languages = { 
        "1": "en",
        "2": "es",
        "3": "fr",
        "4": "de",
        "5": "it",
        "6": "sq"
    }
    return languages.get(choice)

def main():
    dest_language = display()
    original_text = stt()
    if original_text:
        translated_text = translate(original_text, dest_language)
        print(f"Translated text: {translated_text}")
        speak(translated_text, dest_language)
if __name__ == "__main__":
    main()