# -*- coding: utf-8 -*-
"""
Created on Mon May  4 23:20:03 2020

@author: joshe
"""

from __future__ import print_function
from myo.utils import TimeInterval
import myo
import collections
import numpy as np
from lstm_final_model_load import create_and_predict_model
import sys 
    
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
                    
                    # updates sample count (max: 50).             
                    sample_count = sample_count + 1
                    np.savetxt('sample_count.txt', [sample_count])
                    
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
    
    else:
        print('\nTranslating gesture...') # flavor text.
        
        # retrieve all data as arrays. 
        emgPod_1 = np.loadtxt("emgPod1" + ".txt")
        emgPod_2 = np.loadtxt("emgPod2" + ".txt")
        emgPod_3 = np.loadtxt("emgPod3" + ".txt")
        emgPod_4 = np.loadtxt("emgPod4" + ".txt")
        emgPod_5 = np.loadtxt("emgPod5" + ".txt")
        emgPod_6 = np.loadtxt("emgPod6" + ".txt")
        emgPod_7 = np.loadtxt("emgPod7" + ".txt")
        emgPod_8 = np.loadtxt("emgPod8" + ".txt")
        quat_w = np.loadtxt("quaternion_w" + ".txt")
        quat_i = np.loadtxt("quaternion_i" + ".txt")
        quat_j = np.loadtxt("quaternion_j" + ".txt")
        quat_k = np.loadtxt("quaternion_k" + ".txt")
        
        # stack data element-wise.
        input_data= np.dstack((emgPod_1, emgPod_2, emgPod_3, 
                               emgPod_4, emgPod_5, emgPod_6, 
                               emgPod_7, emgPod_8, quat_i, 
                               quat_j, quat_k, quat_w)) 
        
        # reshape for use in NN.
        input_data = np.array(input_data).reshape((1, 50, 12))
        
        # interface with NN.
        gesture = create_and_predict_model(input_data)
        
        # print output. 
        print('\nYou said: "' + str(gesture) + '."')        
    
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
    
    
    

    



