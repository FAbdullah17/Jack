import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import openai
from gtts import gTTS
import pygame
import os

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<YOUR_NEWS_API>"

# Initialize Pygame mixer once
pygame.mixer.init()


def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    # Load and play the MP3 file
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    # Wait until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiProcess(command):
    client = openai.OpenAI(
        api_key="<YOUR_OPENAI_API_KEY>",
    )

    completion = client.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a virtual assistant named Jack skilled in general tasks like Alexa and Google Cloud. Give short responses please",
            },
            {"role": "user", "content": command},
        ],
    )

    return completion.choices[0].message["content"]


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open twitter" in c.lower():
        webbrowser.open("https://twitter.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com")

    elif "news" in c.lower():
        try:
            r = requests.get(
                f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
            )
            if r.status_code == 200:
                # Parse the JSON response
                data = r.json()

                # Extract the articles
                articles = data.get("articles", [])

                # Print the headlines
                for article in articles:
                    speak(article["title"])
            else:
                speak("I couldn't retrieve the news at the moment.")
        except Exception as e:
            speak(f"An error occurred: {e}")
    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Starting Jack....")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for Jack...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            word = recognizer.recognize_google(audio)
            print(f"Heard: {word}")
            if word.lower() == "Jack":
                speak("Yup, I'm here")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jack Active...")
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
