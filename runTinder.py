#!/usr/local/bin/python3.6
import sys
from fbTinderAccess import *

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("----------------------------------------------------------------------")
        print("Please enter both your fb email and password as command line arguments\n")
        print("For example: ./runTinder.py fbEmail fbPassword")
        print("----------------------------------------------------------------------")
        sys.exit()

    fbEmail = sys.argv[1]
    fbPassword = sys.argv[2]

    accessToken = get_fb_access_token(fbEmail, fbPassword)
    fbId = get_fb_id(accessToken)
    print(accessToken)
    print(fbId)
