from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

import numpy as np

from PIL import Image

import tensorflow as tf # TF2 required


class imageClassifier(object):
    def __init__(self,input_mean = 127.5,input_std = 127.5):
        self.input_mean = input_mean
        self.input_std = input_std
        self.model_file = '/Users/mmalherbe/Desktop/fridgepy/imageclassifier/'+'fridgev2.tflite'
        self.label_file = '/Users/mmalherbe/Desktop/fridgepy/imageclassifier/'+'class_labels.txt'
        self.interpreter = tf.lite.Interpreter(model_path=self.model_file)
        self.interpreter.allocate_tensors()
        self.resultProbs = dict()
        self.treshold = 0.5


    def load_labels(self,filename):
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines()]

    def checkForKnownLabel(self,frame):
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        # check the type of the input tensor
        floating_model = input_details[0]['dtype'] == np.float32

  # NxHxWxC, H:1, W:2
        height = input_details[0]['shape'][1]
        width = input_details[0]['shape'][2]
        img = Image.fromarray(frame).resize((width, height))

  # add N dim
        input_data = np.expand_dims(img, axis=0)

        if floating_model:
            input_data = (np.float32(input_data) - self.input_mean) / self.input_std

        self.interpreter.set_tensor(input_details[0]['index'], input_data)

        self.interpreter.invoke()

        output_data = self.interpreter.get_tensor(output_details[0]['index'])
        results = np.squeeze(output_data)

        top_k = results.argsort()[-5:][::-1]
        labels = self.load_labels(self.label_file)
        
        self.resultProbs.clear()
        for i in top_k:
            #if floating_model:
                #print('{:08.6f}: {}'.format(float(results[i]), labels[i]))
            #else:
                #print('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))
            if(float(results[i]) > self.treshold):
                self.resultProbs[labels[i]] = results[i]
        return self.resultProbs