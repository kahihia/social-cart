__author__ = 'indrajit'

import requests
import json
from settings import GOOGLE_API_KEY

GCM_URL = 'https://gcm-http.googleapis.com/gcm/send'


def send_gcm_notification(data_dict):
    json_data = json.dumps(data_dict)
    r = requests.post(GCM_URL, json=json_data, headers={'Authorization': 'key='+GOOGLE_API_KEY})