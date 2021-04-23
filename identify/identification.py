import threading
import numpy as np
import scipy.spatial

_ID_GEN_LOCK = threading.Lock()

# Tracking parameters
NEW_OBJ_THRESHOLD = 100  # pixels
EXPIRE_THRESHOLD = 40  # frames


def _db_generate():
    return {'next_id': 0, 'missing': {}}


def _id_generate(db):
    _ID_GEN_LOCK.acquire(True)
    next_id = db['next_id']
    db['next_id'] += 1
    _ID_GEN_LOCK.release()
    return str(next_id)


def _ensure_ids(meta, db):
    """ Ensure all objects in frame have IDs. """
    for item in meta['objects']:
        if not item.get('id'):
            item['id'] = _id_generate(db)


def centroid_identify(meta0, meta1=None):
    """ Identify tracked objects from previous frame to current frame. """
    # initialize database if necessary
    db = meta0.get('tracking')
    if not db:
        db = _db_generate()
    _ensure_ids(meta0, db)

    # return formatted frame data if no comparison was requested
    if not meta1:
        meta0['tracking'] = db
        return meta0

    # calculate centroids of all objects
    centroids0 = [np.mean(np.array(item['box']).reshape((2, 2)), axis=0)
                  for item in meta0['objects']]
    ids0 = [item['id'] for item in meta0['objects']]
    centroids1 = [np.mean(np.array(item['box']).reshape((2, 2)), axis=0)
                  for item in meta1['objects']]

    # add missing objects to old frame data
    ids_missing = list(db['missing'].keys())
    centroids_missing = [db['missing'][ident]['centroid'] for ident in ids_missing]
    centroids0 += centroids_missing
    ids0 += ids_missing
                    
    # placeholder in old frame for new objects
    null = len(ids0)
    ids0.append(None)

    # calculate distance between all new and all old objects
    distances = scipy.spatial.distance.cdist(centroids1, centroids0)
    eligible = distances <= NEW_OBJ_THRESHOLD

    # assume the shortest distance moved is the match
    new2old = [distances[idx].argmin() for idx in range(distances.shape[0])]
    new2old = [new2old[idx] if eligible[idx][new2old[idx]] else null for idx in range(distances.shape[0])]
    ids1 = np.array(ids0)[new2old].tolist()
                    
    # assign ids to new objects
    ids1 = [ident or _id_generate(db) for ident in ids1]
                    
    # report found objects
    for found in [ident for ident in ids_missing if ident in ids1]:
        del db['missing'][found]
                    
    # report new missing objects
    lost = [ident for ident in ids0 if ident and ident not in ids1 and ident not in ids_missing]
    for ident in lost:
        known_info = next(item for item in meta0['objects'] if item["id"] == ident)
        last_loc = centroids0[ids0.index(ident)]
        db['missing'][ident] = known_info
        db['missing'][ident]['centroid'] = last_loc.tolist()
        db['missing'][ident]['frames'] = 0
                    
    # bury expired objects
    new_missing = {}
    for ident, item in db['missing'].items():
        item['frames'] += 1
        if item['frames'] <= EXPIRE_THRESHOLD:
            new_missing[ident] = item
    db['missing'] = new_missing

    # update metadata
    for index in range(len(ids1)):
        meta1['objects'][index]['id'] = ids1[index]
        meta1['objects'][index]['centroid'] = centroids1[index].tolist()
    meta1['tracking'] = db
                    
    return meta1