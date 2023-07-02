#
 # This file is part of the SpotifyStatsCreator distribution (https://github.com/Chareste/SpotifyStatsCreator).
 # Copyright (c) 2023 Chareste.
 #
 # This program is free software: you can redistribute it and/or modify
 # it under the terms of the GNU General Public License as published by
 # the Free Software Foundation, version 3.
 #
 # This program is distributed in the hope that it will be useful, but
 # WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 # General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 #

import json
import os
from pathlib import Path
from enum import Enum
import plotext as plt
import numpy as np
import time as tume

class DayTime(Enum):
   Night=0
   Deep_night=1
   Early_morning=2
   Late_morning=3
   Early_afternoon=4
   Afternoon=5
   Evening=6
   Late_evening=7

print("It's time to display your stats!")

data_path = Path(os.getcwd()+"/out/data.json")
info_path =Path(os.getcwd()+'/out/additionalInfo.json')
if data_path.is_file() and info_path.is_file:
   with open(data_path) as data_file, open(info_path) as info_file:
      data = json.load(data_file)
      info = json.load(info_file)
else:
   print("You need to run a parser before to elaborate your data!")
   print("Check the README and try again later.")
   exit(1)


#isExtended = 0;
elabdatini = {}
artistalley= {}
f=open("out.txt", "w")
totalMillis = info["TotalMS"]
for i, val in enumerate(sorted(data.items(), key=lambda x:x[1]['TimesPlayed'], reverse=True)):

   elabdatini[i] ={'ID':val[0]}|val[1]

   #the list divided by artists
   if val[1]['Artist'] not in artistalley:
      artistalley[val[1]['Artist']] = {"totalMillis": 0, "totalListens": 0, "Tracks": {}, "timeDistribution": [0]*8}
   for j,t in enumerate(val[1]['timeDistribution']):
      artistalley[val[1]['Artist']]['timeDistribution'][j] += val[1]['timeDistribution'][j]
   artistalley[val[1]['Artist']]['totalMillis'] += val[1]['msPlayed']
   artistalley[val[1]['Artist']]['totalListens'] += val[1]['TimesPlayed']
   artistalley[val[1]['Artist']]['Tracks'][val[1]['Title']] = {"ID": val[0], "TimesPlayed": val[1]['TimesPlayed']}


f.write(f"- Stats fetched for {info['User']} -\n"
        f"Total play time: {totalMillis//(60*60*1000)}:{(totalMillis//(60*1000))%60:02d}:{(totalMillis//1000)%60:02d}, "
        f"equating to at least {totalMillis//(24*60*60*1000)} days.\n\n")

f.close()
f=open("out.txt", "a")

#elaborating the graph with plotext
plt.clc()
plt.plot_size(400, 15)
plt.xlim(right=25)
plt.ylim(0,int(np.max(info['DayDistribution'])*1.05))
plt.vline(np.argmax(info['DayDistribution'])+1, "blue")
plt.yaxes(False, False)
plt.xticks(range(1,27,3),[i*3 for i in range(0,9)])
plt.yticks([])
plt.title("Listens distribution throughout the day")
plt.xlabel("Hour")
plt.grid(False,True)

x = list(range(0,24))
y = [info['DayDistribution'][i] for i in x]
y.append(info['DayDistribution'][0] )

plt.plot(y,fillx=False, color= 40, marker="hd")
plt.show()
tume.sleep(0.1)
plt.save_fig(os.getcwd()+'/out.txt',append=True)
tume.sleep(0.1)

  
f.write("\nTop 100 most played songs\n") 
f.write("-----------------------------------\n")
for i in elabdatini:
   if i >= 100:
      f.write("You'll find the full leaderboard in tracksData.json\n")
      break
   time = []
   # ---: {'ID': '---', 'Artist': '---', 'Title': '---', 'msDuration': ---, 'TimesPlayed': ---, 'msPlayed': ---, 'timeDistribution': [---]}

   for index,j in enumerate(elabdatini[i]['timeDistribution']):
      if not time:
         time.append(index)
      else:
         if elabdatini[i]['timeDistribution'][index] >elabdatini[i]['timeDistribution'][time[0]]:
            time = [index]
         elif elabdatini[i]['timeDistribution'][index] == elabdatini[i]['timeDistribution'][time[0]]:
            time.append(index)

   f.write(f" {i+1}: {elabdatini[i]['Title']} by {elabdatini[i]['Artist']}\n")
   f.write(f"   Played {elabdatini[i]['TimesPlayed']} times for a total of {elabdatini[i]['msPlayed']//(60*60*1000)}"
           f":{(elabdatini[i]['msPlayed']//(60*1000))%60:02d}:{(elabdatini[i]['msPlayed']//1000)%60:02d}.\n"
           f"   Average plays by song length: {elabdatini[i]['msPlayed']/elabdatini[i]['msDuration']:.2f}\n"
           f"   You've listened to this song mostly during {DayTime(time.pop(0)).name.replace('_',' ')}")
   for j in time:
      f.write(f", {DayTime(time.pop(0)).name.replace('_',' ')}")
   f.write("\n\n")
   
f.write("\nStats by artist - Top 50\n")
f.write("-----------------------------------\n")

artists={}
for i, val in enumerate(sorted(artistalley.items(), key=lambda x:x[1]['totalListens'], reverse=True)):

   artists[val[0]]={"Position":i+1}|val[1]


for i, val in enumerate(artists):
   if i>= 50:
      f.write("You'll find the data for every artist in artistsData.json\n")
      break

   time = []
   for index, j in enumerate(artists[val]['timeDistribution']):
      #print(j, artists[val]['timeDistribution'])
      if not time:
         time.append(index)
      else:
         if artists[val]['timeDistribution'][index] > artists[val]['timeDistribution'][time[0]]:
            time = [index]
         elif artists[val]['timeDistribution'][index] == artists[val]['timeDistribution'][time[0]]:
            time.append(index)

   f.write(f"{i+1}: {val}\n")
   f.write(f"   Played their tracks {artists[val]['totalListens']} times for a total of {artists[val]['totalMillis']//(60*60*1000)}:"
           f"{(artists[val]['totalMillis']//(60*1000))%60:02d}:{(artists[val]['totalMillis']//1000) %60:02d}.\n"
           f"   You've listened to this artist mostly during {DayTime(time.pop(0)).name.replace('_', ' ')}.\n")
   for j in time:
      f.write(f", {DayTime(time.pop(0)).name.replace('_', ' ')}")

   f.write("   Top 5 songs:\n")
   #print(artists[val])
   for j,s in enumerate(sorted(artists[val]['Tracks'].items(),key= lambda x:x[1]['TimesPlayed'], reverse=True)):
      #print(s)
      if j>=5:
         f.write("      [...]\n")
         break
      f.write(f"      {j+1}: {s[0]} - {s[1]['TimesPlayed']} times\n")
  
   
   
f.write("\n\nStats fetched and elaborated by SpotifyParser and SpotifyStatsDisplayer by github.com/Chareste\n"
        f"File updated at {info['LastUpdated']}")
#json files dump 
with open(os.getcwd()+'/out/tracksData.json', 'w') as elab, open(
        os.getcwd()+'/out/artistsData.json', 'w') as art:
    json.dump(elabdatini, elab)
    json.dump(artists, art)
f.close()

print("Done!")
   

   
   
   
   

   


