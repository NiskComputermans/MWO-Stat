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
  ## Class initialization
  #    Anything which should be initialized before use should be set to its initial values here.
  def __init__(self):
    self.pilots = []
    self.mwo_url = 'https://mwomercs.com/do/login'

    self.sess = None
    self.cookie_jar = None

    self.debug_on = False

  ## Debug mode
  #    This function enables the debug flag. When debugging is on, some tests will print output to screen.
  #    Debug mode is equivalent to running most programs with the -v flag.
  def EnableDebug(self):
    self.debug_on = True

  ## Pilot import
  #    This function takes a file or list of pilot names and populates the internal pilots list.
  #    The internal list is then used for further queries against the website.
  def ImportPilots(self, pilot_file=None, pilot_list=None):
    if pilot_file is not None:
      if pilot_list is not None:
        return("ERR: Use either pilots file or pilot list.")

      f = open(pilot_file, 'r')
      self.pilots = f.read().splitlines()
      f.close()

    elif pilot_list is not None:
      if type(pilot_list) != list:
        return("ERR: pilot_list must be a list of case insensitive strings which match pilot names.")

      self.pilots = pilot_list

    else:
      return("ERR: No pilot file or list has been specified.")

  ## Login to mwomercs.com
  #    This function is used to login to mwomercs.com with a user account. Logging in is required to scrape
  #    the leaderboard on the website. The leaderboard functions will not work without logging in first.
  def Login(self, mwo_username=None, mwo_password=None):
    self.post_data = { 'email': mwo_username, 'password': mwo_password }

    url = 'https://mwomercs.com/do/login'

    self.sess = requests.Session()
    ret = self.sess.post(url, data = self.post_data)

    if self.debug_on:
      print("MWO login return code: %s" % (ret))

  ## Get first season on the leaderboard
  #    The website does not host every season back to season zero. This function scrapes the season picker
  #    from the leaderboards to get the number of the first available season.
  def GetFirstSeason(self):
    if self.sess is None:
      return("ERR: Invalid session. Must log on to MWO by running Login before scraping stats!")

    url = 'https://mwomercs.com/profile/leaderboards?type=%i&user=%s' % (0, "Nisk")
    ret = self.sess.get(url)

    soup = BeautifulSoup(ret.text, 'html.parser')

    first_season = int(list(soup.find('select', id="season").stripped_strings)[0].split(" ")[1])

    return first_season

  ## Get latest season on the leaderboard
  #    This function scrapes the season picker from the leaderboards to gete the number of the most recent
  #    season. Note that the most recent season is the live season and stats for it will change up until
  #    the start of the next season.
  def GetLatestSeason(self):
    if self.sess is None:
      return("ERR: Invalid session. Must log on to MWO by running Login before scraping stats!")

    url = 'https://mwomercs.com/profile/leaderboards?type=%i&user=%s' % (0, "Nisk")
    ret = self.sess.get(url)

    soup = BeautifulSoup(ret.text, 'html.parser')

    latest_season = int(list(soup.find('select', id="season").stripped_strings)[-1].split(" ")[1])

    return latest_season

  ## Get leaderboard statistics
  #    This function scrapes leaderboard statistics for each pilot in the internal pilots list, broken down
  #    by weight class. If a season is not specified, the current season will be picked. Iterating over
  #    this function season by season will generate a list of all data for the pilots list per season.
  def GetLeaderboardStats(self, mwo_season=-1):
    if self.sess is None:
      return("ERR: Invalid session. Must log on to MWO by running Login before scraping stats!")
    if len(self.pilots) == 0:
      return("ERR: No pilots list loaded. Run ImportPilots before scraping stats!")

    if int(mwo_season) == -1:
      mwo_season = self.GetLatestSeason()

      if self.debug_on:
        print("No season specified, using season %s" % (mwo_season))

    first_season = self.GetFirstSeason()

    if int(mwo_season) < first_season:
      if self.debug_on:
        print("Season %s is not available on mwo website, using earliest available season (%s)" % (mwo_season, first_season))
      mwo_season = first_season

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
