from tkinter.constants import CENTER
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
from wikipedia.wikipedia import languages
import tkinter as tk
import tkinter.font as tkf
import requests, json
from gnewsclient import gnewsclient
import cv2
import capture
import pyscreenshot
from pycaw.pycaw import AudioUtilities
import schedule
from youtube_search import YoutubeSearch
from pytube import YouTube

client = gnewsclient.NewsClient(language='english',location='india',max_results=3)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[4].id)

api_key = "5995f5e32100e6a622ffb2f0d088cb02"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
def setevery(jobhisetkrnah):
    w.config(text = jobhisetkrnah)
    w.update()
    speak(jobhisetkrnah)
    

    
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning")

    elif hour>=12 and hour<18:
        speak("Good Afternoon")

    else:
        speak("Good Evening")

    speak("Artemis at your Command Sir.")

def takeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Artemis : Listening ...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Artemis : Recognizing ...")
        query = r.recognize_google(audio, language='en-in')
        query=query.lower()

    except Exception as e:
        return "none"
    
    if 'artemis' not in query:
        return "none"
    else:
        query=query.replace("artemis ","^")
        query=query.replace("artemis","^")
        return query

def takeCommandMeow():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        w.config(text = "Listening")
        w.update()
        print("Artemis : Listening ...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Artemis : Recognizing ...")
        query = r.recognize_google(audio, language='en-in')
        print('command :',query.title())
        w.config(text = 'Command  : '+query.title())
        w.update()

    except Exception as e:
        print("Artemis : Please Repeat ...")
        return "None"
    return query

def takeCommandMeowAgain():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')

    except Exception as e:
        return "None"
    return query

def everything():
    wish()
    schedule.every().day.at("01:00").do(lambda:setevery("It is Quite Late Now, You Should Have Some Rest"))
    while True:
        schedule.run_pending()
        query=takeCommand()
        
        if query=="^":
            w.config(text = "Yes Sir !")
            w.update()
            speak("Yes Sir")
            query=takeCommandMeow().lower()
            
        if "^" in query:
            query=query.replace("^","")    
                        
        if 'youtube' in query:
            query = query.replace("search youtube for", "")
            query = query.replace("search on youtube", "")
            query = query.replace("youtube", "")
            query = query.replace(" ","+")
            webbrowser.open("https://www.youtube.com/results?search_query="+query)
            w.config(text = "Results are Shown in Browser")
            w.update()
            speak("These are some results")
            
        elif 'google' in query or 'search' in query:
            query = query.replace("google", "")
            query = query.replace("search", "")
            query = query.replace(" ","+")
            webbrowser.open("www.google.com/search?q="+query)
            w.config(text = "Results are Shown in Browser")
            w.update()
            speak("These are some results")
            
        elif 'capture' in query or 'selfie' in query:
            w.config(text = "Say Cheese, Hit Spacebar & Tell The Filename")
            w.update()
            speak("Say cheese, hit spacebar and tell the filename")
            capture.cap()
            setevery("Photo Saved Succesfully")
            
        elif 'screenshot' in query:
            setevery("Taking Screenshot")
            ss = pyscreenshot.grab()
            ss.show()
            setevery("Provide Filename")
            filename=takeCommandMeowAgain().title()
            os.chdir("C:\Everything\FRIDAY\Captures")
            ss.save(filename+".png")
            setevery("Screenshot Saved Succesfully")

        elif 'dnd' in query:
            if 'enable' in query or 'on' in query:
                mutevalue=1
            if 'disable' in query or 'off' in query:
                mutevalue=0
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                volume = session.SimpleAudioVolume
                volume.SetMute(mutevalue, None)
                setevery("DND Status Set Succesfully")
        
        elif 'what is the weather in' in query:
            query=query.replace("what is the weather in","")
            complete_url = base_url + "appid=" + api_key + "&q=" + query
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                weatext=(" Temperature = " +
                    str(round(current_temperature-273.15)) +
                    " \N{DEGREE SIGN}C\nPressure = " +
                    str(current_pressure) +
                    " hPa\nHumidity = " +
                    str(current_humidity) +
                    " Percent\nDescription = " +
                    str(weather_description).title())
                w.config(text=weatext)
                w.update()
                speak("The Temperature in "+query+" is "+str(round(current_temperature-273.15))+"degree celsius and the weather can be described as "+str(weather_description))
            else:
                w.config(text = 'City Not Found')
                w.update()
                speak("City Not Found")
                
        elif 'news' in query:
            news_list = client.get_news()
            for item in news_list:
                st = item['title'].split(' - ', 1)[0]
                w.config(text = st)
                w.update()
                speak(st)

        elif 'play' in query and 'music' in query:
            folder="C:\Everything\FRIDAY\Songs"
            os.chdir(folder)
            setevery("Do You Want To Play Existing Songs or Download New Ones")
            query=takeCommandMeowAgain()
            if 'download' in query:
                setevery("Which Song Would You Like To Download")
                query=takeCommandMeowAgain()
                results = YoutubeSearch(query, max_results=3).to_dict()
                setevery("Choose One of The Following")
                for res in results:
                    setevery(res['title'])
                query=takeCommandMeowAgain()
                if "second" in query:
                    gaanano=1
                elif "third" in query:
                    gaanano=2
                else:
                    gaanano=0
                linkgaana="https://www.youtube.com/watch?v="+results[gaanano]['id']
                yt = YouTube(linkgaana)
                video = yt.streams.filter(only_audio=True).first()
                out_file = video.download(output_path=".")
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                setevery("Succesfully Downloaded")
                w.config(text = 'Playing '+results[gaanano]['title'])
                w.update()
                speak("Playing Music")
                os.startfile(os.path.join(folder, new_file))
            else:
                songs = os.listdir(folder)
                w.config(text = 'Playing '+songs[0])
                w.update()
                speak("Playing Music")
                os.startfile(os.path.join(folder, songs[0]))
        
        elif 'suggest' in query:
            query = query.replace("suggest", "best")
            query = query.replace(" ","+")
            webbrowser.open("www.google.com/search?q="+query)
            w.config(text = "Results are Shown in Browser")
            w.update()
            speak("These are some results")
            
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H hours and %M minutes")
            w.config(text = 'The Time is '+strTime)
            w.update()
            speak("The Time is "+strTime)
            
        elif 'wikipedia' in query or 'what are' in query or 'what is' in query:
            query = query.replace("wikipedia", "")
            query = query.replace("what are", "")
            query = query.replace("what is","")
            try:
                results = wikipedia.summary(query, sentences=1)
            except:
                query = query.replace(" ","+")
                webbrowser.open("www.google.com/search?q="+query)
                w.config(text = "Results are Shown in Browser")
                w.update()
                speak("These are some results")
            else:
                w.config(text = 'According to Wikipedia '+results)
                w.update()
                speak("According to Wikipedia"+results)

        elif 'calculate' in query or 'evaluate' in query:
            query = query.replace(" ","")
            query = query.replace("calculate","")
            query = query.replace("evaluate","")
            if 'into' in query:
                query = query.replace("into","*")
            if 'by' in query:
                query = query.replace("by","/")
            try:
                result=eval(query)
            except:
                result="invalid"
            w.config(text = "Results is "+str(result))
            w.update()
            speak("Result is "+str(result))
            
        elif 'remember' in query or 'remind' in query:
            if 'what' not in query:
                query=query.replace("remember ","")
                query=query.replace("remind me","")
                fil = open("rem.txt","a")
                w.config(text = "Okay")
                w.update()
                speak("Okay")
                fil.write(query+"\n")
                fil.close()
            else:
                with open('rem.txt','r') as fil:
                    remtemp = fil.read()
                w.config(text = "You Told Me To Remember : \n"+remtemp.title())
                w.update()
                speak("You told me to remember "+remtemp)
                fil.close()
                os.remove("rem.txt")
        
        elif 'run' in query:
            query=query.replace("run ","")
            try:
                w.config(text = "Opening "+query)
                w.update()
                speak("Opening "+query)
                if (os.system(query))==1:
                    w.config(text = "Could Not Open")
                    w.update()
                    speak("Could not open")
            except:
                w.config(text = "Could Not Open")
                w.update()
                speak("Could not open")
                
        elif 'shutdown' in query:
            w.config(text = 'Shutting Down')
            w.update()
            speak("Shutting Down")
            os.system("shutdown -s")            

        elif 'bye' in query or 'exit' in query:
            w.config(text = 'Bella Ciao')
            w.update()
            speak("Bella Ciao")
            root.destroy()
            exit(0)

        elif 'none' in query:
            continue

        else:
            w.config(text = "I Coudn't Understand You. Try Rephrasing Your Statement")
            w.update()
            speak("I Coudnt Understand You. Try Rephrasing Your Statement")

root = tk.Tk()
root.attributes('-alpha',0.6)
root.attributes('-topmost', True)
root.overrideredirect(1)
root.geometry('300x150-20+20')
filename = tk.PhotoImage(file = "c:/meow.gif")
fs=tkf.Font(family='Impact',size=11)
w = tk.Label(root, text="Artemis At Your Command Sir !",pady=50,wraplength=200,image=filename,compound=CENTER,font=fs,foreground='white')
w.pack()
root.after(100,everything)
root.mainloop()