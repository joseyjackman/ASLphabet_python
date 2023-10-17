import tkinter

import cv2
import os
import mediapipe as mp
from pytesseract import pytesseract
import platform
from tkinter import Tk, Label, Button, Canvas, PhotoImage
from PIL import Image

# Identify platform and assign to variable
platform_id = str(platform.system())
print(platform_id)

# Create a MediaPipe holistic model
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Initialize the holistic model
holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Tkinter setup - starter screen
globalquit = "q"
root = Tk()
root.title("ASLphabet")
width =1017
height=616
width2 =700
height2=600
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
align = '%dx%d+%d+%d' % (width, height, (screenheight - width)/2, (screenheight - height)/2)
align2 = '%dx%d+%d+%d' % (width2, height2, (screenheight - width2)/2, (screenheight - height2)/2)
root.geometry(align)
root.resizable(width=False, height=False)
root.iconbitmap('Logo.ico')

def menu():
    canvas = Canvas(root, bg="#e0f8f8", width=width, height=height)
    canvas.pack()
    myLabel = Label(canvas, bg="#e0f8f8", justify="center", font=('Modern', 30, "bold"), text=("Welcome ")+os.getlogin()+"!").place(x=70, y=40, width = 330, height = 68)
    myImage = PhotoImage(file="LogoNoBackground.png").subsample(1)
    canvas2 = Canvas(canvas, bg="#f0f8ff", width=508, height=620)
    canvas2.place(x=506, y=0)
    canvas2.create_image(250, 308, anchor="center" ,image=myImage)
    myLabel1 = Label(canvas, bg="#e0f8f8", fg="#0071bc", justify="center", font=('Modern', 15), text="Press Q to quit out of the camera.").place(x=70, y=100, width = 330, height = 68)
    myLabel1 = Label(canvas, bg="#e0f8f8", justify="center", font=('Modern', 15), text="Brought to you by: ").place(x=70, y=500, width=330, height=68)
    myButton1 = Button(canvas, bg="#80CC23", font=('Modern', 18, "bold"), justify="center", text="Launch Camera", command=camera).place(x=50, y=270, width=378, height=68)
    myButton2 = Button(canvas, bg="#80CC23", font=('Modern', 18, "bold"), justify="center", text="Instruction", command=instructions).place(x=50, y=190, width = 378, height = 68)
    myButton3 = Button(canvas, bg="#80CC23", font=('Modern', 18, "bold"), justify="center", text="Text-to-Image", command=texttoimage).place(x=50, y=350, width=378, height=68)
    myButton4 = Button(canvas, bg="#80CC23", font=('Modern', 18, "bold"), justify="center", text="Settings", command=settings).place(x=50, y=430, width=378, height=68)
    root.mainloop()

def closeAndopenSettings(self):
    self.destroy()
    settings()

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

    # Set the Tesseract executable path
    pytesseract.tesseract_cmd = path_to_tesseract

    # Use Tesseract to extract text from the captured image
    text = pytesseract.image_to_string(Image.fromarray(imagepath))

    # Print the extracted text, excluding the last character
    print(text[:-1])

def camera():
    width = 1280
    height = 720
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    camera.set(cv2.CAP_PROP_FPS, 30)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*'MJPG'))

    while camera.isOpened():
        ret, frame = camera.read()

        # Call the mediapipe_detection function with the frame
        image, results = mediapipe_detection(frame)
        tesseract(image, platform_id)

        cv2.imshow('OpenCV Feed', image)

        if cv2.waitKey(10) & 0xFF == ord(globalquit):
            break
    camera.release()
    cv2.destroyAllWindows()
    menu()

def settings():
    child = tkinter.Toplevel(root)
    child.geometry(align2)
    child.resizable(width=False, height=False)
    child.iconbitmap('Logo.ico')

    canvas = Canvas(child, bg="#f0f8ff", width=width2, height=height2)
    canvas.pack()
    canvas2 = Canvas(canvas, bg="#e0f8f8", width=625, height=height2)
    canvas2.place(x=35, y=0)
    myLabel = Label(canvas2, bg="#e0f8f8", justify="center", font=('Modern', 30, "bold"), text=("Settings")).place(x=160, y=2, width=320, height=100)

def texttoimage():
    child = tkinter.Toplevel(root)
    child.geometry(align2)
    child.resizable(width=False, height=False)
    child.iconbitmap('Logo.ico')

    canvas = Canvas(child, bg="#f0f8ff", width=width2, height=height2)
    canvas.pack()
    canvas2 = Canvas(canvas, bg="#e0f8f8", width=625, height=height2)
    canvas2.place(x=35, y=0)

    myLabel = Label(canvas2, bg="#e0f8f8", justify="center", font=('Modern', 30, "bold"), text=("Text-to-Image")).place(x=160, y=2, width=320, height=100)
def instructions():
    child = tkinter.Toplevel(root)
    child.geometry(align2)
    child.resizable(width=False, height=False)
    child.iconbitmap('Logo.ico')

    canvas = Canvas(child, bg="#f0f8ff", width=width2, height=height2)
    canvas.pack()
    canvas2 = Canvas(canvas, bg="#e0f8f8", width=625, height=height2)
    canvas2.place(x=35, y=0)

    myLabel = Label(canvas2, bg="#e0f8f8", justify="center", font=('Modern', 30, "bold"),text=("Instructions")).place(x=160, y=2, width=320, height=100)
    myLabel1 = Label(canvas2, bg="#e0f8f8", fg="#0071bc", justify="left", font=('Modern', 20),text="Step 1: ").place(x=25, y=120)
    myLabel2 = Label(canvas2, bg="#e0f8f8", justify="left", font=('Modern', 15), text="  Use text-to-image in order to find the desired ASL sign.\n  Take note of the finger placements!").place(x=100, y=123)
    myLabel3 = Label(canvas2, bg="#e0f8f8", fg="#0071bc", justify="left", font=('Modern', 20), text="Step 2: ").place(x=25, y=210)
    myLabel4 = Label(canvas2, bg="#e0f8f8", justify="left", font=('Modern', 15),text="  Launch the camera. Present your ASL sign to the camera and \n  take a clear picture. Use the best lighting available to you!").place(x=100, y=213)
    myLabel5 = Label(canvas2, bg="#e0f8f8", fg="#0071bc", justify="left", font=('Modern', 20), text="Step 3: ").place(x=25, y=300)
    myLabel6 = Label(canvas2, bg="#e0f8f8", justify="left", font=('Modern', 15), text="  Observe your results. If the sign was succesfully picked up by\n  the camera - then congratulations! If not, checkout the \n  additional resources provided and try again.").place(x=100, y=303)
    myLabel7 = Label(canvas2, bg="#e0f8f8", fg="#0071bc", justify="left", font=('Modern', 20), text="Step 4: ").place(x=25, y=410)
    myLabel8 = Label(canvas2, bg="#e0f8f8", justify="left", font=('Modern', 15),text="  Most importantly - take it easy! Learning a new language is\n  a long process, so try taking it a few signs as a time until\n  you get the hang of it!").place(x=100, y=413)
menu()