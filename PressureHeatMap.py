import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import plotly.express as px
from imageToolbox import createCorrectionImages
from imageToolbox import imgAverage
from imageToolbox import flatFieldCorrection
from imageToolbox import cropPhotos
from photoDiodeToolbox import intensity2PressureFunction

dirname = os.path.dirname(__file__) #Directs to ~/Glow-in-the-Dark-Science/

# os.path.join combines the cwd with the 'CurrentSpeed' folder
# next(os.walk())[1] grabs all of the directories within 'CurrentSpeed'
# https://stackoverflow.com/questions/10989005/do-i-understand-os-walk-right
speedFolders = next(os.walk(os.path.join(dirname, 'CurrentSpeed')))[1]

#First, take care of cropping the photos based on the coordinates of the upper right
#and lower left hand corners of the photo
yMinC = 362
yMaxC = 400
xMinC = 617
xMaxC = 711

uncroppedList = ['Corrections\Ambient', 'Corrections\FlatField', 'Corrections\DarkNoise']
for speed in speedFolders:
    uncroppedList.append('CurrentSpeed/' + speed)
for loc in uncroppedList:
    folderToCrop = os.path.join(dirname, loc)
    cropPhotos(folderToCrop, yMinC, yMaxC, xMinC, xMaxC)

ambImg, ffImg, darkImg = createCorrectionImages(dirname)

for speed in speedFolders:
    # Take the average of each photo
    currentSpeedPhotoAvg = imgAverage(os.path.join(dirname, 'CurrentSpeed', speed, 'Cropped'))
    correctedSpeedPhoto = flatFieldCorrection(currentSpeedPhotoAvg, ffImg, darkImg)

    fig = plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(currentSpeedPhotoAvg)
    plt.subplot(1, 2, 2)
    plt.imshow(correctedSpeedPhoto)
    plt.show()
    
    int2pressFunc = intensity2PressureFunction()
    pressureDistributionCorrected = np.vectorize(int2pressFunc)(correctedSpeedPhoto)
    pressureDistributionUncorrected = np.vectorize(int2pressFunc)(currentSpeedPhotoAvg)

    fig = px.imshow(pressureDistributionCorrected)
    fig.show()



