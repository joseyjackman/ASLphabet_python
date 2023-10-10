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
root = Tk()
root.title("ASLphabet")
width =1017
height=616
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
align = '%dx%d+%d+%d' % (width, height, (screenheight - width)/2, (screenheight - height)/2)
root.geometry(align)
root.resizable(width=False, height=False)
root.iconbitmap('Logo.ico')

def menu():
    canvas = Canvas(root, bg="#e0f8f8", width=width, height=height)
    canvas.pack()
    myLabel = Label(canvas, bg="#e0f8f8", justify="center", font=('Modern', 40, "bold"), text=("Welcome ")+os.getlogin()+"!").place(x=40, y=40, width = 330, height = 68)
    myImage = PhotoImage(file="LogoNoBackground.png").subsample(1)
    canvas2 = Canvas(canvas, bg="#e0f8f8", width=508, height=616)
    canvas2.place(x=507, y=0)
    canvas2.create_image(250, 308, anchor="center" ,image=myImage)
    myLabel1 = Label(canvas, bg="#e0f8f8", justify="center", font=('Modern', 15), text="Press Q to quit out of the camera.").place(x=40, y=100, width = 330, height = 68)
    myLabel1 = Label(canvas, bg="#e0f8f8", justify="center", font=('Modern', 15), text="Brought to you by: ").place(x=40, y=500, width=330, height=68)
    myButton1 = Button(canvas, bg="#80CC23", font=('Modern', 18, "bold"), justify="center", text="Launch Camera", command=camera).place(x=20, y=190, width = 378, height = 68)
    myButton2 = Button(canvas, bg="#80CC23", font=('Modern', 18, "bold"), justify="center", text="Instruction", command="").place(x=20, y=270, width=378, height=68)
    myButton3 = Button(canvas, bg="#80CC23", font=('Modern', 18, "bold"), justify="center", text="ASL Dictionary", command="").place(x=20, y=350, width=378, height=68)
    myButton4 = Button(canvas, bg="#80CC23", font=('Modern', 18, "bold"), justify="center", text="Settings", command="").place(x=20, y=430, width=378, height=68)
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

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()
    menu()

menu()
