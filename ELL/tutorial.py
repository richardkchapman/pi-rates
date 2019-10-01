import sys
import os
import time
import cv2

import tutorial_helpers as helpers
import model

def get_image_from_camera(camera):
    if camera:
        ret, frame = camera.read()
        if not ret:
            raise Exception("your capture device is not returning images")
        return frame
    return None

def main():
    camera = cv2.VideoCapture(0)
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
        cv2.imshow("ELL model", image)

if __name__ == "__main__":
    main()
