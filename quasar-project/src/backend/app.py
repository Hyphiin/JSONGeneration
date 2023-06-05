from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask_cors import CORS
import os
from PIL import Image
from ultralytics import YOLO
import cv2
import numpy as np
import base64
import io


app = Flask(__name__)

# This is necessary because QUploader uses an AJAX request
# to send the file
cors = CORS()
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})

model = YOLO("best.pt")

# @app.route('/predict', methods=['POST'])
# def predict():
#     preds_list = []
#     for fname in request.files:
#         f = request.files.get(fname)
#         img = Image.open(f.stream)  # Open image file
#         preds = model(img)  # Run model prediction
#         preds_plotted = preds[0].plot()

#         if preds:  # Check if preds is not None or empty
#             for pred in preds:
#                 if hasattr(pred, 'to_dict'):
#                     preds_list.append(pred.to_dict())
#                 else:
#                     preds_list.append(str(pred))

#     return jsonify(predictions=preds_list)  # Return JSON response

@app.route('/predict', methods=['POST'])
def predict():
    preds_list = []
    for fname in request.files:
        f = request.files.get(fname)
        img = Image.open(f.stream)  # Open image file
        preds = model(img)  # Run model prediction
        preds_plotted = preds[0].plot()

        # Convert the numpy array image to PIL Image, then save to BytesIO
        pil_image = Image.fromarray(preds_plotted)
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Convert the byte string into a base64 string
        img_base64 = base64.b64encode(img_byte_arr).decode('ascii')

        if preds:  # Check if preds is not None or empty
            for pred in preds:
                if hasattr(pred, 'to_dict'):
                    preds_list.append(pred.to_dict())
                else:
                    preds_list.append(str(pred))

    return jsonify(predictions=preds_list, image=img_base64)


if __name__ == '__main__':
    if not os.path.exists('./predicts'):
        os.mkdir('./predicts')
    app.run(debug=True)
