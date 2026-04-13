import speech_recognition as sr  # this we can use to call it using the short name sr
import webbrowser as wb
import pyttsx3
import musiclibrary
# import requests
import pyjokes
import google.generativeai as genai


# google ai studio api key 
genai.configure(api_key="AIzaSyC-mRs-k5trWLR3NefR7CC2v9ssz0CqIbA")


# Configure the AI to give short, voice-friendly answers
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction="You are a helpful voice assistant. Keep your answers extremely brief, conversational, and to the point. Use only 1 or 2 short sentences. Do not use asterisks, bolding, or lists."
)
chat = model.start_chat(history=[])


def processGenAi(command_text):
    # sends text to Gemini and speaks the response
    try:
        response = chat.send_message(command_text)
        # Clean up any potential markdown formatting
        clean_response = response.text.replace('*', '')
        speak(clean_response)
    except Exception as e:
        print(f"API Error: {e}")
        speak("Sorry, I am having trouble connecting to my brain.")


def giveJoke():
  joke = pyjokes.get_joke()
  return joke


# pip install pocketsphinx ---> this we have run to make the sphinx working 


# creating the object for the recognition 
recognizer = sr.Recognizer()
# engine = pyttsx3.init()   # this was running only one time therefore it is saying it only one time first one 

def speak(text):
  engine = pyttsx3.init()
  engine.say(text)
  engine.runAndWait()

# this will process the command 
def processCommand(c: str):
  #  if (c.lower() == "open Jarvis"):    this we are not using we are using this in different fromat

  if "open google" in c.lower() :
   speak("opening google")
   wb.open("https://www.google.com/")
  elif "open facebook" in c.lower() :
   speak("opening facebook")
   wb.open("https://www.facebook.com/")
  elif "open linkedin" in c.lower() :
   speak("opening linkedin")
   wb.open("https://www.linkedin.com/")
  elif "open youtube" in c.lower() :
   speak("opening youtube")
   wb.open("https://www.youtube.com/")
  elif c.lower().startswith("play") :
   song = c.lower().split(" ")[1]
   speak(f"playing {song}")
   link = musiclibrary.music[song]    # mistake : i have used the parenthesis here but this is a dictionary 
   wb.open(link)
  elif "joke" in c.lower() :
   speak("here is a joke for you.")
   speak(giveJoke())
  else :
     processGenAi(c.lower())
    
  



if __name__ == "__main__" :

  speak("Initializing Jarvis ......")
  while True:
    # Listening for the word "Jarvis"
    # obtain audio from the microphone
    r = sr.Recognizer()

    # this we moved to the try section to dont get the error
    # with sr.Microphone() as source:
    #     print("Listening.......")
    #     audio = r.listen(source,timeout=2)   # this take the two argument timeout to do the recognitze faster we need to set the timeout 


    print("Recognizing....")
    # recognize speech using Sphinx
    try:
        # print("Sphinx thinks you said " + r.recognize_sphinx(audio))
        # command = r.recognize_sphinx(audio)  we are not using this as this is not giving the proper answer

        """ This is just for the silent demo tommorow we will initialize it """
        with sr.Microphone() as source:
            print("Listening.......")
            audio = r.listen(source,timeout=2,phrase_time_limit=1)  # this is for listening one word only
        word = r.recognize_Jarvis(audio)
        print(word)
        
        """---------------------------------------------------------------------"""

        # this is just for the demo 
        # word = input("Please enter the command to activate.... \n:")
        if(word.lower() == "Jarvis"):
            speak("yes How may i help you")

            # Listen for command 
            """This is disabled only for the demo of the function tommorrow need to intialize"""
            with sr.Microphone() as source:
                print("Jarvis Active, Listening for command....")
                audio = r.listen(source)
                command = r.recognize_Jarvis(audio)
            """ Till here """

            # command = input("please enter the command ")
            # we are processing the command here 
            processCommand(command)

    # this is for the error exception 
    except Exception as e :
        print("Error; {0}".format(e))
    
    # this we are not using 
    # except sr.UnknownValueError:
    #     print(" could not understand audio")
    # except sr.RequestError as e:
    #     print("Sphinx error; {0}".format(e))