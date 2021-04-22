import argparse

from flask import Flask, request
from detection import load_model, detect

# Web Server Configuration
DETECTION_URL = "/v1/detect"
PORT = 8080


class ModelServer(Flask):
    """ Flask server that contains a YoloV5 model. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_model()

    def load_model(self):
        """ Load the YoloV5 model. """
        (self.model, self.strid, self.imgz) = load_model()
        
APP = ModelServer(__name__)


@APP.route(DETECTION_URL, methods=["POST"])
def detect(img_file=None):
    if request.files.get("image"):
        img_file = request.files["image"].read()
        return json.dumps(detect(img_file))

    
def parse_args():
    """ Parse CLI arguments. """
    parser = argparse.ArgumentParser(description="Flask api exposing yolov5 model")
    parser.add_argument("--port", default=PORT, type=int, help="port number")
    args = parser.parse_args()
    return args.port


def main():
    port = parse_args()
    APP.run(host='0.0.0.0', port=port)

    
if __name__ == "__main__":
    main()
