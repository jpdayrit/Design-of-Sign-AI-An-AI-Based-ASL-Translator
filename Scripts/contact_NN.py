# -*- coding: utf-8 -*-
"""

Interface with neural network for gesture recognition. 

"""

import numpy as np
import os
from keras.models import load_model
from keras.models import Sequential

def contact_neuralNet():
    
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
    
    # retrieve labels. 
    directory = 'gesturedat'
    catalog = []
    for folders in os.listdir(directory):
        catalog.append(folders)
    
    # load model using appropriate weights. 
    loaded_model = Sequential()
    loaded_model = load_model('finalized_weights.hdf5')
    
    # interface with model. 
    raw_prediction = loaded_model.predict_classes(input_data)
    
    output = catalog[raw_prediction[0]]
    
    np.savetxt("output_gesture.txt", [output], fmt="%s")
    
contact_neuralNet()
        