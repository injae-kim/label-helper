import cv2 # Opencv ver 3.1.0 used
import numpy as np
import os
import json

import sys
sys.setrecursionlimit(10 ** 9)

import selectinwindow as selectinwindow

originImageDirectory = os.getcwd() + '/data/origin/'
labelJsonDirectory = os.getcwd() + '/data/label/json/'
originImageNames = os.listdir(originImageDirectory)
labelJsonNames = os.listdir(labelJsonDirectory)

for jsonName in labelJsonNames:
    imageName = jsonName[6:-5] + '.jpg'

    assert(imageName in originImageNames)

    image = cv2.imread(originImageDirectory + imageName)

    with open(labelJsonDirectory + jsonName) as json_file:
        json_data = json.load(json_file)

        for data in json_data.values():
            cv2.rectangle(image, (data["x"], data["y"]),
                (data["x"] + data["w"],
                data["y"] + data["h"]), (0, 255, 0), 2)

        cv2.imshow("label", image)
        print('reconstruct..', imageName)

        while True:
            key = cv2.waitKey(1)

            if (key == 27):
                break
        