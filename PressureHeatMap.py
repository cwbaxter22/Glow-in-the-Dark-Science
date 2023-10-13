import os
from imageToolbox import createCorrectionImages
from imageToolbox import imgAverage
from imageToolbox import flatFieldCorrection

dirname = os.path.dirname(__file__) #Directs to ~/Glow-in-the-Dark-Science/
# os.path.join combines the cwd with the 'CurrentSpeed' folder
# next(os.walk())[1] grabs all of the directories within 'CurrentSpeed'
# https://stackoverflow.com/questions/10989005/do-i-understand-os-walk-right
speedFolders = next(os.walk(os.path.join(dirname, 'CurrentSpeed')))[1] 

ambImg, ffImg, darkImg = createCorrectionImages(dirname)

for speed in speedFolders:
    # Take the average of each photo
    currentSpeedPhotoAvg = imgAverage(os.path.join(dirname, 'CurrentSpeed', speed))
    correctedSpeedPhoto = flatFieldCorrection(currentSpeedPhotoAvg, ffImg, darkImg)

    #plt.imshow(currentSpeedPhotoAvg)
    #plt.show()


