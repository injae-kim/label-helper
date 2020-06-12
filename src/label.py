import cv2 # Opencv ver 3.1.0 used
import numpy as np
import os
import json

import sys
sys.setrecursionlimit(10 ** 9)

import selectinwindow as selectinwindow

wNames = ["left-eye", "right-eye", "left-ear", "right-ear", "nose", "mouth", "face"]


# offset_x, y s relative distance to Image's Center Point
eye = {
    "width": 50,
    "height": 25,
    "offset_x": 60,
    "offset_y": -20,
}
ear = {
    "width": 15,
    "height": 40,
    "offset_x": 100,
    "offset_y": 30,
}
nose = {
    "width": 50,
    "height": 80,
    "offset_x": 0,
    "offset_y": 10,
}
mouth = {
    "width": 70,
    "height": 40,
    "offset_x": 0,
    "offset_y": 90,
}
face = {
    "width": 230,
    "height": 320,
    "offset_x": 0,
    "offset_y": 0,
}

dataDirectory = os.getcwd() + '/data/origin/'
dataFileNames = os.listdir(dataDirectory)
dataFileNames.sort()

labelImageDirectory = os.getcwd() + '/data/label/image/'
labelJsonDirectory = os.getcwd() + '/data/label/json/'
labelFileNames = os.listdir(labelImageDirectory)

for dataFileName in dataFileNames:

    # If label Image Exist, PASS
    labelFileName = 'label_' + dataFileName

    if labelFileName in labelFileNames:
        continue

    image = cv2.imread(dataDirectory + dataFileName)
    imageWidth = image.shape[1]
    imageHeight = image.shape[0]

    centerX = int(imageWidth / 2)
    centerY = int(imageHeight / 2)

    _left_eye = [centerX - eye["offset_x"] - int(eye["width"] / 2), centerY + eye["offset_y"] - int(eye["height"] / 2), eye["width"], eye["height"]]
    _right_eye = [centerX + eye["offset_x"] - int(eye["width"] / 2), centerY + eye["offset_y"] - int(eye["height"] / 2), eye["width"], eye["height"]]
    _left_ear = [centerX - ear["offset_x"] - int(ear["width"] / 2), centerY + ear["offset_y"] - int(ear["height"] / 2), ear["width"], ear["height"]]
    _right_ear = [centerX + ear["offset_x"] - int(ear["width"] / 2), centerY + ear["offset_y"] - int(ear["height"] / 2), ear["width"], ear["height"]]
    _nose = [centerX + nose["offset_x"] - int(nose["width"] / 2), centerY + nose["offset_y"] - int(nose["height"] / 2), nose["width"], nose["height"]]
    _mouth = [centerX + mouth["offset_x"] - int(mouth["width"] / 2), centerY + mouth["offset_y"] - int(mouth["height"] / 2), mouth["width"], mouth["height"]]
    _face = [centerX + face["offset_x"] - int(face["width"] / 2), centerY + face["offset_y"] - int(face["height"] / 2), face["width"], face["height"]]

    # left-eye, right-eye, ,left-ear, right-ear, nose, mouth, face
    # initXYWHx = [(100, 55, 30, 30), (170, 55, 30, 30), 
    #             (70, 55, 10, 30), (230, 55, 10, 30), 
    #             (140, 110, 30, 30), (115, 165, 70, 20), (60, 20, 200, 200)]
    initXYWHx = [_left_eye, _right_eye, _left_ear, _right_ear, _nose, _mouth, _face] 

    rects = [selectinwindow.dragRect() for _ in range(len(wNames))]
    selectinwindows = [selectinwindow.utils() for _ in range(len(wNames))]

    for i in range(len(wNames)):
        cv2.namedWindow(wNames[i])
        selectinwindows[i].init(rects[i], image, wNames[i], imageWidth, imageHeight, initXYWHx[i])
        
        cv2.setMouseCallback(rects[i].wname, selectinwindows[i].dragrect, rects[i])

    for i in range(len(wNames)):
        selectinwindows[i].initDraw(rects[i], image, wNames[i], imageWidth, imageHeight, initXYWHx[i])

    cv2.namedWindow("result")
    cv2.setMouseCallback("result", selectinwindow.utils().resultCallBack, rects)


    enter = 13
    esc = 27

    print('ESC: PASS to Next Image, ENTER: SEE Label Image\n')

    while True:
        key = cv2.waitKey(1)

        if key == esc:
            print('PASS!')
            break

        elif key == enter:
            
            cv2.destroyAllWindows()

            for rect in selectinwindow.coords.values():
                cv2.rectangle(image, (rect.outRect.x, rect.outRect.y),
                    (rect.outRect.x + rect.outRect.w,
                    rect.outRect.y + rect.outRect.h), (0, 0, 255), 1)
            
            cv2.imshow('result', image)

            print('ESC: PASS and DO NOT SAVE, ENTER: SAVE this Label Image\n')

            while True:                
                key = cv2.waitKey(1)

                if key == esc:
                    print('PASS!\n')
                    break
                    
                elif key == enter:
                    # SAVE json file
                    jsonFileName = labelJsonDirectory + labelFileName[:-4] + '.json'
                    label_data = {}

                    for name in wNames:
                        label_data[name] = selectinwindow.coords[name].outRect.__dict__

                    # for rect in selectinwindow.coords.keys():
                    #     label_data[rect] = selectinwindow.coords[rect].outRect.__dict__
                                
                    with open(jsonFileName,  'w', encoding="utf-8") as make_file:
                        json.dump(label_data, make_file, ensure_ascii=False, indent="\t")

                    cv2.imwrite(labelImageDirectory + labelFileName, image)

                    print(jsonFileName,'SAVED!')
                    
                    break

            break

    cv2.destroyAllWindows()

print('FINISHED!')