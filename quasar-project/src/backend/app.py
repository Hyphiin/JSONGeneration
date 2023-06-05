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
import torch


app = Flask(__name__)

cors = CORS()
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})

model = YOLO("best.pt")

@app.route('/predict', methods=['POST'])
def predict():
    preds_list = []
    for fname in request.files:
        f = request.files.get(fname)
        img = Image.open(f.stream)
        prediction = model.predict(img, conf=0.5)
        preds_plotted = prediction[0].plot()

        pil_image = Image.fromarray(preds_plotted)
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        img_base64 = base64.b64encode(img_byte_arr).decode('ascii')

        if prediction:
            for pred in prediction:
                for pre in pred:
                  print("PRE: ",pre.boxes)
                  box = pre.boxes
                  class_number = box.cls[0].item()
                  class_name = pre.names[class_number]
                  single_object = {
                      "x": box.xywh[0][0].item(),
                      "y":box.xywh[0][1].item(),
                      "width": box.xywh[0][2].item(),
                      "height": box.xywh[0][3].item(),
                      "confidence": box.conf[0].item(),
                      "class": class_name
                  }
                  print("Single Object: ",single_object)
                  preds_list.append(single_object)

    return jsonify(predictions=preds_list, image=img_base64)


if __name__ == '__main__':
    if not os.path.exists('./predicts'):
        os.mkdir('./predicts')
    app.run(debug=True)
