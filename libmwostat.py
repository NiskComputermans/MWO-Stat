#!/usr/bin/python3

import argparse
import requests
from bs4 import BeautifulSoup

argparser = argparse.ArgumentParser()
argparser.add_argument('-u', dest='username', required=True)
argparser.add_argument('-p', dest='password', required=True)
argparser.add_argument('-P', dest='pilot', required=False)
argparser.add_argument('-s', dest='season', required=False)

args = argparser.parse_args()

mwo_username = args.username
mwo_password = args.password
mwo_pilot = args.pilot
mwo_season = -1

url = 'https://mwomercs.com/do/login'
post_data = { 'email': mwo_username, 'password': mwo_password }

sess = requests.Session()
ret = sess.post(url, data = post_data)

url = 'https://mwomercs.com/profile/leaderboards?type=%i&user=%s' % (0, mwo_pilot)
ret = sess.get(url)

soup = BeautifulSoup(ret.text, 'html.parser')
#print(soup.find('table'))

for row in soup('table')[0].findAll('tr'):
  column = row.findAll('td')

  if len(column) == 0:
    continue

  pilot_name = column[1].string

  if pilot_name == mwo_pilot:
    print('Season: %i\nRank: %i\nWins: %i\nLosses: %i\nWin/Loss Ratio: %f\nKills: %i\nDeaths: %i\nKill/Death Ratio: %f\nGames Played: %i\nAverage Score: %i\n' % (
    -1,
    int(column[0].string),
    int(column[2].string),
    int(column[3].string),
    float(column[4].string),
    int(column[5].string),
    int(column[6].string),
    float(column[7].string),
    int(column[8].string),
    int(column[9].string)))
    break
