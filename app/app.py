"""
Run a rest API exposing the yolov5s object detection model
"""
import argparse
import io
import json

import cv2
from PIL import Image
from flask import Flask, request
import numpy as np
import torch

from yolov5.models.experimental import attempt_load
from yolov5.utils.datasets import letterbox
from yolov5.utils.general import check_img_size, non_max_suppression


# Web Server
APP = Flask(__name__)
DETECTION_URL = "/v1/detect"
PORT = 5000

# Model Parameters
MODEL = None
STRIDE = None
IMGSZ = 704
CONF_THRESH = 0.4  # Object confidence threshold
IOU_THRESH = 0.45  # IOU threshold for NMS
NMS_CLASSES = None  # Class filter for NMS
AGNOSTIC_NMS = False  # Class agnostic NMS
CLASS_MAP = ['boats']

# Hardware Parameters
DEVICE = 'cpu'


def preprocess(image_file):
    """ Prepare the input for inferencing. """
    # read image file
    img = image_file.read()
    img = np.asarray(bytearray(img), dtype="uint8")
    img = cv2.imdecode(img, 1)

    # resize image
    img = letterbox(img, IMGSZ, stride=STRIDE)[0]

    # convert from BGR to RGB
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)

    # convert to tensor
    img = torch.from_numpy(img).to(DEVICE)

    # normalize RGB values to percentage
    img = img.float() / 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    return img


def map_classes(predictions):
    """ Convert class IDs to class names. """
    return [{"x0": row[0], "y0": row[1],
             "x1": row[2], "y1": row[3],
             "confidence": row[4],
             "class": CLASS_MAP[int(row[5])]} for row in predictions]


@APP.route(DETECTION_URL, methods=["POST"])
def detect():
    if not request.method == "POST":
        return

    if request.files.get("image"):
        # load and prep the image
        img_file = request.files["image"]
        img = preprocess(img_file)

        # run inferencing
        pred = MODEL(img)[0]
        pred = non_max_suppression(pred, CONF_THRESH, IOU_THRESH, NMS_CLASSES, agnostic=AGNOSTIC_NMS)[0]
        pred = pred.cpu().numpy().tolist()
        pred = map_classes(pred)

        # return the results
        return json.dumps({'objects': pred})


def parse_args():
    """ Parse CLI arguments. """
    parser = argparse.ArgumentParser(description="Flask api exposing yolov5 model")
    parser.add_argument("--port", default=PORT, type=int, help="port number")
    args = parser.parse_args()
    return args.port


if __name__ == "__main__":
    # get user options
    PORT = parse_args()

    # load model
    MODEL = attempt_load('weights.pt', map_location='cpu')
    STRIDE = int(MODEL.stride.max())
    IMGSZ = check_img_size(IMGSZ, s=STRIDE)

    APP.run(host="0.0.0.0", port=PORT)
