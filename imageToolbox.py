import os
from PIL import Image
import matplotlib.image as mpimg
import numpy as np
import cv2

def cropPhotos(photosLocation, yMinC, yMaxC, xMinC, xMaxC):
    #Create a folder to store the cropped photos
    os.makedirs(photosLocation + '/Cropped')
    cropAddress = os.path.join(photosLocation, 'Cropped')

    #https://stackoverflow.com/questions/17291455/how-to-get-an-average-picture-from-100-pictures-using-pil
    #Grab all files within the folder location (imgLocation)
    allfiles=os.listdir(photosLocation)
    imlist=[filename for filename in allfiles if  filename[-4:] in [".jpg",".JPG"]]

    for im in imlist:
        originalIm = mpimg.imread(os.path.join(photosLocation, im))
        croppedIm = originalIm[yMinC:yMaxC, xMinC:xMaxC]
        #cv2.imwrite(os.path.join(photosLocation, '\Cropped', im), croppedIm)
        cv2.imwrite(os.path.join(cropAddress, im), croppedIm)

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
    ambientFolder = os.path.join(dirname, 'Corrections\Ambient\Cropped')
    ffcFolder = os.path.join(dirname, 'Corrections\FlatField\Cropped')
    darkFolder = os.path.join(dirname, 'Corrections\DarkNoise\Cropped')

    #Create the average corrected images
    ambImg = imgAverage(ambientFolder)
    ffImg = imgAverage(ffcFolder)
    darkImg = imgAverage(darkFolder)
    return ambImg, ffImg, darkImg

def flatFieldCorrection(raw, flat, dark):
    FmD = flat - dark
    m = np.average(FmD)
    return ((raw - dark)*(m/FmD))

def outlineImageHeatmap(img, imgToCombineWith):
    # https://stackoverflow.com/questions/46020894/superimpose-heatmap-on-a-base-image-opencv-python
    # Current function will return an outline of a sample as long as the background is dark
    th = cv2.threshold(img,140,255,cv2.THRESH_BINARY)[1]
    blur = cv2.GaussianBlur(th,(13,13), 11)
    heatmap_img = cv2.applyColorMap(blur, cv2.COLORMAP_JET)
    hm1d = heatmap_img[:, :, 1]
    hm1dMatchType = hm1d.astype(imgToCombineWith.dtype)
    #Below for superimposing images (if needed)
    #super_imposed_img = cv2.addWeighted(hm1dMatchType, 0.9, pressureDistribution, 0.5, 0)

    return hm1dMatchType