# Glow-in-the-Dark-Science
Code to process Pressure-Sensitive Paint (PSP) images taken of wind tunnel models using a CCD camera
**Note:** This repository will soon be replaced by a better version in the Glow-In-The-Dark repository.
This repo was created prior to taking a course in Software Engineering. The skills learned will be implemented there. 

# PressureHeatMap.py
This file creates a 'heat map' of the different pressures on the sample.
Put speeds to be evaluated in the 'CurrentSpeed' folder, inside folders named with the speed in mph
Put the correction images in respective bins (currently down for maintentenance)

# Image correction Feature
Software should be using algorithm to correct for various types of noise in the image.
However, this algorithm is interfering with results. Current working theory is that since the
majority of the image is dark, contrasted with the small bright area, the surplus of dark patches 
is drowning out the sample section.
