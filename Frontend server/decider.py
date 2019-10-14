import pyttsx3
import speech_recognition as sr
import re
import pandas as pd
from command import *
import requests

global regex_data

regex_data = pd.read_csv("regex.csv")

engine= pyttsx3.init('sapi5')
voices= engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voices',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#new yet to be embedded opens mic and listens to calls...(be safe)
def auto_listen():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening....")
        while True:
            audio = r.adjust_for_ambient_noise(source)
            #r.pause_threshold = 1
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio,language='en-in')
                query = query.lower()
                print(query)
                if "yo yo" in query:
                    speak("yes tell me")
                    decide_speak()
            except:
                pass



def takecommand():
    '''take input as speech and
    gives string in return'''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening.....")
        audio = r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, phrase_time_limit=10)
    try:
        print("recognizing...")
        query = r.recognize_google(audio,language='en-in')
        #speak("please wait")
        #print(f"user said: {query}\n")
        return query
    except Exception as e:

        print("say that again please...")
        return None

def decide_type(query):
    query = query.lower()
    response = None
    # query = 'Start camera'
    # exit()
    if query is not None:
        # speak(query)
        for row, key in zip(regex_data["regex"], regex_data["key"]):
            if re.match(row, query) is not None:
                if re.match(row, query).group() == query:
                    response = command_caller(key, query)
                    #speak(response)
                    return response


                ############################link to server########################
        if response is None:
            reply = requests.post("http://192.168.137.1:8000/chatbot/",data= query)
            #print(reply)
            #speak(reply)
            return reply.text

def decide_speak():
    query = takecommand()
    #query = 'Start camera'
    #exit()
    if query is not None:
        query = query.lower()
        response = None
        #speak(query)


        for row, key in zip(regex_data["regex"],regex_data["key"]):
            if re.match(row, query) is not None:
                if re.match(row, query).group() == query:
                    response = command_caller(key, query)
                    #speak(response)
                    return response
        ###################link to server###########################
        if response is None:
            reply = requests.post("http://192.168.137.1:8000/chatbot/", data=query)
            # print(reply)
            # speak(reply)
            return reply.text

#if __name__ == "__main__":


    #auto_listen()
#decide_speak()