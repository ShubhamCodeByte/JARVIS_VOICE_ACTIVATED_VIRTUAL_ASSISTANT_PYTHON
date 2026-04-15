import speech_recognition as sr  # this we can use to call it using the short name sr
import webbrowser as wb
import pyttsx3
import musiclibrary
import pyjokes
import google.generativeai as genai

# this is for the playing of the audio file by gTTs
import pygame
import time


# installing the module for the voice change 
from gtts import gTTS

# for the api key from the .env file configured
import os 
from dotenv import load_dotenv

# Load the secret key from the .env file
try:
  load_dotenv()
  api_key = os.getenv("GEMINI_API_KEY")

  if not api_key:
      print("Error: No API key found. Check your .env file.")
  else:
      genai.configure(api_key=api_key)
  # to use the api key from the .env
except Exception as e :
  print("Error: {}".format(e))



# google ai studio api key 
genai.configure(api_key=api_key)


# Configure the AI to give short, voice-friendly answers
model = genai.GenerativeModel( 
    'gemini-3-flash-preview',
    system_instruction=(
            "You are Jarvis, a helpful and witty voice assistant. "
            "If asked about your identity, confirm you are Jarvis, a virtual assistant. "
            "Keep all answers extremely brief and conversational. "
            "Use only one or two short sentences. "
            "Do not use any markdown formatting like asterisks, bolding, or lists."
        ),
    )
chat = model.start_chat(history=[])

# function to process the command and give the output 
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

# creating the object for the recognition 
recognizer = sr.Recognizer()

# fuction to speak the text this is the older one to use the default voice 
def speak_old(text):
  engine = pyttsx3.init()
  engine.say(text)
  engine.runAndWait()

# this speak is with the gTTs
def speak(text):
    tts = gTTS(text)
    tts.save('jarvis.mp3')

    # 1. Initialize the mixer
    pygame.mixer.init()

    # 2. Load the music file (replace with your filename)
    pygame.mixer.music.load("jarvis.mp3")

    # 3. Start playback
    # -1 means the music will loop indefinitely, 0 plays it once
    pygame.mixer.music.play()

    # print("Playing music...")

    # 4. Keep the script running
    # Without a loop or delay, the script ends and the music stops immediately
    while pygame.mixer.music.get_busy():
        time.sleep(1)

    pygame.mixer.music.unload()
    os.remove("jarvis.mp3")


# this will process the command 
def processCommand(c: str):
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
   link = musiclibrary.music[song]   
   wb.open(link)
  elif(c.lower() == "say joke") :
   speak("here is a joke for you.")
   speak(giveJoke())
  else :
     processGenAi(c.lower())



COMMAND_LIMIT = 20
COMMAND_PAUSE = 0.5
MIC_SENSITIVITY = 300

r = sr.Recognizer()
   
  



if __name__ == "__main__" :

  speak("Initializing Jarvis ......")
  while True:
    # Listening for the word "Jarvis"
    # obtain audio from the microphone
    # r = sr.Recognizer() this i am keeping the thing to run only one time

    # this is to clear the word and the commnad after every execution 
    word = ""
    command = ""

    try:
        # print("Sphinx thinks you said " + r.recognize_sphinx(audio))
        # command = r.recognize_sphinx(audio)  we are not using this as this is not giving the proper answer

        """ This is just for the silent demo tommorow we will initialize it """
        with sr.Microphone() as source:
            print("Listening.......")
       
            # 1. This is the magic line that fixes inconsistency!
            r.adjust_for_ambient_noise(source, duration=1)  # this i am keeping outside this so that it will run only one time and will not take the extra lag
            print("Caliberating...")
            r.pause_threshold = 0.5       # Wait 1 seconds of silence before stopping (default 0.8)
            r.energy_threshold = 300       # Mic sensitivity (adjust if noisy environment)
            r.dynamic_energy_threshold = True  # Auto-adjusts to background noise

            audio = r.listen(source,timeout=None,phrase_time_limit=2)  # this is for listening **Timeout** = max wait time to start talking; **Phrase Limit** = max length of the recording.
            print("Recognizing......")
        word = r.recognize_google(audio, language='en-in')
        print(word)
      
        #check for the two word to invoke the command listening 
        if ("jarvis" in word.lower() or "google" in word.lower()):    # we can escape the brackets while using the statement of if in this format  # this is good as i have increased the time limit of listening 
            speak("yes how may i help you")
            # Tune the recognizer BEFORE listening
            r.pause_threshold = COMMAND_PAUSE        # Wait 1 seconds of silence before stopping (default 0.8)
            # r.energy_threshold = MIC_SENSITIVITY       # Mic sensitivity (adjust if noisy environment)
            r.dynamic_energy_threshold = True  # Auto-adjusts to background noise

            # Listen for command 
            while(1):
                try :
                
                    with sr.Microphone() as source:
                        print("Jarvis Active, Listening for command....")
                        # timeout=5: Waits 5 seconds for you to START talking
                        # phrase_time_limit=12: Stops recording after 12 seconds total 
                        # This keeps the Gemini input short and prevents token exhaustion
                        audio = r.listen(
                        source,
                        timeout=5,
                        phrase_time_limit=COMMAND_LIMIT, # this will auto stop as the threshold is set 
                        )
                        command = r.recognize_google(audio, language='en-in')
                        print(command)
                        

                except sr.UnknownValueError:
                    speak("I didn't catch that. Will you please repeat it .")
                except sr.WaitTimeoutError:
                    speak("Sorry speech timeout closing")
                    break  # break the loop when timeout will come 
                except Exception as e:
                    print(f"Error: {e}")
                    break
                else:
                   break


            # we are processing the command here 
            processCommand(command)

    # # this is for the error exception 
    # except Exception as e :
    #     print("Error; {0}".format(e))
    
    except sr.UnknownValueError:
            print("Jarvis: I didn't catch that.")
    except sr.WaitTimeoutError:
            pass # No speech detected
    except Exception as e:
            print(f"Error: {e}")
    