from parliament import Context

import json
import identification
import logging
 
logging.warning(f'Outside main')

def main(context: Context):
    """ 
    Function template
    The context parameter contains the Flask request object and any
    CloudEvent received with the request.
    """
    logging.warning(f'Inside main, context = {context}')
    
    data = context.request.get_json(silent=True)

    if data:
        resp = identification.centroid_identify(data.get('last_time'), data['last'], data.get('now_time'), data.get('now'))
        return json.dumps(resp), 200
    
    else:
        return {"invalid":"data!"}, 204
