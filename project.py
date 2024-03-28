import os
import speech_recognition
from googletrans import Translator
import pyttsx3
from moviepy.editor import VideoFileClip

# Install the required libraries if not already installed:
# speech_recognition, pyttsx3, pyaudio, googletrans, moviepy, pydub

sr = speech_recognition.Recognizer()


def count_words(texts):
    count_word = texts.split()
    return len(count_word)


def count_letters(texts):
    count_letter = [char for char in texts if char.isalpha()]
    return len(count_letter)


def translate_speech(target_language, text):
    try:
        translator = Translator()
        translated_text = translator.translate(text, dest=target_language)
        return translated_text.text
    except Exception:
        return None


def recognize_your_voice(microphone):
    try:
        if microphone is None:
            return "No speech detected or microphone issue"
        sr.adjust_for_ambient_noise(microphone, duration=0.5)
        audio = sr.listen(microphone)
        return sr.recognize_google(audio)
    except speech_recognition.UnknownValueError:
        return "I cannot recognize your voice...again"


def recognize_audio_file():
    try:
        name = input("Enter the location of the audio file: ")
        if os.path.exists(name):
            with speech_recognition.AudioFile(name) as a_file:
                record = sr.record(a_file)
                text = sr.recognize_google(record)
                return text
        else:
            print("File not found.")
    except Exception as e:
        print(e)


def text_to_speech(text):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voices', voices[0].id)
        engine.setProperty('rate', 110)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(e)


def convert_mp4_to_mp3():
    try:
        mp4_loc = input("Enter the location of the MP4 file: ")
        if os.path.exists(mp4_loc):
            video = VideoFileClip(mp4_loc)
            audio = video.audio
            mp3_loc = os.path.splitext(mp4_loc)[0] + ".mp3"  # Save MP3 file in the same directory
            audio.write_audiofile(mp3_loc)
            print("Converted successfully.")
        else:
            print("File not found.")
    except Exception as e:
        print(e)


def main():
    while True:
        try:
            command = input("""
Type the corresponding number
1. Count words
2. Count letters
3. Translate to (desired language)
4. Speech to text
5. Read from an audio file
6. Text to speech
7. Convert MP4 to MP3
Command: """)

            if command == '5':
                print(recognize_audio_file())
            elif command == '6':
                text = input("Enter text to convert to speech: ")
                text_to_speech(text)
            elif command == '7':
                convert_mp4_to_mp3()
            else:
                with speech_recognition.Microphone() as microphone:
                    print("You may now start speaking")
                    text = recognize_your_voice(microphone)
                    if command == '1':
                        num_words = count_words(text.replace("command count words", ""))
                        print(f"There are {num_words} words in what you said")
                    elif command == '2':
                        num_letters = count_letters(text.replace("command count letters", ""))
                        print(f"There are {num_letters} letters in what you said")
                    elif command == '3':
                        target_lang = text.split("translate to")[1].strip()
                        translated = translate_speech(target_lang, text)
                        if translated is not None:
                            print(f"Translated command: {translated}")
                        else:
                            print("Translation failed.")
                    elif command == '4':
                        print(f"You said: {text}")

        except KeyboardInterrupt:
            print("Goodbye")
            break


if __name__ == '__main__':
    main()
