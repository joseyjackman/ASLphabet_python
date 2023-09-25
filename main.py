"""--------------------------------------------------------------------------
                                    Import Start
--------------------------------------------------------------------------"""
import cv2
import cv2 as cv
from PIL import Image
from pytesseract import pytesseract

# ----------------------------------------------
#           Unused Import Start
# ----------------------------------------------
# import numpy as np
# import matplotlib.pyplot as plt
# import tensorflow as tf
# ----------------------------------------------
#            Unused Import End
# ----------------------------------------------
"""--------------------------------------------------------------------------
                                    Import End
--------------------------------------------------------------------------"""
"""--------------------------------------------------------------------------
                               Start of Main Method
--------------------------------------------------------------------------"""
# Initialize the webcam
camera = cv2.VideoCapture(0)

while True:
    _, image = camera.read()  # Read the webcam stream till the loop breaks

    cv2.imshow('Text detection', image)

    # Capture a window that will print the text in the image
    if cv2.waitKey(1) & 0xFF == ord('s'):  # if you press s then it will screenshot on the popup window
        cv2.imwrite('test1.jpg', image)  # stores image as a test1.jpg
        break

# Release the webcam and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()


def tesseract():
    # The following is the path to the tesseract executable
    path_to_tesseract = r"C:\Users\Draco\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    imagepath = 'test1.jpg'

    # Set the Tesseract executable path
    pytesseract.tesseract_cmd = path_to_tesseract

    # Use Tesseract to extract text from the captured image
    text = pytesseract.image_to_string(Image.open(imagepath))

    # Print the extracted text, excluding the last character
    print(text[:-1])


tesseract()

"""--------------------------------------------------------------------------
                               Start of Main Method
--------------------------------------------------------------------------"""
