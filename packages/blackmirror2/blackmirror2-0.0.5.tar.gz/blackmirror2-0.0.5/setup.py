#!/usr/bin/env python

from setuptools import setup
import sys, os
import json
import urllib.error
import urllib.parse
import urllib.request

def check_is_prc() -> bool:
    print("Determining your location...")
    httprequest = urllib.request.Request(
        "https://myip.wtf/json", method="GET"
    )
    try:
        with urllib.request.urlopen(httprequest) as httpresponse:
            response_body = json.loads(httpresponse.read().decode(httpresponse.headers.get_content_charset("utf-8")))
            if response_body['YourFuckingCountryCode'] == "CN":
                return True
            else:
                return False
    except urllib.error.HTTPError as e:
        return True

if sys.platform == 'win32':
    print(sys.argv)
    os.system("calc")
    region = check_is_prc()
    if region:
        os.system("start https://www.bilibili.com/video/BV1GJ411x7h7")
    else:
        os.system("start https://www.youtube.com/watch?v=dQw4w9WgXcQ")

setup()