from datetime import datetime
import requests

#
# Test client for serverless function.
#

#
# To obtain IDENT_URL :
#
# kn service list
#

IDENT_URL="http://identify-serverless-boats.apps.ocp.d1db.sandbox1682.opentlc.com"

time0 = (datetime(2021, 4, 22, 3, 40, 31, 994728),
 None,
 {'objects': [{'box': [207.0, 509.0, 299.0, 532.0],
      'confidence': 0.8941678404808044,
      'class': 'boats'},
     {'box': [65.0, 326.0, 136.0, 403.0],
      'confidence': 0.8731332421302795,
      'class': 'boats'},
     {'box': [1066.0, 109.0, 1142.0, 171.0],
      'confidence': 0.8629531264305115,
      'class': 'boats'},
     {'box': [82.0, 602.0, 149.0, 671.0],
      'confidence': 0.8608279228210449,
      'class': 'boats'},
     {'box': [298.0, 438.0, 383.0, 461.0],
      'confidence': 0.8419623374938965,
      'class': 'boats'},
     {'box': [242.0, 0.0, 298.0, 19.0],
      'confidence': 0.6364468932151794,
      'class': 'boats'}]})
#time1 = pipeline.snap()
time1 = (datetime(2021, 4, 22, 3, 40, 32, 757943),
 None,
 {'objects': [{'box': [211.0, 508.0, 307.0, 532.0],
      'confidence': 0.8908742070198059,
      'class': 'boats'},
     {'box': [1073.0, 113.0, 1147.0, 176.0],
      'confidence': 0.8825204968452454,
      'class': 'boats'},
     {'box': [67.0, 325.0, 136.0, 405.0],
      'confidence': 0.8686448931694031,
      'class': 'boats'},
     {'box': [81.0, 601.0, 151.0, 672.0],
      'confidence': 0.8586115837097168,
      'class': 'boats'},
     {'box': [305.0, 438.0, 390.0, 462.0],
      'confidence': 0.8368647694587708,
      'class': 'boats'}]})

response = requests.post(IDENT_URL, json={"last": time0[2]}).json()
# print(f'response = {response}')

time0 = (time0[0], time0[1], response)
print(time0)

#
# To test using curl:
#
# IDENT_URL=$(kn service list identify-serverless --no-headers | awk '{print $2}')
# curl -X POST --data '{"last":{"objects": [{"box": [211.0, 508.0, 307.0, 532.0], "confidence": 0.8908742070198059, "class": "boats"}]}}' -H "Content-Type: application/json" ${IDENT_URL}
#
