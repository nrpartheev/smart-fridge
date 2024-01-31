import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from playsound import playsound
from pathlib import Path
from openai import OpenAI
import os
import time

client = OpenAI()


def say(text):
    speech_file_path = Path(__file__).parent / "sounds/speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(speech_file_path)
    playsound(speech_file_path)


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Speak something...")
        audio = recognizer.listen(source)
        print(audio)
        print("Hmmmmm")
        try:
            text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("value")
            playsound("sounds/ValueError.mp3")
            text = listen()
        except sr.RequestError:
            print("NETWORK ERROR MOSTLY")
            playsound("sounds/ValueError.mp3")
            text = listen()
            
    return text


say("Hi There..")
time.sleep(2)
time.sleep(3)
say("What is your name.")
time.sleep(3)
say("What is the reason for your visit")
time.sleep(3)
time.sleep("we will the owner know about your visit")


