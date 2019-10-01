import cv2
import numpy as np
import tutorial_helpers as helpers
import model

model_wrapper = model.ModelWrapper()

input_shape = model_wrapper.GetInputShape()
output_shape = model_wrapper.GetOutputShape()

print("Model input shape: [{0.rows}, {0.columns}, {0.channels}]".format(
    input_shape))
print("Model output shape: [{0.rows}, {0.columns}, {0.channels}]".format(
    output_shape))

preprocessing_metadata = helpers.get_image_preprocessing_metadata(model_wrapper)
sample_image = cv2.imread("coffeemug.jpg")

input_data = helpers.prepare_image_for_model(sample_image, input_shape.columns,
                                             input_shape.rows, preprocessing_metadata=preprocessing_metadata)

input_data = model.FloatVector(input_data)
predictions = model_wrapper.Predict(input_data)
prediction_index = int(np.argmax(predictions))
print("Category index: {}".format(prediction_index))
print("Confidence: {}".format(predictions[prediction_index]))
