from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ["Go shopping", "Clean house", "Learn a new technology"]

#GREETING
def greeting():
    speaker.say("Hello, what can I do for you?")
    speaker.runAndWait()
#QUIT
def quit():
    speaker.say("Bye!")
    speaker.runAndWait()
    sys.exit(0)

#CREATING A NOTE
def create_note():
    global recognizer
    speaker.say("What do you want to write onto your note?")
    speaker.runAndWait()

    done = False

    while not done :
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a filename!")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say("The filename have been created successfully, you can find it on {filename}")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again!")
            speaker.runAndWait()

#ADD ITEMS TO DO LIST
def add_todo():
    global recognizer

    speaker.say("What do you want to add?")
    speaker.runAndWait()

    done= False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)
                done = True

                speaker.say("I added the item to the list!")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again!")
            speaker.runAndWait()

def show_todos():

    speaker.say("The items on your list are the following")
    for item in todo_list:
        speaker.say(item)
        speaker.runAndWait()


# MAPPING
mappings = {
    "greeting": greeting,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "exit": quit
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

            assistant.request(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()