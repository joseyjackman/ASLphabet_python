import tkinter
import cv2
import os
import mediapipe as mp
import platform
import pygame
from pygame import mixer
from tkinter import Tk, Label, Button, Canvas, PhotoImage, Entry, constants, Text, ttk
import winsound
from PIL import Image, ImageTk
import time  # used to take a break between pictures
import uuid  # used to name image files
import sqlite3
IMAGES_PATH = 'Tensorflow/workspace/images/collectedimages'




import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math


def launch_camera():
    global cap
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=2)
    classifier = Classifier("ASLRecognitionRevived/Model/keras_model.h5", "ASLRecognitionRevived/Model/labels.txt")
    
    offset = 20
    imgSize = 300
    
    labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y"]
    
    while True:
        success, img = cap.read()
        if not success:
            continue  # Skip the iteration if the frame is not successfully captured
    
        imgOutput = img.copy()
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
    
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
    
            # Ensure cropping coordinates are within the image boundaries
            x1, y1 = max(x - offset, 0), max(y - offset, 0)
            x2, y2 = min(x + w + offset, img.shape[1]), min(y + h + offset, img.shape[0])
    
            imgCrop = img[y1:y2, x1:x2]
    
            # Check if the cropped image is empty
            if imgCrop.size == 0:
                continue
    
            aspectRatio = h / w
    
            try:
                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    if wCal > 0:
                        imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                        wGap = math.ceil((imgSize - wCal) / 2)
                        imgWhite[:, wGap:wGap + wCal] = imgResize
                        prediction, index = classifier.getPrediction(imgWhite, draw=False)
    
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    if hCal > 0:
                        imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                        hGap = math.ceil((imgSize - hCal) / 2)
                        imgWhite[hGap:hGap + hCal, :] = imgResize
                        prediction, index = classifier.getPrediction(imgWhite, draw=False)
    
                if prediction is not None and index < len(labels):
                    label = labels[index]
                    prob = round(prediction[index] * 100, 2)
                    print(f'Prediction: {label}, Probability: {prob}%')
                    cv2.putText(imgOutput, f'{label} {prob}%', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
                cv2.imshow("ImageCrop", imgCrop)
                cv2.imshow("Image", imgOutput)
    
            except Exception as e:
                print(f"An error occurred: {e}")
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    cv2.destroyAllWindows()


def HunterStuff(): #this to the end of function is hunter's code:
    IMAGES_PATH = 'Tensorflow/workspace/images/collectedimages'

    labels = ['hello', 'thanks', 'yes', 'no', 'iloveyou']
    number_imgs = 15  # number of images to collect for training + testing
    # Loop through all labels in the label array
    for label in labels:
        # Create a directory for each one of the labels
        os.mkdir(os.path.join(IMAGES_PATH, label))

        # Start video capture using opencv and computer camera
        cap = cv2.VideoCapture(
            0)  # If the video capture does not work, play around with the number (e.g., MACs may use 2)

        print('Collecting images for {}'.format(label))

        # Wait for 5 seconds to get in position to collect images
        time.sleep(5)

        # Loop through the number of images wanted to collect
        for imgnum in range(number_imgs):
            ret, frame = cap.read()

            # Format the image names
            image_name = os.path.join(IMAGES_PATH, label, f"{label}.{str(uuid.uuid1())}.jpg")
            cv2.imwrite(image_name, frame)

            # Show the image on the screen
            cv2.imshow('frame', frame)

            # Wait for 2 seconds
            time.sleep(2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release video capture
        cap.release()

# Identify platform and assign to variable
platform_id = str(platform.system())
print(platform_id)

# Create a MediaPipe holistic model
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Initialize the holistic model
holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Tkinter setup - starter screen
pygame.init()
mixer.init()
mixer.music.load("City-of-Tomorrow_v001_Looping.wav")
mixer.music.play(loops=-1)

instructionsopen = None
settingsopen = None
texttoimageopen = None
cameraopen = None
globalquit = "q"
root = Tk()
root.title("ASLphabet")
width = 1017
height = 616
width2 = 700
height2 = 600
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
align = '%dx%d+%d+%d' % (width, height, (screenheight - width)/2, (screenheight - height)/2)
align2 = '%dx%d+%d+%d' % (width2, height2, (screenheight - width2)/2, (screenheight - height2)/2)
root.geometry(align)
root.resizable(width=False, height=False)
root.iconphoto(True, PhotoImage(file='Logo.png'))
name = os.getlogin()
color1="#e0f8f8"
color2 ="#f0f8ff"
color3 = "#0071bc"
color4 = "#80CC23"
language = 'en'

def RBGAImage(path):
    return Image.open(path).convert("RGBA")

def rebootMenu(root):
    root.destroy()
    menu()

def menu():
    background = PhotoImage(file = "Pattern.png")
    logo = PhotoImage(file = "LogoNoBackground.png")
    canvas = Canvas(root, bg=color1, width=width, height=height)
    canvas.pack()
    myLabel = Label(canvas, bg=color1, justify="center", font=('Modern', 30, "bold"), text=("Welcome ")+name+"!").place(x=70, y=40, width = 330, height = 68)
    canvas2 = Canvas(canvas, bg=color2, width=508, height=620)
    Background = RBGAImage("Pattern.png")
    Logo = RBGAImage("LogoNoBackground.png")
    Background.paste(Logo, (0, 75), Logo)
    finalLogo = ImageTk.PhotoImage(Background)
    canvas2.place(x=506, y=0)
    label1 = Label(canvas2, image=finalLogo).place(x=0, y=0)
    myLabel1 = Label(canvas, bg=color1, fg=color3, justify="center", font=('Modern', 15), text=("Press ")+ globalquit + (" to quit out of the camera.")).place(x=70, y=100, width = 330, height = 68)
    myLabel1 = Label(canvas, bg=color1, justify="center", font=('Modern', 15), text="Brought to you by: Austin, Hunter, and Emily").place(x=35, y=500, width=400, height=68)
    myButton1 = Button(canvas, bg=color4, font=('Modern', 18, "bold"), justify="center", text="Launch Camera", command=launch_camera).place(x=50, y=370, width=378, height=80)
    myButton2 = Button(canvas, bg=color4, font=('Modern', 18, "bold"), justify="center", text="Instruction", command=instructions).place(x=50, y=190, width = 378, height =80)
    myButton3 = Button(canvas, bg=color4, font=('Modern', 18, "bold"), justify="center", text="ASL Dictionary", command=texttoimage).place(x=50, y=280, width=378, height=80)
    #myButton4 = Button(canvas, bg=color4, font=('Modern', 18, "bold"), justify="center", text="Settings", command=settings).place(x=50, y=430, width=378, height=68)
    root.mainloop()

def closeAndopenSettings(self):
    self.destroy()
    settings()

def mouseClick():
    winsound.PlaySound('click.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)


def texttoimage():
    mouseClick()
    child = tkinter.Toplevel(root)
    child.geometry(align2)
    child.resizable(width=False, height=False)
    child.iconphoto(True, PhotoImage(file='Logo.png'))

    canvas = Canvas(child, bg=color2, width=width2, height=height2)
    canvas.pack()
    canvas2 = Canvas(canvas, bg=color1, width=625, height=height2)
    canvas2.place(x=35, y=0)

    myLabel = Label(canvas2, bg=color1, justify="center", font=('Modern', 30, "bold"), text=("ASL Dictionary")).place(x=160, y=2, width=320, height=100)
    myLabel = Label(canvas2, bg=color1, fg=color3, justify="center", font=('Modern', 15, "bold"), text=("Which ASL sign are you looking for?")).place(x=160, y=85, width=320, height=50)
    myEntry = (Entry(canvas2, justify="center", font=('Modern', 20)))
    myEntry.place(x=90, y=150, width=320, height=50)
    myText = Text(canvas2, font=('Modern', 20), wrap=constants.WORD).place(x=50, y=240, width=520, height=300)
    myButton = Button(canvas2, bg=color4, font=('Modern', 18, "bold"), justify="center", text=("Lookup"), command=lambda: PlayWord(myEntry.get())).place(x=440, y=150, width=100, height=50)
    ##^^^ changed to insert entered text into video find/play to search for and play relevant vid.

def instructions():
    mouseClick()
    child = tkinter.Toplevel(root)
    child.geometry(align2)
    child.resizable(width=False, height=False)
    child.iconphoto(True, PhotoImage(file='Logo.png'))

    canvas = Canvas(child, bg=color2, width=width2, height=height2)
    canvas.pack()
    canvas2 = Canvas(canvas, bg=color1, width=625, height=height2)
    canvas2.place(x=35, y=0)

    myLabel = Label(canvas2, bg=color1, justify="center", font=('Modern', 30, "bold"),text=("Instructions")).place(x=160, y=2, width=320, height=100)
    myLabel1 = Label(canvas2, bg=color1, fg=color3, justify="left", font=('Modern', 20),text="Step 1: ").place(x=25, y=120)
    myLabel2 = Label(canvas2, bg=color1, justify="left", font=('Modern', 15), text="  Use text-to-image in order to find the desired ASL sign.\n  Take note of the finger placements!").place(x=100, y=123)
    myLabel3 = Label(canvas2, bg=color1, fg=color3, justify="left", font=('Modern', 20), text="Step 2: ").place(x=25, y=210)
    myLabel4 = Label(canvas2, bg=color1, justify="left", font=('Modern', 15),text="  Launch the camera. Present your ASL sign to the camera and \n  observe. Use the best lighting available to you!").place(x=100, y=213)
    myLabel5 = Label(canvas2, bg=color1, fg=color3, justify="left", font=('Modern', 20), text="Step 3: ").place(x=25, y=300)
    myLabel6 = Label(canvas2, bg=color1, justify="left", font=('Modern', 15), text="  If the sign was succesfully picked up by\n  the camera - then congratulations! If not, checkout the \n  additional resources provided and try again.").place(x=100, y=303)
    myLabel7 = Label(canvas2, bg=color1, fg=color3, justify="left", font=('Modern', 20), text="Step 4: ").place(x=25, y=410)
    myLabel8 = Label(canvas2, bg=color1, justify="left", font=('Modern', 15),text="  Most importantly - take it easy! Learning a new language is\n  a long process, so try taking it a few signs as a time until\n  you get the hang of it!").place(x=100, y=413)

def PlayWord(sentence):
    mouseClick()

    words = sentence.split()
    def play_video(video_file):
        #new tkinter popup window 4 vid playback
        video_window = tkinter.Toplevel()
        video_window.title("insert relevant word here")

        #tkinter frame 4 vid
        frame = ttk.Frame(video_window)
        frame.grid(column=0, row=0)

        video_capture = cv2.VideoCapture(video_file)

        #function for update vid frames
        def update_frame():
            ret, frame = video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                label.config(image=photo)
                label.image = photo
                video_window.after(10, update_frame)  #update frame every 10 ms

        #make label for vid frame:
        label = tkinter.ttk.Label(frame)
        label.grid(column=0, row=0)

        #self-explanatory:
        update_frame()

        #start tkinter main loop for the video
        video_window.mainloop()

    for word in words:
        video_url = get_video_link(word)
        if video_url:
            play_video(video_url)
        else:
            print(f"Sorry, {word} not in the database.")


def PlayWord2(word):
    #get vid link:
    video_url = get_video_link(word)

    #kaggle


    def play_video(video_file):
        #new tkinter popup window 4 vid playback
        video_window = tkinter.Toplevel()
        video_window.title("insert relevant word here")

        #tkinter frame 4 vid
        frame = ttk.Frame(video_window)
        frame.grid(column=0, row=0)

        video_capture = cv2.VideoCapture(video_file)

        #function for update vid frames
        def update_frame():
            ret, frame = video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                label.config(image=photo)
                label.image = photo
                video_window.after(10, update_frame)  #update frame every 10 ms

        #make label for vid frame:
        label = tkinter.ttk.Label(frame)
        label.grid(column=0, row=0)

        #self-explanatory:
        update_frame()

        #start tkinter main loop for the video
        video_window.mainloop()

    if video_url:
        play_video(video_url)
        #play_video('https://www.signingsavvy.com/media2/mp4-ld/21/21622.mp4')
    else:
        print("Sorry, (" + word + ") not in db")

        #play_video('https://www.signingsavvy.com/media2/mp4-ld/21/21622.mp4')


def spellItOut(word):
    conn = sqlite3.connect('letters.db')
    cursor = conn.cursor()
    # case INSENSITIVE change:

    letter_list = []

    for letter in word:
        cursor.execute("SELECT letter_url FROM letters WHERE letter = ? COLLATE NOCASE", (letter,))
        letter_url = cursor.fetchone()

        letter_list.insert(letter_url)

def get_video_link(word):
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()
    #case INSENSITIVE change:
    cursor.execute("SELECT video_url FROM dictionary WHERE word = ? COLLATE NOCASE", (word,))

    video_url = cursor.fetchone()
    conn.close()

    if video_url:
        print(video_url)
        return video_url[0]
    else:
        print('cursor did not fetchone')
        #return None
        return 'word_not_found.mp4'


def get_letter_link(letter):
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()

    cursor.execute("SELECT letter_url FROM dictionary WHERE letter = ?", (letter,))

    letter_url = cursor.fetchone()
    conn.close()

    if letter_url:
        return letter_url[0]
    else:
        return None


menu()
