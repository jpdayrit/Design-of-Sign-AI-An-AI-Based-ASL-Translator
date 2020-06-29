# -*- coding: utf-8 -*-
"""
Performs text-to-speech conversion through Google TTS API.

"""

from gtts import gTTS
from playsound import playsound
import os
import numpy as np

def getTTSoutput():
    
    gesture = str(np.genfromtxt("output_gesture.txt", dtype="str"))
    
    sound_file = "output_TTS.mp3"
    
    # passes text to Google Voice. 
    tts = gTTS(text=gesture, lang="en")
    
    # saves text as .mp3. 
    tts.save(sound_file)
    
    # play .wav file via playsound.
    playsound(sound_file)
    
    # deletes sound file after use.
    os.remove(sound_file)

getTTSoutput()