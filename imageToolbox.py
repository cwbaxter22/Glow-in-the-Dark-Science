import os
from PIL import Image
import matplotlib.image as mpimg
import numpy as np

def imgAverage(imgLocation):
    #https://stackoverflow.com/questions/17291455/how-to-get-an-average-picture-from-100-pictures-using-pil
    #Grab all files within the folder location (imgLocation)
    allfiles=os.listdir(imgLocation)
    imlist=[filename for filename in allfiles if  filename[-4:] in [".jpg",".JPG"]]

    #All pictures are the same size, so grab the dimenions of the first image
    w,h=Image.open(os.path.join(imgLocation, imlist[0])).size
    N=len(imlist)

    #Initialize an array to hold the average, 3rd index of zeros is 1 because these are CCD
    arr=np.zeros((h,w),float)

    #Add each image to an array and average them
    for im in imlist:
        imarr = np.array(Image.open(os.path.join(imgLocation, im)),dtype=float)
        arr=arr+imarr/N

    #Round the value of each float and cast it to 8-bit integer
    arr=np.array(np.round(arr),dtype=np.uint8)
    return arr

def createCorrectionImages(dirname):
    # Function that generates the ambient, flat-field, and dark-noise images for the image correction
    # Designed to be only run once to save computational space
    #Image Correction Files
    ambientFolder = os.path.join(dirname, 'Corrections\Ambient')
    ffcFolder = os.path.join(dirname, 'Corrections\FlatField')
    darkFolder = os.path.join(dirname, 'Corrections\DarkNoise')

    #Create the average corrected images
    ambImg = imgAverage(ambientFolder)
    ffImg = imgAverage(ffcFolder)
    darkImg = imgAverage(darkFolder)
    return ambImg, ffImg, darkImg

def flatFieldCorrection(raw, flat, dark):
    FmD = flat - dark
    m = np.average(FmD)
    return ((raw - dark)*(m/FmD))