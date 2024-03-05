
import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import os 
import time
import playsound as ps
import speech_recognition as sr
from gtts import gTTS
import pyttsx3


configFile = 'config.txt'
apiKeyFromFile = None

if os.path.exists(configFile):
  with open(configFile, 'r') as file:
    apiKeyFromFile = file.read().strip()
else:
  apiKeyFromFile = input("Enter your google Gemini API key: ")
  with open(configFile, 'w') as file:
    file.write(apiKeyFromFile)

apiKey = apiKeyFromFile
genai.configure(api_key=apiKey)

model = genai.GenerativeModel("gemini-pro")

wake1 = 'hey dot'
wake2 = 'hey doc'
wake3 = 'hey dock'
wake4 = 'play dot'

safetysettings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  }
]

prefix = "Pretend you are an AI called dot. In one to five sentences, "

def speak(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    # engine.setProperty('rate', 150)  # Speed (words per minute)

    # Speak the given text
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()

def getResponse(input):
  response = model.generate_content(
    prefix + str(input), 
    safety_settings=safetysettings
  )

  return response

def get_audio(timeoutCount):
  r = sr.Recognizer()
  with sr.Microphone() as source:
    try:
      audio = r.listen(source, timeout=timeoutCount)
      print("Exception: " + "Audio Timed Out")

    except:
      audio = ''  
    said = ''

    try:
      said = r.recognize_google(audio)
      print(said)
    except Exception as e:
      print("Exception: " + "No audio heard")

  return said

while True:
  userSpeech = get_audio(0.35) 

  if userSpeech.count(wake1) > 0 or userSpeech.count(wake2) > 0 or userSpeech.count(wake3) > 0:
    speak("I'm ready!")
    userSpeech = get_audio(1)
    if 'what is your name' in userSpeech or "what\'s your name" in userSpeech:
      speak("I'm Dot! Your virtual assistant")
    elif 'how was your day' in userSpeech or 'how\'s your day' in userSpeech:
      speak("Its going great so far, thanks for asking!")
    else:
      response = getResponse(userSpeech)
      print(response.text)
      speak(response.text)   