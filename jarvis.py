import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2

import random
from requests import get
import requests
from bs4 import BeautifulSoup
import wikipedia
import webbrowser
import pywhatkit as kit
import calendar
from datetime import date
import sys
import time
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisUi import Ui_jarvisUi


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voices',voices[0].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        speak("Good Morning Sir")
    elif hour>=12 and hour<18:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")
    curr_date = date.today()
    curr_day = calendar.day_name[curr_date.weekday()]
    speak(f"its {curr_date}")
    speak(f"its {curr_day}")
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"the time is {strTime}")
    speak("I am jarvis , please tell me how can i help you?")

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()


    def takecommand(self):

            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 1
                audio = r.listen(source,timeout = 10 ,phrase_time_limit=5)

            try:
                print("Recognizing...")
                query =r.recognize_google(audio, language='en-in')
                print(f"user said: {query}")

            except Exception as e:
                speak("Say that again please")
                return "None"
            query = query.lower()
            return query

    def TaskExecution(self):
        wish()
        while True:
            self.query = self.takecommand()

            if "notepad" in self.query:
                npath="C:\\WINDOWS\\system32\\notepad.exe"
                os.startfile(npath)
                speak("notepad is open sir note it out ")

            elif "kill notes" in self.query:
                speak("okay sir, closing notepad")
                os.system("taskkill /f /im notepad.exe")
            elif "how are you" in self.query:
                speak("I am absolutely fine sir,what about you ? ")

            elif "open cmd" in self.query:
                os.system("start cmd")
                speak("command prompt is live")

            elif "close cmd" in self.query:
                speak("okay sir, closing command prompt")
                os.system("taskkill /f /im cmd.exe")

            elif "open camera" in self.query:
                speak ("just a second!,starting camera")
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam',img)
                    k = cv2.waitKey(50)
                    if k==27:
                        break;
                cap.release()
                cv2.destroyAllWindows()



            elif "play music" in self.query:
                speak ("jsut a second sir! ,Starting Music")
                music_dir ="E:\\music"
                songs =os.listdir(music_dir)
                os.startfile(os.path.join(music_dir,songs[0]))


            elif "ip address" in self.query:
                ip =get('https://api.ipify.org').text
                speak(f"your IP address is {ip}")

            elif "wikipedia" in self.query:
                speak("searching wikipedia...")
                self.query = self.query.replace("wikipedia","")
                results =wikipedia.summary(self.query, sentences=2)
                speak("acccording to wikipedia")
                speak(results)


            elif "open youtube" in self.query:
                # speak("what should you looking for on youtube")
                # am =takecommand().lower()
                webbrowser.open("www.youtube.com")

            elif "open facebook" in self.query:
                webbrowser.open("www.facebook.com")

            elif "open stackoverflow" in self.query:
                webbrowser.open("www.stackoverflow.com")

            elif "open google" in self.query:
                speak("sir,what should i search on google")
                cm =self.takecommand()
                webbrowser.open(f"{cm}")


            elif "send message" in self.query:
                # speak("sir,what is the message ")
                # ms =takecommand().lower()
                kit.sendwhatmsg("+919370246005","hii",13,5)
            elif "open gmail " in self.query:
                webbrowser.open("mail.google.com")

            elif "set alarm" in self.query:

                nm=(datetime.datetime.now().hour)
                speak("setting alarm")
                if nm==22:
                    music_dir = 'E:\\music'
                    songs = os.listdir(music_dir)
                    os.startfile(os.path(music_dir,songs[0]))

            elif "temperature" in self.query:
                search ="temperature in Bhusawal"
                url =f"https://www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text,"html.parser")
                temp = data.find("div",class_="BNeawe").text
                speak(f"current {search} is {temp}")

            elif "wait" in self.query:
                speak("ok sir,waiting for your command!")
                time.sleep(5)
            elif "no sleep"  in self.query:
                speak("thanks for using me sir, have a good day!")
                sys.exit()

            speak ("Sir,do you have any other work ")

    # if __name__== "__main__":
    #     while True:
    #         self.permission = self.takecommand()
    #         if "wake up" in permission:
    #             TaskExecution()
    #         elif "goodbye" in permission:
    #             sys.exit()


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_jarvisUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:/Users/locha/PycharmProjects/firstpythonProject/venv/gif1.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie ("C:/Users/locha/PycharmProjects/firstpythonProject/venv/gif2.gif")
        self.ui.label_2.setMovie (self.ui.movie)
        self.ui.movie.start ()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date =QDate.currentDate()
        label_time = current_time.toString("hh:mm:ss")
        label_date =current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText (label_date)
        self.ui.textBrowser.setText (label_time)



app =QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())