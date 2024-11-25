from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json, os
from . credentials import MpesaAccessToken, LipanaMpesaPassword

from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, 'home.html', {'navbar':'home'})


def token(request):
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    api_URL = os.getenv('API_URL')

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})



def pay(request):
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = os.getenv('API_URL')
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
            "Password": LipanaMpesaPassword.decode_password,
            "Timestamp": LipanaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Cynthia Inc",
            "TransactionDesc": "Web Dev Charges"
        }

        



    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse("success")


def stk(request):
    return render(request, 'pay.html', {'navbar':'stk'})