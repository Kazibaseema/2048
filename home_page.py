# Import the required libraries
from tkinter import filedialog
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
from PIL import Image, ImageTk
from stegano import lsb
from tkinter import ttk

# Create an instance of tkinter frame or window
ws=Tk()

# Set the size of the tkinter window
ws.geometry("700x500+150+180")
#ws.resizable(False,False)
ws.title("Disclaimer")



#___________________icon__________________


image_icon=PhotoImage(file="logo.png")
ws.iconphoto(False,image_icon)


# Load the image
image=Image.open('homepage.jpg')

# Resize the image in the given (width, height)  #h=350 #fixing imag to screen
img=Image.resize((690, 495))

# Conver the image in TkImage
my_img=ImageTk.PhotoImage(img)

# Display the image with label
label=Label(ws, image=my_img)
label.pack()


# Define the function to show the message box
def display_message():
    messagebox.showwarning("Disclaimer !", "WE DOES NOT Promote or encourage ANY Illegal Activities,all content provied by us is meant for EDUCATIONAL PURPOSE only.")

# Create the button and add it to the main window
button = tk.Button(ws, text="DISCLAIMER",bg="red",fg="white",bd="10",font="arial 15 bold",relief=RAISED, command=display_message).place(x=183,y=400)
#button.pack()



def nextPage():
    ws.destroy()
    import page2

def prevPage():
    ws.destroy()
    import page3
    







Button(
    ws, 
    text="CLICK HERE",bg="green",fg="white",bd="10",font="arial 15 bold",relief=RAISED,command=nextPage).place(x=380,y=400)
   

ws.mainloop()
