#!/usr/bin/python3

# MwO Pilot Statistics Library
#   v0.3 (2021051700)
# (c) 2021 Kirk Stephenson
# E: nisk.is.afk@gmail.com
# W: github.com/NiskComputermans
#
# Python 3 port of eta0h's MWO-Leaderboard-Stats (https://github.com/eta0h/MWO-Leaderboard-Stats)

import argparse
import requests
from bs4 import BeautifulSoup

pilots_file = "pilots.txt"

## ARGUMENT HANDLING
#
argparser = argparse.ArgumentParser()
argparser.add_argument('-u', dest='username', required=True)
argparser.add_argument('-p', dest='password', required=True)
argparser.add_argument('-f', dest='pilotfile', required=False, default=None)
argparser.add_argument('-s', dest='season', required=False, default='-1')

args = argparser.parse_args()

mwo_username = args.username
mwo_password = args.password
mwo_season = args.season

pilot_stats = []

# Read in pilots file.
f = open(pilots_file, 'r')
mwo_pilots = f.read().splitlines()
f.close()

## LOGIN
#
url = 'https://mwomercs.com/do/login'
post_data = { 'email': mwo_username, 'password': mwo_password }
  
sess = requests.Session()
ret = sess.post(url, data = post_data)

cookie_jar = requests.cookies.RequestsCookieJar()
cookie_jar.set('leaderboard_season', str(mwo_season), domain='.mwomercs.com', path='/')

outputs = []

for mwo_pilot in mwo_pilots:
  cooked_stats = {'Pilot': mwo_pilot, 'Season': mwo_season,
    'All':{'Wins':0,'Losses':0,'Kills':0,'Deaths':0,'Games Played':0,'Average Score':0},
    'Light':{'Wins':0,'Losses':0,'Kills':0,'Deaths':0,'Games Played':0,'Average Score':0},
    'Medium':{'Wins':0,'Losses':0,'Kills':0,'Deaths':0,'Games Played':0,'Average Score':0},
    'Heavy':{'Wins':0,'Losses':0,'Kills':0,'Deaths':0,'Games Played':0,'Average Score':0},
    'Assault':{'Wins':0,'Losses':0,'Kills':0,'Deaths':0,'Games Played':0,'Average Score':0}
  }
  
  for weight_class in ['All', 'Light', 'Medium', 'Heavy', 'Assault']:
    if weight_class == 'All': class_index = 0
    if weight_class == 'Light': class_index = 1
    if weight_class == 'Medium': class_index = 2
    if weight_class == 'Heavy': class_index = 3
    if weight_class == 'Assault': class_index = 4

    url = 'https://mwomercs.com/profile/leaderboards?type=%i&user=%s' % (class_index, mwo_pilot)
    sess.cookies.update(cookie_jar)
    ret = sess.get(url)
    
    soup = BeautifulSoup(ret.text, 'html.parser')
    
    for row in soup('table')[0].findAll('tr'):
      column = row.findAll('td')
    
      if len(column) == 0:
        continue
  
      pilot_name = column[1].string

      if pilot_name.lower() == mwo_pilot.lower():
        if pilot_name != cooked_stats['Pilot']:
          cooked_stats.update({'Pilot': pilot_name})

        class_stats = {weight_class:{'Wins': int(column[2].string), 'Losses': int(column[3].string), 'Kills': int(column[5].string), 'Deaths': int(column[6].string), 'Games Played': int(column[8].string), 'Average Score': int(column[9].string) }}
        cooked_stats.update(class_stats)
        break

  outputs.append(cooked_stats)
for line in outputs:
  for key in line:
    whitespace = ' ' *(10 - len(key))
    print("%s:%s%s" % (key, whitespace, line[key]))
