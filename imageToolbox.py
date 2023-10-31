import os
from PIL import Image
import matplotlib.image as mpimg
import numpy as np
import cv2

def cropPhotos(photos_location, y_min, y_max, x_min, x_max):
    """Crops all photos in a directory based on the (x,y) coordinates of the crop area.
    Creates a folder within the directory titled '/Cropped' containing the cropped images 

    Parameters
    ----------
    photos_location : str
        Directory that contains the folders with the images
    y_min : int
        The minimum y location of the crop area (bottom left y-coordinate)
    y_max : int
        The maximum y location of the crop area (top right y-coordinate)
    x_min : int
        The minimum x location of the crop area (bottom left x-coordinate)
    x_max : int
        The maximum x location of the crop area (top right x-coordinate)
    

    Returns
    -------
    None
    """
    
    #Create a folder to store the cropped photos
    os.makedirs(photos_location + '/Cropped')
    cropAddress = os.path.join(photos_location, 'Cropped')

    #https://stackoverflow.com/questions/17291455/how-to-get-an-average-picture-from-100-pictures-using-pil
    #Grab all files within the folder location (imgLocation)
    allfiles=os.listdir(photos_location)
    imlist=[filename for filename in allfiles if  filename[-4:] in [".jpg",".JPG"]]

    for im in imlist:
        originalIm = mpimg.imread(os.path.join(photos_location, im))
        croppedIm = originalIm[y_min:y_max, x_min:x_max]
        #cv2.imwrite(os.path.join(photosLocation, '\Cropped', im), croppedIm)
        cv2.imwrite(os.path.join(cropAddress, im), croppedIm)

def imgAverage(images_location):
    """Performs element-wise averaging of the images within the input directory.  

    Parameters
    ----------
    images_location : str
        Directory that contains the folders with the images
    

    Returns
    -------
        None
    """
    #https://stackoverflow.com/questions/17291455/how-to-get-an-average-picture-from-100-pictures-using-pil
    #Grab all files within the folder location (imgLocation)
    allfiles = os.listdir(images_location)
    imlist=[filename for filename in allfiles if  filename[-4:] in [".jpg",".JPG"]]

    #All pictures are the same size, so grab the dimenions of the first image
    w,h=Image.open(os.path.join(images_location, imlist[0])).size
    N=len(imlist)

    #Initialize an array to hold the average, 3rd index of zeros is 1 because these are CCD
    arr=np.zeros((h,w),float)

    #Add each image to an array and average them
    for im in imlist:
        imarr = np.array(Image.open(os.path.join(images_location, im)),dtype=float)
        arr=arr+imarr/N

    #Round the value of each float and cast it to 8-bit integer
    arr=np.array(np.round(arr),dtype=np.uint8)
    return arr

def createCorrectionImages(folders_location):
    """Applies the imgAverage() function to the 3 folders of images required to perform the flat
    field image correction.

    ## Prerequisites
    1. Create a folder 'Corrections\' within the directory
    2. Include folders named 'Ambient' 'FlatField' and 'DarkNoise' for each of the 3 types
    and include the photos within them.

    Parameters
    ----------
    folders_location : str
        Directory that contains the folders with the images
        

    Returns
    -------
    ambient_image : image
        averaged ambient image
    flat_field_image : image
        averaged flat field image
    dark_noise_image : image
        averaged dark noise image
    """
    
    # Function that generates the ambient, flat-field, and dark-noise images for the image correction
    # Designed to be only run once to save computational space
    #Image Correction Files
    ambientFolder = os.path.join(folders_location, 'Corrections\Ambient\Cropped')
    ffcFolder = os.path.join(folders_location, 'Corrections\FlatField\Cropped')
    darkFolder = os.path.join(folders_location, 'Corrections\DarkNoise\Cropped')

    #Create the average corrected images
    ambient_image = imgAverage(ambientFolder)
    flat_field_image = imgAverage(ffcFolder)
    dark_noise_image = imgAverage(darkFolder)
    return ambient_image, flat_field_image, dark_noise_image

def flatFieldCorrection(raw, flat, dark):
    """Applies a flat-field correction to the each image within the directory

    ## Prerequisite:
    Function createCorrectionImages() must have run first to create the correction images

    Parameters
    ----------
    raw : image
        image of sample (averaged)
    flat : image
        flat field image (uniformly illuminated white paper, averaged)
    dark : image
        image taken with the lens cap on (dark-noise, averaged)

        

    Returns
    -------
    corrected_image : image
        single image with flat-field correction applied
    """

    FmD = flat - dark
    m = np.average(FmD)
    corrected_image = ((raw - dark)*(m/FmD))
    return corrected_image

def outlineImageHeatmap(img, imgToCombineWith):
    """Identifies focal image, blurs, and applies an outline. 
    This outline is then superimposed over another image.

    Parameters
    ----------
    img : image
        image to take outline of
    imgToCombineWith : image
        image to superimpose outline over        

    Returns
    -------
    hm1dMatchType : image
        imgToCombineWith with outline of img superimposed
    """
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