#!/usr/local/bin/python3.7
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

    while len(personIds) < iterations:
        tempList = []
        tempList = getRecommendations()
        tempListIds = [temp['_id'] for temp in tempList]
        personIds.extend(list(set(tempListIds) - set(personIds)))

    count = 0
    for id in personIds:
        if count == iterations:
            break
        likeById(id)
        count += 1

if __name__ == "__main__":
    if len(sys.argv) < 3:
        if len(sys.argv) == 2 and sys.argv[1] == "help":
            print("----------------------------------------------------------------------")
            print("How to use this program:\n")
            print("1) Enter the base arguments:\n\tpython runTinder.py\n")
            print("2) Add in your facebook email and password separated by spaces:")
            print("\tpython runTinder.py user@gmail.com password\n")
            print("3) Add in the number of times you want to run the program:")
            print("\tpython runTinder.py user@gmail.com password 100\n")
            print("4) Press enter and hope for the best\n")
            print("Note: Tinder gives you about 100 likes per 12 hours")
            print("Please send me a fb message or email at dimitar@uoguelph.ca if you ")
            print("have any feedback")
            print("----------------------------------------------------------------------")
            sys.exit()
        else:
            print("----------------------------------------------------------------------")
            print("Please enter both your fb email and password as command line arguments\n")
            print("For example: python runTinder.py fbEmail fbPassword")
            print("----------------------------------------------------------------------")
            sys.exit()
    elif len(sys.argv) == 3:
        print("----------------------------------------------------------------------")
        print("Please enter the number of iterations you wish to run\n")
        print("For example: python runTinder.py fbEmail fbPassword 10")
        print("----------------------------------------------------------------------")
        sys.exit()
    elif len(sys.argv) > 3:
        iterations = 0
        if sys.argv[3] is not None and str.isdigit(sys.argv[3]):
            iterations = int(sys.argv[3])
            if iterations > 0:
                fbAuth = getFacebookAuth(sys.argv[1], sys.argv[2])
                tinderToken = getTinderToken(fbAuth)
                header['X-Auth-Token'] = tinderToken
                autoLike(iterations)   
        else:
            print("----------------------------------------------------------------------")
            print("Invalid iteration number, please try again")
            print("----------------------------------------------------------------------")
            sys.exit()
