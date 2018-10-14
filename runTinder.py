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

    if "error" in fbId:
        sys.exit()

    return {"facebook_token": accessToken, "facebook_id": fbId}

def getTinderToken(fbAuth):
    try:
        r = requests.post(hostName + '/auth', data = fbAuth)
        r.raise_for_status()
        return r.json()['token']
    except requests.exceptions.RequestException as e:
        print("Request has failed: couldn't get tinder token")
        print(e)
        sys.exit()

def getProfile():
    try:
        r = requests.get(hostName + '/profile', headers = header)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Request has failed")
        print(e)
        sys.exit()

def getRecommendations():
    try:
        r = requests.get(hostName + '/user/recs', headers = header)
        r.raise_for_status()
        return r.json()["results"]
    except requests.exceptions.RequestException as e:
        print("Request has failed")
        print(e)
        sys.exit()

def likeById(id):
    try:
        r = requests.get(hostName + '/like/' + id, headers = header)
        r.raise_for_status()
        print("Match? " + str(r.json()["match"]) + ", likes remaining: " + str(r.json()['likes_remaining']))
    except requests.exceptions.RequestException as e:
        print("Request has failed")
        print(e)
        sys.exit()
    

def autoLike(iterations):
    personList = []
    personList = getRecommendations()
    personIds = [person['_id'] for person in personList]

    #print("Initial list size: " + str(len(personIds)))

    while len(personIds) < iterations:
        print("Masterlist size: " + str(len(personIds)))
        #print("MASTER BEFORE: " + str(sorted(personIds)))
        tempList = []
        tempList = getRecommendations()
        tempListIds = [temp['_id'] for temp in tempList] 
        #print("TEMPLIST: " + str(sorted(tempListIds)))
        personIds.extend(list(set(tempListIds) - set(personIds)))
        #print("Temp list size: " + str(len(tempListIds)))
        #print("MASTER AFTER: " + str(sorted(personIds)))
        #print("NEW Masterlist size: " + str(len(personIds)))

    count = 0
    for id in personIds:
        if count == iterations:
            break
        print(id)
        #likeById(id)
        count += 1

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("----------------------------------------------------------------------")
        print("Please enter both your fb email and password as command line arguments\n")
        print("For example: ./runTinder.py fbEmail fbPassword")
        print("----------------------------------------------------------------------")
        sys.exit()
    elif len(sys.argv) > 3:
        iterations = 0
        if sys.argv[3] is not None and str.isdigit(sys.argv[3]):    
            iterations = int(sys.argv[3])

        fbAuth = getFacebookAuth(sys.argv[1], sys.argv[2])
        tinderToken = getTinderToken(fbAuth)

        header['X-Auth-Token'] = tinderToken
        if iterations > 0:
            autoLike(iterations)
