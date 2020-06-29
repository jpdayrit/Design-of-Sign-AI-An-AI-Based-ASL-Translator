# -*- coding: utf-8 -*-
"""
tkinter GUI for Sign AI.

"""

import tkinter as tk
from multiprocessing import Process, Queue
from queue import Empty
from myo.utils import TimeInterval
import myo
import collections
import numpy as np
import time
import subprocess
from gtts import gTTS
from playsound import playsound
import os
import speech_recognition as STT

my_queue = Queue()

class Listener(myo.DeviceListener):

    def __init__(self):
        self.interval = TimeInterval(None, 0.05)
        self.orientation = None
        self.pose = myo.Pose.rest # unused
        self.emg_enabled = True
        self.locked = False
        self.rssi = None
        self.emg = None

    def output(self):
        if not self.interval.check_and_reset():
          return      
        
        sample_count = int(np.loadtxt('sample_count.txt'))
        sample_limit = 50
        
        # files containing EMG and orientation data. 
        quat_w = open("quaternion_w" + ".txt", "a+")
        quat_i = open("quaternion_i" + ".txt", "a+")
        quat_j = open("quaternion_j" + ".txt", "a+")
        quat_k = open("quaternion_k" + ".txt", "a+")
        
        emgPod_1 = open("emgPod1" + ".txt", "a+")
        emgPod_2 = open("emgPod2" + ".txt", "a+")    
        emgPod_3 = open("emgPod3" + ".txt", "a+")    
        emgPod_4 = open("emgPod4" + ".txt", "a+")
        emgPod_5 = open("emgPod5" + ".txt", "a+")    
        emgPod_6 = open("emgPod6" + ".txt", "a+")    
        emgPod_7 = open("emgPod7" + ".txt", "a+")    
        emgPod_8 = open("emgPod8" + ".txt", "a+")
        
        # temp variables for EMG and orientation data. 
        quaternions_read = collections.deque(maxlen=4)      
        instances_quat = 4
        emg_read = collections.deque(maxlen=8)
        instances_emg = 8
        
        if sample_count != sample_limit: 
            if self.orientation and self.emg:
                
                # get orientation data. 
                for element in self.orientation:
                    quaternions_read.append(element)
                    instances_quat = instances_quat - 1
                    if instances_quat == 0:
                        quat_w.write(str(quaternions_read[0]) + ' ')
                        quat_i.write(str(quaternions_read[1]) + ' ')                
                        quat_j.write(str(quaternions_read[2]) + ' ')
                        quat_k.write(str(quaternions_read[3]) + ' ')
                        
                # get EMG data.             
                for element in self.emg:
                    emg_read.append(element)
                    instances_emg = instances_emg - 1
                    if instances_emg == 0:
                        emgPod_1.write(str(emg_read[0]) + ' ')
                        emgPod_2.write(str(emg_read[1]) + ' ')                
                        emgPod_3.write(str(emg_read[2]) + ' ')
                        emgPod_4.write(str(emg_read[3]) + ' ')
                        emgPod_5.write(str(emg_read[4]) + ' ')
                        emgPod_6.write(str(emg_read[5]) + ' ')
                        emgPod_7.write(str(emg_read[6]) + ' ')
                        emgPod_8.write(str(emg_read[7]) + ' ') 
                        
                        # updates sample count.             
                        sample_count = sample_count + 1
                        np.savetxt('sample_count.txt', [sample_count])
        
        else:
            pass
        
        # close files with orientation data once they will no longer be accessed.     
        quat_w.close()
        quat_i.close()
        quat_j.close()
        quat_k.close()
        
        # close files with EMG data once they will no longer be accessed.
        emgPod_1.close()
        emgPod_2.close()
        emgPod_3.close() 
        emgPod_4.close()
        emgPod_5.close()   
        emgPod_6.close()   
        emgPod_7.close()
        emgPod_8.close()
    
    def on_connected(self, event):
        event.device.request_rssi()
        event.device.stream_emg(True)

    def on_rssi(self, event):
        self.rssi = event.rssi
        self.output()

    def on_pose(self, event):
        self.pose = event.pose
        self.output()

    def on_orientation(self, event):
        self.orientation = event.orientation
        self.output()

    def on_emg(self, event):
        self.emg = event.emg
        self.output()
    
    def on_unlocked(self, event):
        self.locked = False
        self.output()

    def on_locked(self, event):
        self.locked = True
        self.output()
    
class SignAI_GUI():
    def __init__(self, root):
        
        self.root = root
        
        self.gestureText = tk.Label(master=self.root, text="Latest Gesture : ")
        self.gestureText.grid(row=0)
        self.gestureOutput = tk.Entry(master=self.root)
        self.gestureOutput.grid(row=0, column=1)
        
        self.speechText = tk.Label(master=self.root, text="Latest Speech : ")
        self.speechText.grid(row=1)
        self.speechOutput = tk.Entry(master=self.root)
        self.speechOutput.grid(row=1, column=1)
        
        self.gestureButton = tk.Button(master=self.root, text="Perform ASL", 
                                       width=15,
                                       command=self.onGestureButton)
        self.gestureButton.grid(row=2)
        
        self.speechButton = tk.Button(master=self.root, text="Listen to Others",
                                      width=15,
                                      command=self.onSTT)
        self.speechButton.grid(row=2, column=1)
        
        self.text2speechButton = tk.Button(master=self.root, text="Speak", 
                                           width=15,
                                           command=self.onTTS)
        self.text2speechButton.grid(row=3)
        
    def onTTS(self):
        self.text2speechButton.config(state=tk.DISABLED)
        self.gesture = str(np.genfromtxt("output_gesture.txt", dtype="str"))
        self.TTS_process = Process(target=perform_TTS, args=(self.gesture,))
        self.TTS_process.start()
        self.root.after(10, self.onWaitTTS)
        
    def onWaitTTS(self):
        if (self.TTS_process.is_alive()):
            self.root.after(10, self.onWaitTTS)
            return
        else:
            self.text2speechButton.config(state=tk.NORMAL)
            
    def onSTT(self):
        self.speechButton.config(state=tk.DISABLED)
        self.STT_process = Process(target=perform_STT, args=(my_queue,))
        self.STT_process.start()
        self.root.after(10, self.onWaitSTT)
    
    def onWaitSTT(self):
        if (self.STT_process.is_alive()):
            self.root.after(10, self.onWaitSTT)
            return
        else:
            self.speechOutput.delete(0, tk.END)
            self.speechOutput.insert(0, my_queue.get(0))
            self.speechButton.config(state=tk.NORMAL)
        
    def onGestureButton(self):
        self.gestureButton.config(state=tk.DISABLED)
        self.acquire_process = Process(target=onGetGesture, args=(my_queue,))
        self.acquire_process.start()
        self.root.after(10, self.onPrintGesture)
          
    def onPrintGesture(self):
        if (self.acquire_process.is_alive()):
            self.root.after(50, self.onPrintGesture)
            return
        else:
            try:
                self.gestureOutput.delete(0, tk.END)
                self.gestureOutput.insert(0, my_queue.get(0))
                self.gestureButton.config(state=tk.NORMAL)
            except Empty:
                print("\nQueue is empty.")

                
def onGetGesture(my_queue):
    start_hub() # begin acquiring sensor data. 
    output = subprocess.call("contact_NN.py", shell=True)
    output = np.genfromtxt("output_gesture.txt", dtype="str")
    my_queue.put(output)
    reset() # dump out data in sensor files. 
    
def start_hub():
    myo.init('myo-sdk-win-0.9.0/bin/myo64.dll')
    hub = myo.Hub()
    listener = Listener()
    max_time_allowed = 3.5 # in seconds.
    start = time.time()

    while hub.run(listener.on_event, 500):
        if time.time() - start > max_time_allowed:
            hub.stop()
            break
        
def reset():
    
    file_directory = ["emgPod1.txt", "emgPod2.txt", "emgPod3.txt",
                      "emgPod4.txt", "emgPod5.txt", "emgPod6.txt",
                      "emgPod7.txt", "emgPod8.txt", 
                      "quaternion_w.txt", "quaternion_i.txt", 
                      "quaternion_j.txt", "quaternion_k.txt"]
    
    # reset data files after use. 
    for files in file_directory:
        doc = open(files, "w")
        doc.write('')
        doc.close()
    
    # reset sample count to 0. 
    np.savetxt("sample_count.txt", [int(0)])

def perform_TTS(gesture):
    
    sound_file = "output_TTS.mp3"
    
    # passes text to Google Voice. 
    tts = gTTS(text=gesture, lang="en")
    
    # saves text as .mp3. 
    tts.save(sound_file)
    
    # play .wav file via playsound.
    playsound(sound_file)
    
    # deletes sound file after use.
    os.remove(sound_file)
    
def perform_STT(my_queue):
    output = speech2text()
    my_queue.put(output)

def speech2text():
    
    # initialize gTTS.
    converter = STT.Recognizer()
    
    with STT.Microphone() as sound:
        
        # filter out noise when audio is received. 
        converter.adjust_for_ambient_noise(sound)
        
        # acquire audio.
        output = converter.listen(sound)
        
        # store converted output in 'speech' variable.
        try:
            speech = converter.recognize_google(output)
        except:
            speech = 'Try again'
        
        return speech
    
def main():
    root = tk.Tk()
    app = SignAI_GUI(root)
    for child in root.winfo_children(): 
        child.grid_configure(padx=10, pady=10)
    root.mainloop()
    
if __name__ == '__main__':
    main()  


