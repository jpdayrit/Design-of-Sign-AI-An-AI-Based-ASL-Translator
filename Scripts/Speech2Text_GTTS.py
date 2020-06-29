# -*- coding: utf-8 -*-
"""
Performs speech-to-text (STT) conversion through Google Voice.

"""

import speech_recognition as STT
 
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
 
    


