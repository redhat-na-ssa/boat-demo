import threading
import numpy as np
import sklearn.cluster


# Grouping parameters
GROUP_RFACTOR = 3


def meanshift_group(meta1=None):
    """ Use meanshift clustering to find groups. """
    # initialize datasets
    if not meta1:
        return {}
    centroids = [item.get('centroid', [0,0]) for item in meta1.get('objects', [])]
    
    # calculate average object length
    lengths = [((item['box'][2] - item['box'][0])**2 + (item['box'][3] - item['box'][1])**2) ** 0.5 
               for item in meta1.get('objects', [])]
    r = np.mean(lengths)
    
    # fit the clustering algorithm
    clustering = sklearn.cluster.MeanShift(bandwidth=GROUP_RFACTOR*r).fit(centroids)
    
    # parse the results
    groups = clustering.labels_
    groups_centroids = clustering.cluster_centers_
        
    # update metadata
    for index in range(len(meta1.get('objects', []))):
        meta1['objects'][index]['cluster'] = int(groups[index])
    meta1['clusters'] = groups_centroids.tolist()
        
    return meta1