import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def intensity2PressureFunction():
    dirname = os.path.dirname(__file__) #Directs to ~/Glow-in-the-Dark-Science/
    # os.path.join combines the cwd with the 'PDCalibrationCurve' folder
    # next(os.walk())[1] grabs all of the files within 'PDCalibrationCurve'
    # the [0] is grabbing the first file (which is the .csv)
    # There should only be 1 .csv file in that location
    # https://stackoverflow.com/questions/10989005/do-i-understand-os-walk-right
    pviSpreadsheetName = next(os.walk(os.path.join(dirname, 'PDCalibrationCurve')))[2][0]
    pviSpreadsheetPath = os.path.join(dirname, 'PDCalibrationCurve', pviSpreadsheetName)
    pviDF = pd.read_csv(pviSpreadsheetPath)
    pressureTorr = np.array(pviDF["Pressure"].tolist())
    pressurePascal = pressureTorr*133.3 #Convert to Pascals
    ratio = np.array(pviDF["ratio"].tolist())

    # polyfit credit: https://stackoverflow.com/questions/19165259/python-numpy-scipy-curve-fitting
    # calculate polynomial
    # Fourth order fit seems to accomodate data well
    # Function being calculated is pressure as a function of I/I0 where I0 is the lowest intensity
    z = np.polyfit(ratio, pressurePascal, 5) 
    return np.poly1d(z)
    