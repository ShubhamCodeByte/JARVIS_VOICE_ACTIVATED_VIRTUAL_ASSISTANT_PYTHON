import speech_recognition as sr  # this we can use to call it using the short name sr
import webbrowser as wb
import pyttsx3
import musiclibrary
# import requests
import pyjokes
import google.generativeai as genai


# google ai studio api key 
genai.configure(api_key="AIzaSyCOwxmoiiTBfuawQUZDDf-lvRoSaN_hJlE")


# Configure the AI to give short, voice-friendly answers
model = genai.GenerativeModel(
    # 'gemini-1.5-flash',     # this is the older version this is not working 
    'gemini-3-flash-preview',
    system_instruction="You are a helpful voice assistant. Keep your answers extremely brief, conversational, and to the point. Use only 1 or 2 short sentences. Do not use asterisks, bolding, or lists."
)
chat = model.start_chat(history=[])

# function to process the command and give the out put 
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

# This is to give the random joke using the pyjoke module 
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
  elif c.lower().startswith("open website") :           # **this is added to open the websites dynamically 
   website = c.lower().split(" ")[2]
   speak(f"opening {website}")                       
   wb.open(f"https://www.{website}.com/")
  elif c.lower().startswith("play") :
   song = c.lower().split(" ")[1]
   speak(f"playing {song}")
   link = musiclibrary.music[song]    # mistake : i have used the parenthesis here but this is a dictionary 
   wb.open(link)
  elif(c.lower() == "say joke") :
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
       
            # 1. This is the magic line that fixes inconsistency!
            r.adjust_for_ambient_noise(source, duration=0.5)

            audio = r.listen(source,timeout=3,phrase_time_limit=2)  # this is for listening **Timeout** = max wait time to start talking; **Phrase Limit** = max length of the recording.
        word = r.recognize_google(audio)
        print(word)
        
        """---------------------------------------------------------------------"""

        # this is just for the demo 
        # word = input("Please enter the command to activate.... \n:")
        # if(word.lower() == "jarvis" or word.lower() == "google"):
        if ("jarvis" in word.lower() or "google" in word.lower()):     # this is good as i have increased the time limit of listening 
            speak("yes how may i help you")
            # Tune the recognizer BEFORE listening
            r.pause_threshold = 1.5        # Wait 2 seconds of silence before stopping (default 0.8)
            r.energy_threshold = 300       # Mic sensitivity (adjust if noisy environment)
            r.dynamic_energy_threshold = True  # Auto-adjusts to background noise

            # Listen for command 
            """This is disabled only for the demo of the function tommorrow need to intialize"""
            with sr.Microphone() as source:
                print("Jarvis Active, Listening for command....")
                # timeout=5: Waits 5 seconds for you to START talking
                # phrase_time_limit=12: Stops recording after 12 seconds total 
                # This keeps the Gemini input short and prevents token exhaustion
                audio = r.listen(
                   source,
                   timeout=5,
                   phrase_time_limit=33, # this will auto stop as the threshold is set 
                   )
                command = r.recognize_google(audio)
                print(command)
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