#!/usr/bin/python3

# MwO Pilot Statistics Library
#   v0.4 (2021052200)
# (c) 2021 Kirk Stephenson
# E: nisk.is.afk@gmail.com
# W: github.com/NiskComputermans
#
# Python 3 port of eta0h's MWO-Leaderboard-Stats (https://github.com/eta0h/MWO-Leaderboard-Stats)

import requests
from bs4 import BeautifulSoup

class MWOStat:
  def __init__(self):
    self.pilots = []
    self.mwo_url = 'https://mwomercs.com/do/login'

    self.sess = None
    self.cookie_jar = None

    self.debug_on = False

  def EnableDebug(self):
    self.debug_on = True

  def ImportPilots(self, pilot_file=None, pilot_list=None):
    if pilot_file is not None:
      if pilot_list is not None:
        return("ERR: Use either pilots file or pilot list.")

      f = open(pilot_file, 'r')
      self.pilots = f.read().splitlines()
      f.close()

    elif pilot_list is not None:
      self.pilots = pilot_list

    else:
      return("ERR: No pilot file or list has been specified.")

  def Login(self, mwo_username=None, mwo_password=None):
    self.post_data = { 'email': mwo_username, 'password': mwo_password }

    url = 'https://mwomercs.com/do/login'

    self.sess = requests.Session()
    ret = self.sess.post(url, data = self.post_data)

    if self.debug_on:
      print("MWO login return code: %s" % (ret))

  def GetLeaderboardStats(self, mwo_season=-1):
    if self.sess is None:
      return("ERR: Invalid session. Must log on to MWO by running Login before scraping stats!")
    if len(self.pilots) == 0:
      return("ERR: No pilots list loaded. Run ImportPilots before scraping stats!")

    if int(mwo_season) == -1:
      url = 'https://mwomercs.com/profile/leaderboards?type=%i&user=%s' % (0, "Nisk")
      ret = self.sess.get(url)

      soup = BeautifulSoup(ret.text, 'html.parser')

      mwo_season = int(list(soup.find('select', id="season").stripped_strings)[-1].split(" ")[1])

      if self.debug_on:
        print("No season specified, using season %s" % (mwo_season))

    self.cookie_jar = requests.cookies.RequestsCookieJar()
    self.cookie_jar.set('leaderboard_season', str(mwo_season), domain='.mwomercs.com', path='/')

    outputs = []

    for mwo_pilot in self.pilots:
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
        self.sess.cookies.update(self.cookie_jar)
        ret = self.sess.get(url)

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

    return(outputs)
