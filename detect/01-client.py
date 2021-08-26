import os
import sys

from PIL import Image, ImageDraw
import requests

IMAGE = os.path.abspath('../boats.png')
DETECTION_URL = 'http://127.0.0.1:8080'
DETECTION_URL = 'http://detect-serverless-boats-demo.apps.ocp.d1db.sandbox1682.opentlc.com'

response = requests.post(DETECTION_URL, files={"image": open(IMAGE, "rb").read()}).json()
print(f'response = {response}')
