"""
Run a rest API exposing the yolov5s object detection model
"""
import argparse
import io
import json
import os

import cv2
from PIL import Image
from flask import Flask, request
import numpy as np
import torch

from yolov5.models.experimental import attempt_load
from yolov5.utils.datasets import letterbox
from yolov5.utils.general import check_img_size, non_max_suppression, scale_coords


# Model Parameters
WEIGHTS = os.path.join(os.path.dirname(__file__), 'weights.pt')
IMGSZ = 704
CONF_THRESH = 0.4  # Object confidence threshold
IOU_THRESH = 0.45  # IOU threshold for NMS
NMS_CLASSES = None  # Class filter for NMS
AGNOSTIC_NMS = False  # Class agnostic NMS
CLASS_MAP = ['boats']

# Hardware Parameters
DEVICE = 'cpu'


def load_model(weights=WEIGHTS, device=DEVICE, imgsz=IMGSZ):
    """ Load the YoloV5 model. """
    model = attempt_load(weights, map_location=device)
    stride = int(model.stride.max())
    imgsz = check_img_size(imgsz, s=stride)
    return (model, stride, imgsz)


def preprocess(image_file, stride, imgsz):
    """ Prepare the input for inferencing. """
    # read image file
    img = np.asarray(bytearray(image_file), dtype="uint8")
    img = cv2.imdecode(img, 1)
    imgsz0 = torch.Tensor(img.shape[:2])

    # resize image
    img = letterbox(img, imgsz, stride=stride)[0]

    # convert from BGR to RGB
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)

    # convert to tensor
    img = torch.from_numpy(img).to(DEVICE)

    # normalize RGB values to percentage
    img = img.float() / 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    return img, imgsz0


def postprocess(predictions, imgsz0, imgsz1):
    """ Convert class IDs to class names. """
    predictions[:, :4] = scale_coords(imgsz1, predictions[:, :4], imgsz0).round()
    predictions = predictions.cpu().numpy().tolist()
    return [{"box": row[:4],
             "confidence": row[4],
             "class": CLASS_MAP[int(row[5])]} for row in predictions]


def detect(img_file, model, stride, imgsz):
    # preprocess image
    img, imgsz0 = preprocess(img_file, stride, imgsz)

    # run inferencing
    pred = model(img)[0]
    pred = non_max_suppression(pred, CONF_THRESH, IOU_THRESH, NMS_CLASSES, agnostic=AGNOSTIC_NMS)[0]

    # postprocess results
    pred = postprocess(pred, imgsz0, img.shape[2:])

    # return the results
    return {'objects': pred}