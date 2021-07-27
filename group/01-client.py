from datetime import datetime
import requests
#
# Test client for serverless function.
#

#
# To set the GROUP_URL :
#
# kn service list
#

GROUP_URL="http://group-serverless-boats.apps.ocp.d1db.sandbox1682.opentlc.com"

#time0 = pipeline.snap()
time0 = {'objects': [{'box': [521.0, 417.0, 609.0, 442.0],
    'confidence': 0.8895850777626038,
    'class': 'boats',
    'id': '4',
    'centroid': [565.0, 429.5],
    'speed': 3.5681668404020375,
    'direction': 0.0},
   {'box': [382.0, 500.0, 469.0, 527.0],
    'confidence': 0.8717858195304871,
    'class': 'boats',
    'id': '0',
    'centroid': [425.5, 513.5],
    'speed': 9.589160252084428,
    'direction': 7.125016348901757},
   {'box': [98.0, 354.0, 184.0, 417.0],
    'confidence': 0.8691210150718689,
    'class': 'boats',
    'id': '2',
    'centroid': [141.0, 385.5],
    'speed': 6.935269733055477,
    'direction': 30.96375653207352},
   {'box': [70.0, 601.0, 136.0, 678.0],
    'confidence': 0.8541313409805298,
    'class': 'boats',
    'id': '3',
    'centroid': [103.0, 639.5],
    'speed': 1.1893889468006793,
    'direction': 90.0},
   {'box': [1234.0, 269.0, 1280.0, 331.0],
    'confidence': 0.6892146468162537,
    'class': 'boats',
    'id': '1',
    'centroid': [1257.0, 300.0],
    'speed': 1.6820499795021724,
    'direction': 45.00000000000001}],
  'tracking': {'next_id': 5, 'missing': {}}}


response = requests.post(GROUP_URL, json={'last': {}, "last_time": 123, "now_time": 123, "now": time0}).json()
print(f'response = {response}')
