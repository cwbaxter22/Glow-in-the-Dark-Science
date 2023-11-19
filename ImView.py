import tkinter as tk
from tkinter import *
from tkinter import filedialog
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import plotly.express as px

def clicked():
    '''Simple python function to preview image intensities on older PC that does not have python installed.'''
    file_path = filedialog.askopenfilename()
    lbl.configure(text = file_path)
    img = mpimg.imread(file_path)
    plt.imshow(img)
    plt.show()
 
# create root window
root = tk.Tk()

btn = Button(root, text = "Browse" ,
             fg = "blue", command=clicked)
# set Button grid
btn.pack()

lbl = Label(root, text = "Choose Image")
lbl.pack()
 
# root window title and dimension
root.title("Image Intensity Preview")

# Set geometry (widthxheight)
root.geometry('350x200')
 
#Keep the window
root.mainloop()



