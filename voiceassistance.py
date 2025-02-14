import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
try:
    engine = pyttsx3.init()
except Exception as e:
    print(f"Error initializing TTS engine: {e}")

# Function to make the assistant speak
def speak(text):
    try:
        print(f"Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak function: {e}")

# Function to listen to user commands
def listen():
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)
            print("Audio captured")
            return audio
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except Exception as e:
        print(f"Error in listen function: {e}")
        return None

# Function to handle commands
def handle_command(command):
    print(f"Handling command: {command}")
    if "hello" in command:
        speak("Hello! How can I help you?")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
    elif "search" in command:
        speak("What would you like me to search for?")
        search_query = listen()
        if search_query:
            try:
                search_query_text = recognizer.recognize_google(search_query).lower()
                url = f"https://www.google.com/search?q={search_query_text}"
                webbrowser.open(url)
                speak(f"Here are the search results for {search_query_text}")
            except sr.UnknownValueError:
                speak("Sorry, I did not understand the search query.")
            except sr.RequestError as e:
                speak(f"Could not request results; {e}")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I don't know how to do that.")

# Main function to run the chatbot
def main():
    while True:
        print("Say something...")
        audio = listen()
        if audio:
            try:
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                handle_command(command)
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

if __name__ == "__main__":
    main()