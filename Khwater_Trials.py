import random
from datetime import datetime
import json
import subprocess
import time
import urllib.request
import sqlite3
import os
"""
    This Program for choosing a Random Episode in Khwater(all_Seasons)
    and play it on Youtube (Google chrome)
"""
database = sqlite3.connect("repeated_episodes.db")
c = database.cursor()

def RANDOM():
    global Season,Episode
    # Get a Random number For both Season & Episode
    S = [random.randint(1,12) for item in range(0,12)]
    E = [random.randint(1,31) for item in range(0,31)]
    #using datetime library to get the current time
    now = datetime.now()
    date = now.day
    day = date
    if date >= 12:           #To avoid IndexError in case of the date >= 12
        if date <= 19:
            date = date - 7
        else:
            date = date - 19
    Season = S[date-1]
    Episode = E[day-1]

def check_if_repeated():
    global Season,Episode
    RANDOM()
    s = Season
    e = Episode
    c.execute("SELECT season,episode FROM data")
    for row in c.fetchall():
        if row[0] == Season and row[1] == Episode:
            RANDOM()
    if Season == s and Episode == e:
        c.execute("INSERT INTO data (season,episode) VALUES (?,?)",(s,e))
        database.commit()
    else:
        c.execute("INSERT INTO data (season,episode) VALUES (?,?)",(Season,Episode))
        database.commit()

Links = {
1:"PL5EE49DD2D8C38ECE",
2:"PLA1D51FAF0DD5845E",
3:"PL6C2F3DADE0A1232F",
4:"PL467132E986FD1EC9",
5:"PL8C23FDC1CB110A08",
6:"PL9AF792A465B7FD1D",
7:"PLDC04C71919C9A445",
8:"PLvKVYdfmki7X6dsNLI88AscMkiAmH8Gjb",
9:"PLtQ6jVwjgfV3kJtGgLiQcHjQONJUCZ35I",
10:"PLvKVYdfmki7U-vzbMuTEklVotWJF1cUrh",
11:"PLvKVYdfmki7XCRIjnidascLtTLwWECEHM",
12:"PLjTPwkeuXS8RXFr24Z9kbJM6spnXGxBpS"
}

def getItems(link):
    global Season,Episode
    apiKey = "AIzaSyDYRfQ7NkfRh7VjEjmrRPMqiAOaA0wPmx4nOx74Gjhu827Jgspri53B5nb"
    json_format = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s&maxResults=50&key=apiKey" % link)
    json_format_read =json_format.read()
    json_format_decode = json_format_read.decode("utf-8")
    data = json.loads(json_format_decode)
    Vid_Ids = []
    for i in data['items']:
        Vid_Ids.append(i['snippet']['resourceId']['videoId'])
    V_id = Vid_Ids[Episode-1]
    Chrome_dist = find("chrome.exe",'C:\\')
    # subprocess.Popen([r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", "https://www.youtube.com/watch?v=%s" % V_id ])
    subprocess.Popen(["%s"% Chrome_dist, "https://www.youtube.com/watch?v=%s" % V_id ])


def show():
    global Season,Episode
    #table()
    RANDOM()
    check_if_repeated()
    if Season == 12:
        if Episode > 19 :
            Episode = Episode - 12
            #print(Season,Episode)
            getItems(Links[12])
        #print(Season,Episode)
        getItems(Links[12])
    else:
        #print(Season,Episode)
        getItems(Links[Season])

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


starting = time.time()

show()
c.close()
database.close()

ending = time.time()
print(ending - starting)

#Recourses :
#http://stackoverflow.com/questions/35245246/how-can-you-open-a-url-with-a-specified-web-browser-in-python-3
#http://stackoverflow.com/questions/14858879/split-txt-file-to-multiple-files-named-according-to-their-contents-in-python
