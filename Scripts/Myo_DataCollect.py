"""
Record orientation and EMG data from Myo and log in a text file. 

"""

from __future__ import print_function
from myo.utils import TimeInterval
import myo
import collections

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
    
    sample_parameters = collections.deque(maxlen=2)
    sample_limit = 50
    
    with open("sample_parameters.txt") as file_sampleParam:
        for line in file_sampleParam:
            for num in line.split(','):
                sample_parameters.append(int(num))
                
    sample_count = sample_parameters[0]
    sample_number = sample_parameters[1]
    
    if sample_count == sample_limit:
        contVar = int(input("Do you want to continue? "))
        if contVar == 1:
            sample_number = sample_number + 1
            sample_count = 0
        else:
            pass
        
    else: 
            
        quat_w = open("quaternion_w" + "_" + str(sample_number) + ".txt", "a+")
        quat_i = open("quaternion_i" + "_" + str(sample_number) + ".txt", "a+")
        quat_j = open("quaternion_j" + "_" + str(sample_number) + ".txt", "a+")
        quat_k = open("quaternion_k" + "_" + str(sample_number) + ".txt", "a+")
        
        emgPod_1 = open("emgPod1" + "_" + str(sample_number) + ".txt", "a+")
        emgPod_2 = open("emgPod2" + "_" + str(sample_number) + ".txt", "a+")    
        emgPod_3 = open("emgPod3" + "_" + str(sample_number) + ".txt", "a+")    
        emgPod_4 = open("emgPod4" + "_" + str(sample_number) + ".txt", "a+")
        emgPod_5 = open("emgPod5" + "_" + str(sample_number) + ".txt", "a+")    
        emgPod_6 = open("emgPod6" + "_" + str(sample_number) + ".txt", "a+")    
        emgPod_7 = open("emgPod7" + "_" + str(sample_number) + ".txt", "a+")    
        emgPod_8 = open("emgPod8" + "_" + str(sample_number) + ".txt", "a+")    
           
        quaternions_read = collections.deque(maxlen=4)      
        instances_quat = 4
        emg_read = collections.deque(maxlen=8)
        instances_emg = 8
        
        if self.orientation and self.emg:
            
            for element in self.orientation:
                quaternions_read.append(element)
                instances_quat = instances_quat - 1
                if instances_quat == 0:
                    quat_w.write(str(quaternions_read[0]) + ' ')
                    quat_i.write(str(quaternions_read[1]) + ' ')                
                    quat_j.write(str(quaternions_read[2]) + ' ')
                    quat_k.write(str(quaternions_read[3]) + ' ')
    
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
            
            sample_count = sample_count + 1
        
        #print(quaternions_read)
        #print(emg_read)
        
        quat_w.close()
        quat_i.close()
        quat_j.close()
        quat_k.close()
        
        emgPod_1.close()
        emgPod_2.close()
        emgPod_3.close()
        emgPod_4.close()
        emgPod_5.close()
        emgPod_6.close()
        emgPod_7.close()
        emgPod_8.close()
        
    file_sampleParam = open("sample_parameters.txt", "w")
    file_sampleParam.write(str(sample_count) + ',' + str(sample_number))
    file_sampleParam.close()
    
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

    
if __name__ == '__main__':
  
  myo.init('myo-sdk-win-0.9.0/bin/myo64.dll')
  hub = myo.Hub()
  listener = Listener()
  while hub.run(listener.on_event, 500):
      pass
