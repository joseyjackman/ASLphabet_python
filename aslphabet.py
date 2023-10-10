import cv2
import numpy as np
import os
from future.moves import tkinter
from matplotlib import pyplot as plt
import mediapipe as mp
from PIL import Image
from pytesseract import pytesseract
import platform
from tkinter import Tk, Label, Button

# Identify platform and assign to variable
platform_id = str(platform.system())
print(platform_id)

# Create a MediaPipe holistic model
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Initialize the holistic model
holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Tkinter setup - starter screen
root = Tk()
root.title("ASLphabet")
root.geometry("350x500")

def menu():
    myLabel = Label(root, text="   Welcome to ASLphabet!   \n   ------------   ").place(relx = 0.5,  anchor = tkinter.N)
    myLabel1 = Label(root, text="Press Q to quit out of the camera.").place(relx = 0.5, rely = 0.4, anchor = tkinter.CENTER)
    myButton = Button(root, text="Launch Camera", command=camera).place(relx = 0.5, rely = 0.6, anchor = tkinter.CENTER)
    root.mainloop()

def mediapipe_detection(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Process the image using the holistic model
    results = holistic.process(image)

    image.flags.writeable = True

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    return image, results

def tesseract(imagepath, platform_id):
    # The following is the path to the tesseract executable 
    #currently set up for both linux and windows, selects appropriate path automatically.
    if platform_id == 'Linux':
        path_to_tesseract = r"/bin/tesseract"
    elif platform_id == 'Windows':
        path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        
    
    
    #imagepath = 'test1.jpg'

    # Set the Tesseract executable path
    pytesseract.tesseract_cmd = path_to_tesseract

    # Use Tesseract to extract text from the captured image
    text = pytesseract.image_to_string(Image.fromarray(imagepath))

    # Print the extracted text, excluding the last character
    print(text[:-1])

def camera():
    camera = cv2.VideoCapture(0)
    while camera.isOpened():
        ret, frame = camera.read()

        # Call the mediapipe_detection function with the frame
        image, results = mediapipe_detection(frame)
        tesseract(image, platform_id)

        cv2.imshow('OpenCV Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()
    menu()

menu()
#print(results.face_landmarks)
