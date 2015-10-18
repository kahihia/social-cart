__author__ = 'indrajit'

import requests
import json
from settings import GOOGLE_API_KEY
from .models import logger

GCM_URL = 'https://gcm-http.googleapis.com/gcm/send'


def send_gcm_notification(data_dict):
    try:
        logger.info(data_dict)
        json_data = json.dumps(data_dict)
        r = requests.post(GCM_URL, json=data_dict, headers={'Authorization': 'key='+GOOGLE_API_KEY})
        logger.exception(r)
        r.raise_for_status()
    except Exception as e:
        logger.exception(e)
