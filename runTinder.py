#!/usr/local/bin/python3.6
import sys
import json
import requests
from fbTinderAccess import *

tinderToken = None
hostName = "https://api.gotinder.com"
header = {
    "X-Auth-Token": tinderToken,
    "app_version": "6.9.4",
    "platform": "ios",
    "content-type": "application/json",
    "User-agent": "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)",
    "Accept": "application/json"
}

def getFacebookAuth(fbEmail, fbPassword):
    accessToken = get_fb_access_token(fbEmail, fbPassword)
    fbId = get_fb_id(accessToken)
    return {"facebook_token": accessToken, "facebook_id": fbId}

def getTinderToken(fbAuth):
    r = requests.post(hostName + '/auth', data = fbAuth)
    return r.json()['token']

def getRecommendations():
    r = requests.get(hostName + '/user/recs', headers = header)
    print(r.json())

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("----------------------------------------------------------------------")
        print("Please enter both your fb email and password as command line arguments\n")
        print("For example: ./runTinder.py fbEmail fbPassword")
        print("----------------------------------------------------------------------")
        sys.exit()

    fbAuth = getFacebookAuth(sys.argv[1], sys.argv[2])
    tinderToken = getTinderToken(fbAuth)
    header['X-Auth-Token'] = tinderToken
    getRecommendations()


    
    


