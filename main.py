import pyaudio
import wave
import os
import unittest
import speech_recognition as sr
import webbrowser

def KylieHears():
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "file.wav"

    audio = pyaudio.PyAudio()

    try:
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        print("Listening...")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        audio.terminate()
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

        r = sr.Recognizer()
        with sr.AudioFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), "file.wav")) as source:
            audio = r.record(source)
        return r.recognize_google(audio) # r.recognize_google(audio, language='vi-VN')
        # another way
        # r = sr.Recognizer()
        # with sr.Microphone() as source:
        #     print("Listening...")
        #     audio = r.listen(source)
        #     return r.recognize_google(audio) # r.recognize_google(audio, language='vi-VN')
    except:
        return None

def KylieSays(content):
    content = 'CreateObject("SAPI.SpVoice").Speak"{}"'.format(content)
    with open("speak.vbs", "w") as f:
        f.write(content)
        f.close()
    os.system("speak.vbs")

while 1:
    userInput = KylieHears()
    if userInput == None:
        continue
    userInput = userInput.lower()
    if userInput in ("hello", "hi"):
        KylieSays("hello, sir")
    elif userInput in ("hey kylie", "kylie"):
        KylieSays("yes sir")
    elif userInput in ("i love you", "i crush you", "i like you", "love you"):
        KylieSays("sorry sir, i have a boyfriend")
    elif userInput.startswith(("what is", "what's", "tell me about")):
        KylieSays("Please wait for me a second")
        keyw = '+'.join(userInput.split()[2:])
        webbrowser.open("https://www.google.com.vn/#q=" + keyw)
    elif userInput in ("goodbye", "bye"):
        KylieSays("goodbye sir")
        exit(0)
    else:
        KylieSays("Sorry sir, I don't understand " + userInput)
        print("Unrecognized \"{}\"".format(userInput))
