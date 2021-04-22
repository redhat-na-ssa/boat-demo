

def tmp():
    # calculate centroids of all objects
    centroids0 = [np.mean(np.array(item['box']).reshape((2, 2)), axis=0)
                  for item in time0[2]['detect'][-1]['objects']]
    ids0 = np.array([random.randint(0,50) for i in range(len(centroids0))]) # make some fake ids like mclovin
    centroids1 = [np.mean(np.array(item['box']).reshape((2, 2)), axis=0)
                  for item in time1[2]['detect'][-1]['objects']]

    # calcualte distance between all new and all old objects
    distances = scipy.spatial.distance.cdist(centroids1, centroids0)

    # assume the shortest distance moved is the match
    new2old = [distances[idx].argmin() for idx in range(distances.shape[0])]
    ids1 = ids0[new2old]

    print(ids0)
    print(ids1)