import os, sys


directory = "C:\Users\eyal\Desktop\python\AirBattle\images\explosion1_package\package\png frames\640x480"
i = 0
for filename in os.listdir(directory):
    os.rename(filename, "expl" + str(i) + ".png")
    i+=1
