#!/usr/bin/python3

# MwO Pilot Statistics Library
#   v0.4 (2021052200)
# (c) 2021 Kirk Stephenson
# E: nisk.is.afk@gmail.com
# W: github.com/NiskComputermans
#
# Python 3 port of eta0h's MWO-Leaderboard-Stats (https://github.com/eta0h/MWO-Leaderboard-Stats)

from libmwostat import MWOStat
import argparse

## ARGUMENT HANDLING
#
argparser = argparse.ArgumentParser()
argparser.add_argument('-u', dest='username', required=True)
argparser.add_argument('-p', dest='password', required=True)
argparser.add_argument('-f', dest='pilotfile', required=False, default='pilots.txt')
argparser.add_argument('-s', dest='season', required=False, default=-1)

args = argparser.parse_args()

# Initialize a new instance of MWO Stat
stat = MWOStat()

# Turn on debugging output
stat.EnableDebug()

# Import pilots from file
stat.ImportPilots(pilot_file = args.pilotfile)

# Login to mwomercs.com
stat.Login(mwo_username = args.username, mwo_password = args.password)

# Grab leaderboard stats for the selected season
leaderboard = stat.GetLeaderboardStats(mwo_season = args.season)

for line in leaderboard:
  for key in line:
    whitespace = ' ' *(10 - len(key))
    print('%s:%s%s' % (key, whitespace, line[key]))
