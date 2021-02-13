import speech_recognition as sr
import pyaudio
import os

fd = os.open('/dev/null',os.O_WRONLY)
os.dup2(fd,2)

r = sr.Recognizer() 
 
with  sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print('Speak Anything : ')
    audio = r.listen(source,timeout=5, phrase_time_limit=5)
 
    try:
        text = r.recognize_google(audio, language="es-ES")
        print('You said: {}'.format(text))
    except:
        print('Sorry could not hear')