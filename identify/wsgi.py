import argparse
import json

from flask import Flask, request
import identification

# Web Server Configuration
IDENTIFY_URL = "/v1/identify"
PORT = 8080

APP = Flask(__name__)


@APP.route(IDENTIFY_URL, methods=["POST"])
def identify():
    data = request.get_json(silent=True)
    if data:
        resp = identification.centroid_identify(data.get('last_time'), \
                                                data['last'], \
                                                data.get('now_time'), \
                                                data.get('now'))
        return json.dumps(resp)
    
    
def parse_args():
    """ Parse CLI arguments. """
    parser = argparse.ArgumentParser(description="Object identification API.")
    parser.add_argument("--port", default=PORT, type=int, help="port number")
    args = parser.parse_args()
    return args.port


def main():
    port = parse_args()
    APP.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    main()