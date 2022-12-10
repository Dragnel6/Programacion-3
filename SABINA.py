import speech_recognition as sr
import pyttsx3
import pywhatkit

name = "sabina "
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)

def talk(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            compu = listener.listen(source)
            recs = listener.recognize_google(compu)
            recs = recs.lower()
            print('Has mencionado: ' + recs)
    except:
        pass
    return recs    
   
def run_sabina():
    rec  = listen()
    if name in rec:
        rec = rec.replace(name, '')
        if 'reproduce' in rec:
            musica = rec.replace('reproduce ', '')
            talk("Reproduciendo " + musica)
            pywhatkit.playonyt(musica)

if __name__ == '__main__':
    run_sabina()  
