# -*- coding: utf-8 -*-
"""

Retrieve data from Myo armband for a specified period of time. 

"""

from get_myo_data import Listener 
import myo
import time

def start_hub():
    
    myo.init('myo-sdk-win-0.9.0/bin/myo64.dll')
    
    hub = myo.Hub()
    
    listener = Listener()
    
    max_time_allowed = 4 # in seconds.
    
    start = time.time()

    while hub.run(listener.on_event, 500):
        if time.time() - start > max_time_allowed:
            hub.stop()
            break
    
    msg = "Success"
    
    return msg

