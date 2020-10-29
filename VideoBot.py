import wave 
import contextlib
import struct
import numpy as np
import ffmpeg
import subprocess
import os

allStartTimes = [] ## all the times when the beat happens, we dont need the end because it would cause cuts in the video


def videoFiles():
    videoInput = input("Where is the top tier video: ")
    outputTXT = input("Where do you want the top tier video to be (just give the folder): ")
    outputs = []
    i = 0
    while(i < len(allStartTimes) + 1): # the added one is because we cut according to the first start and thats a non zero number
        outputTXT = f'{outputTXT}\\Output{i}.mp4'
        if(i == 0):
            command = f'ffmpeg -i {videoInput} -ss 00 -to {allStartTimes[i]} {outputTXT}'
            os.system(command)
        elif i == len(allStartTimes):
            command = f'ffmpeg -i {videoInput} -ss {allStartTimes[i-1]} -to {get_length("F:/OldDrive/YouTube/Trying_Hacking/2020-03-28-11-09-11.mp4")} {outputTXT}'
            os.system(command)
        else:
            command = f'ffmpeg -i {videoInput} -ss {allStartTimes[i-1]} -to {allStartTimes[i]} {outputTXT}'
            print(command)
            os.system(command)
        i = i + 1


def get_length(input_video):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)


fname = input("Where is the musica location: ")



with contextlib.closing(wave.open(fname, 'r')) as f: # opens the file in read only
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)

    start = 1
    end = 0
    startData = 0
    endData = 0
    for i in range(0,frames):
        waveData = f.readframes(1)
        data = struct.unpack("<2h", waveData)
        if (start == 1):
            if (len(str(int(data[0])))>=len(str(1234))):
                count=count+1
            else:
                count=0
            if (count == 100):
                startData=i-100
                count = 0
                start = 0
                end = 1
        if (end == 1):
            if (len(str(int(data[0])))<=len(str(123))):
                count=count+1
            else:
                count=0
            if (count == 10):
                endData=i-10
                count = 0
                start = 1
                end = 0
                frames=endData-startData
                duration=frames/float(rate)
                if  duration > 0.09:
                    print("Start "+str(startData/float(rate)))
                    print("End "+str(endData/float(rate)))
                    print("Duration: "+str(duration))
                    allStartTimes.append(startData/float(rate))
    videoFiles()
#IT WORKS YAY
