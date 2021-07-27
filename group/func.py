from parliament import Context
import grouping
import json
import logging
 
def main(context: Context):
    """
    Call the grouping algorythm and return the json. 
    """
    data = context.request.get_json(silent=True)
    if data:
        resp = grouping.meanshift_group(data.get('now'))
        return json.dumps(resp), 200
    else:
        logging.warning(f'**************** main(): Invalid data was received.')
        return {"invalid":"data!"}, 204
