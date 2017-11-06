from flask import Flask, send_from_directory
import os
import cv2
import test
import base64

app = Flask(__name__)
@app.route('/capture')
def captureImage():
    filename = 'image.png'
    camera_capture = None
    while camera_capture==None:
        camera_capture = test.get_image()
    cv2.imwrite(filename,camera_capture)
##    with open("image.png", "rb") as imageFile:
##        f = imageFile.read()
##        b = bytearray(f)
##        print(b)
    with open(filename, 'rb')as img:
        return img.read()

if __name__ == '__main__':
    app.run()