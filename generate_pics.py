import os, sys
import ntpath

directory = "C:\\Users\\eyal\\Desktop\\python\\AirBattle"
i = 0
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"): 
        i +=1
        print("\""+filename+"\""+ ",")
