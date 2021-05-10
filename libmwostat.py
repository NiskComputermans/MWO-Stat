#!/usr/bin/python3

# MwO Pilot Statistics Library
#   v0.1 (2021050701)
# (c) 2021 Kirk Stephenson
# E: nisk.is.afk@gmail.com
# W: github.com/NiskComputermans

import argparse
import requests
from bs4 import BeautifulSoup

pilots_file = "pilots.txt"

argparser = argparse.ArgumentParser()
argparser.add_argument('-u', dest='username', required=True)
argparser.add_argument('-p', dest='password', required=True)
argparser.add_argument('-f', dest='pilotfile', required=False, default=None)
argparser.add_argument('-s', dest='season', required=False, default=None)

args = argparser.parse_args()

mwo_username = args.username
mwo_password = args.password
mwo_season = args.season

pilot_stats = []

url = 'https://mwomercs.com/do/login'
post_data = { 'email': mwo_username, 'password': mwo_password }
  
sess = requests.Session()
ret = sess.post(url, data = post_data)

f = open(pilots_file, 'r')
mwo_pilots = f.read().splitlines()
f.close()

outputs = []

for mwo_pilot in mwo_pilots:
  url = 'https://mwomercs.com/profile/leaderboards?type=%i&user=%s' % (0, mwo_pilot)
  ret = sess.get(url)
  
  soup = BeautifulSoup(ret.text, 'html.parser')
  #print(soup)
  #exit()
  
  for row in soup('table')[0].findAll('tr'):
    column = row.findAll('td')
  
    if len(column) == 0:
      continue

    #print(column)
  
    pilot_name = column[1].string

    cooked_stats = {'Pilot': pilot_name, 'Season': mwo_season,
      'Light':{'Wins':0,'Losses':0,'Kills':0,'Deaths':0,'Games':0,'AvgScore':0},
      'Medium':{'Wins':0,'Losses':0,'Kills':0,'Deaths':0,'Games':0,'AvgScore':0},
      'Heavy':{'Wins':0,'Losses':0,'Kills':0,'Deaths':0,'Games':0,'AvgScore':0},
      'Assault':{'Wins':0,'Losses':0,'Kills':0,'Deaths':0,'Games':0,'AvgScore':0}
    }
  
    if pilot_name.lower() == mwo_pilot.lower():
      print('Name: %s\nSeason: %i\nRank: %i\nWins: %i\nLosses: %i\nWin/Loss Ratio: %f\nKills: %i\nDeaths: %i\nKill/Death Ratio: %f\nGames Played: %i\nAverage Score: %i\n' % (
        pilot_name,
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

      cooked_stats = {'Name': pilot_name, 'Season': mwo_season, 'Rank': int(column[0].string), 'Wins': int(column[2].string) }

      outputs.append(cooked_stats)
      break

print(outputs)
