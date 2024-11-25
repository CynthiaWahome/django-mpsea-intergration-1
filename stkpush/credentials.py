import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
from dotenv import load_dotenv
import os
load_dotenv()


class MpesaC2BCredential:
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    api_URL = os.getenv('API_URL')


class MpesaAccessToken:
    r = requests.get(MpesaC2BCredential.api_URL,
                     auth=HTTPBasicAuth(MpesaC2BCredential.consumer_key, MpesaC2BCredential.consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]


class LipanaMpesaPassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "174379"
    OffSetValue = '0'
    passkey = os.getenv('PASSKEY')

    data_to_encode = Business_short_code + passkey + lipa_time

    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')
