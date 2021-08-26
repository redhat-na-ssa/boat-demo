from parliament import Context
import logging
import detection
import torch
import json

#
# Set a few global constants.
#
weights = f'./weights.pt'
IMGSZ = 704
DEVICE = 'cpu'

#
# Load the model/weights from storage. This should only happen once after the pod starts.
#
logging.warning(f'Pytorch version: {torch.__version__}')
logging.warning(f'Loading model file: {weights}')

try:
    (model, stride, imgsz) = detection.load_model(weights, DEVICE, IMGSZ)
    logging.warning(f'Model loaded, stride = {stride}, image size = {imgsz}')
except:
    logging.warning(f'Error loading model!')

#
# Main (gets called with every request)
#
def main(context: Context):
    """ 
    Main function
    The context parameter contains the Flask request object and any
    CloudEvent received with the request.
    """
    global model
    global stride
    global imgsz

    request = context.request
        
    img_file = None
    if request.files.get("image"):
        img_file = request.files["image"].read()
        logging.warning(f'main(): Returning prediction.')
        return json.dumps(detection.detect(img_file, model, stride, imgsz))
    else:
        return { "message": "Bad data, no prediction!" }, 200
