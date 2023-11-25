import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy.ndimage import uniform_filter1d

"""Module that generates SV plot based on spectra data in .txt files

Input: folder of txt files
Output: csv containing slope info"""

FOLDER_DIR = (r"C:\Users\Colin\Downloads\20231117POfilmAu@RF_80ulR_100ulspray300ul-20231125T013433Z-001\20231117POfilmAu@RF_80ulR_100ulspray300ul")
#User Input:
LOWER_B = 645 #650 625
UPPER_B = 670 #750 700
trapSpacing = 0.215 #width of rectangles for trapezoidal rule integral calculation

_, _, files = next(os.walk(FOLDER_DIR))

pressures_torr = np.zeros(len(files))
for pos, file in enumerate(files): #Cycle through folders
    file_number_str = str(file.replace('.txt', '', 1))
    pressure_float = float(file_number_str.replace('_', '.', 1))
    pressures_torr[pos] = pressure_float*133.3

areas_under_curve = np.zeros(len(files))

for pos, file in enumerate(files):
    df = pd.read_csv(FOLDER_DIR + "\\" + file, header = None, sep='\t', skiprows=17)
    df.drop(df.tail(1).index,inplace=True) # drop final row
    df = df.apply(pd.to_numeric)
    df.columns = ['wavelength', 'intensity']
    unfilteredInt = df.loc[(df['wavelength'] > LOWER_B) & (df['wavelength'] < UPPER_B), 'intensity' ]
    filteredInt = uniform_filter1d(unfilteredInt, size=5)
    ## The trapezoidal rule approximates an integral under a curve. trapz(y, dx)
    # We provide the y-values and the spacing between them on the x-axis, dx
    # Since the spacing is always either 0.21 or 0.22, use 0.215 (moved to start of code)
    area = np.trapz(filteredInt, dx= trapSpacing)
    areas_under_curve[pos] = area

#firstSlope, _, _, _, firstPStdError = linregress(X[index], Y[index])

#https://stackoverflow.com/questions/9764298/given-parallel-lists-how-can-i-sort-one-while-permuting-rearranging-the-other
pressures_torr, areas_under_curve = zip(*sorted(zip(pressures_torr, areas_under_curve)))

plt.figure()
plt.scatter(pressures_torr, areas_under_curve)
plt.xlabel("Pressure (Torr)")
plt.ylabel("Intensity")
plt.title('Intensity of light from spectrum of ' + str(LOWER_B) + 'nm to ' + str(UPPER_B) + 'nm')
plt.show()

ratios = pressures_torr/pressures_torr[0]

pressures_ratio_df = pd.DataFrame()
pressures_ratio_df["Pressure"] = pressures_torr
pressures_ratio_df["Ratio"] = ratios
#pressures_ratio_df.to_csv(r'C:\Users\Colin\OneDrive - UW\Research\SciTechData\FlatPlate\SGfile3.csv')
#z = np.polyfit(ratios, pressures_torr, 5) 

