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

## Argument handling
#    This demo uses argparse to pull arguments from the command line.
argparser = argparse.ArgumentParser()
argparser.add_argument('-m', dest='matchid', required=True)
argparser.add_argument('-a', dest='apikey', required=True)

args = argparser.parse_args()

# Initialize a new instance of MWO Stat
stat = MWOStat()

# Turn on debugging output
stat.EnableDebug()

stat.SetAPIKey(mwo_api_key = args.apikey)

api_results = stat.GetAPIMatchStats(mwo_match_id = args.matchid)

print(type(api_results))
print(api_results)
