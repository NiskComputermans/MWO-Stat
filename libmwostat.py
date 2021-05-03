#!/usr/bin/python3

import argparse
import requests

argparser = argparse.ArgumentParser()
argparser.add_argument('-u', dest='username', required=True)
argparser.add_argument('-p', dest='password', required=True)

args = argparser.parse_args()

mwo_username = args.username
mwo_password = args.password
mwo_season = -1

try:
    url = 'https://mwomercs.com/do/login'
    post_data = { 'email': mwo_username, 'password': mwo_password }
    print(post_data)

    sess = requests.Session()
    ret = sess.post(url, data = post_data)
    print(ret.history)
    print(ret.headers)
    print(ret.status_code)
    print(ret.request)

    url = 'https://mwomercs.com/profile/leaderboards?type=%i&user=%s' % (0, 'Nisk')
    ret = sess.get(url)
    print(ret.history)
    print(ret.headers)
    print(ret.status_code)
    print(ret.request)
    print(ret.text)
except:
    print('Failed to login')
    exit()
