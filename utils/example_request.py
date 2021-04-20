"""Perform test request"""
import pprint

import requests

DETECTION_URL = "http://localhost:8080/v1/detect"
TEST_IMAGE = "boats.png"

image_data = open(TEST_IMAGE, "rb").read()
import pdb; pdb.set_trace()

response = requests.post(DETECTION_URL, files={"image": image_data}).json()

pprint.pprint(response)
