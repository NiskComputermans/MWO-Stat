#!/usr/bin/python3

# MwO Pilot Statistics Library - api test
#   v1.0 (2021052200)
# (c) 2021 Kirk Stephenson
# E: nisk.is.afk@gmail.com
# W: github.com/NiskComputermans
#
# Test script to hit the MWOMercs API.

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
