import speech_recognition as sr  # this we can use to call it using the short name sr
import webbrowser as wb
import pyttsx3
import musiclibrary


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
  #  if (c.lower() == "open google"):    this we are not using we are using this in different fromat

  if "open google" in c.lower() :
   wb.open("https://www.google.com/")
  elif "open facebook" in c.lower() :
   wb.open("https://www.facebook.com/")
  elif "open linkedin" in c.lower() :
   wb.open("https://www.linkedin.com/")
  elif "open youtube" in c.lower() :
   wb.open("https://www.youtube.com/")
  elif c.lower().startswith("play") :
   music = c.lower().split(" ")[1]
   wb.open(musiclibrary.music(music))    
   pass 



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
        # with sr.Microphone() as source:
        #     print("Listening.......")
        #     audio = r.listen(source,timeout=2,phrase_time_limit=1)  # this is for listening one word only
        # # word = r.recognize_google(audio)
        
        """---------------------------------------------------------------------"""

        # this is just for the demo 
        word = input("Please enter the command to activate.... \n:")
        if(word.lower() == "jarvis"):
            speak("how are you ")

            # Listen for command 
            """This is disabled only for the demo of the function tommorrow need to intialize"""
            #  with sr.Microphone() as source:
            #     print("Jarvis Active, Listening for command....")
            #     audio = r.listen(source)
            #     command = r.recognize_google(audio)
            """ Till here """

            command = input("please enter the command ")
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