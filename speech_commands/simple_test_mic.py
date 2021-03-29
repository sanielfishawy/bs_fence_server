import speech_recognition_local as sr
import pyaudio

r = sr.Recognizer()

mic = sr.Microphone(device_index=1, sample_rate=44100, chunk_size=512)
with mic as source:                # use the default microphone as the audio source
    audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

try:
    print("You said " + r.recognize_google(audio))    # recognize speech using Google Speech Recognition
except LookupError:                            # speech is unintelligible
    print("Could not understand audio")