from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import sys
import os
import time
import cv2

import tutorial_helpers as helpers
import model

def init_options():
    global verbose
    verbose = False

def get_image_from_camera(camera):
    if camera:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            return frame.array
    return None

def init_camera():
    global camera
    global rawCapture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    # these values will depend on the lens mounted on the dslr - adjust to fit your needs
    camera.zoom = (0.45,0.38,0.2,0.2)
    # because we are only reading part of the sensor the auto-exposure seems to get things rather wrong
    camera.exposure_compensation = -24
    rawCapture = PiRGBArray(camera, size=(640, 480))

def init_GPIO():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18,GPIO.OUT)

def press_shutter():
    GPIO.output(18, True)

def release_shutter():
    GPIO.output(18, False)

def main():
    init_GPIO()
    init_camera()
    init_options()
    shoot_categories = set([504])
    with open("categories.txt", "r") as categories_file:
        categories = categories_file.read().splitlines()
    model_wrapper = model.ModelWrapper()
    input_shape = model_wrapper.GetInputShape()
    preprocessing_metadata = helpers.get_image_preprocessing_metadata(model_wrapper)
    while (cv2.waitKey(1) & 0xFF) == 0xFF:
        image = get_image_from_camera(camera)
        input_data = helpers.prepare_image_for_model(
            image, input_shape.columns, input_shape.rows, preprocessing_metadata=preprocessing_metadata)
        input_data = model.FloatVector(input_data)
        predictions = model_wrapper.Predict(input_data)
        top_5 = helpers.get_top_n(predictions, 5)
        header_text = ", ".join(["({:.0%}) {}".format(
            element[1], categories[element[0]]) for element in top_5])
        helpers.draw_header(image, header_text)
        if top_5:
            print ( header_text )
        release_shutter()
        for element in top_5:
            if verbose:
                print ( element[0] )
            if element[0] in shoot_categories:
                press_shutter()
                break
        cv2.imshow("BirdWatcher", image)
        rawCapture.truncate(0)

if __name__ == "__main__":
    main()
