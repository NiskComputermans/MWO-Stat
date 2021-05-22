# MWO-Stat

To use the library, import it into your Python 3 project and create a new instance of the MWOStat class
```python
from libmwostat import MWOStat

stat = MWOStat()
```

## Website leaderboard scraping

To scrape the website, create a pilots file to import (or pass an array of pilots), create a login session on mwomercs.com with the Login function, then use GetLeaderboardStats to pull down the match stats for your list of pilots.
```python
# Import pilots from file
stat.ImportPilots(pilot_file = "pilots.txt")

# Login to mwomercs.com
stat.Login(mwo_username = args.username, mwo_password = args.password)

# Grab leaderboard stats for the selected season
leaderboard = stat.GetLeaderboardStats(mwo_season = args.season)
```

```python
# Import pilots from array
stat.ImportPilots(pilot_list = ['ArJuna', 'Guillocuda', 'Kamikaze Viking', 'Nisk', 'ResidentCloakingCommie'])

# Login to mwomercs.com
stat.Login(mwo_username = "JRandomMechWarrior", mwo_password = "correcthorsebatterystaple")

# Grab leaderboard stats for the selected season
leaderboard = stat.GetLeaderboardStats(mwo_season = args.season)
```

Results will be returned in a python list containing a dictionary for each pilot. If the results are zeroes for each field, the name of the pilot is misspelled or they have not been recorded playing in the season you specified.
```python
[{'Pilot': 'ArJuna', 'Season': 58, 'All': {'Wins': 146, 'Losses': 100, 'Kills': 246, 'Deaths': 153, 'Games Played': 246, 'Average Score': 274}, 'Light': {'Wins': 0, 'Losses': 0, 'Kills': 0, 'Deaths': 0, 'Games Played': 0, 'Average Score': 0}, 'Medium': {'Wins': 0, 'Losses': 0, 'Kills': 0, 'Deaths': 0, 'Games Played': 0, 'Average Score': 0}, 'Heavy': {'Wins': 120, 'Losses': 84, 'Kills': 196, 'Deaths': 128, 'Games Played': 204, 'Average Score': 272}, 'Assault': {'Wins': 26, 'Losses': 16, 'Kills': 50, 'Deaths': 25, 'Games Played': 42, 'Average Score': 283}}, {'Pilot': 'Guillocuda', 'Season': 58, 'All': {'Wins': 117, 'Losses': 66, 'Kills': 262, 'Deaths': 96, 'Games Played': 183, 'Average Score': 394}, 'Light': {'Wins': 0, 'Losses': 0, 'Kills': 0, 'Deaths': 0, 'Games Played': 0, 'Average Score': 0}, 'Medium': {'Wins': 13, 'Losses': 10, 'Kills': 16, 'Deaths': 14, 'Games Played': 23, 'Average Score': 340}, 'Heavy': {'Wins': 45, 'Losses': 21, 'Kills': 86, 'Deaths': 32, 'Games Played': 66, 'Average Score': 364}, 'Assault': {'Wins': 59, 'Losses': 35, 'Kills': 160, 'Deaths': 50, 'Games Played': 94, 'Average Score': 429}}, {'Pilot': 'Kamikaze Viking', 'Season': 58, 'All': {'Wins': 29, 'Losses': 29, 'Kills': 47, 'Deaths': 48, 'Games Played': 59, 'Average Score': 287}, 'Light': {'Wins': 0, 'Losses': 0, 'Kills': 0, 'Deaths': 0, 'Games Played': 0, 'Average Score': 0}, 'Medium': {'Wins': 10, 'Losses': 9, 'Kills': 14, 'Deaths': 15, 'Games Played': 20, 'Average Score': 261}, 'Heavy': {'Wins': 11, 'Losses': 11, 'Kills': 20, 'Deaths': 20, 'Games Played': 22, 'Average Score': 284}, 'Assault': {'Wins': 6, 'Losses': 7, 'Kills': 8, 'Deaths': 10, 'Games Played': 13, 'Average Score': 323}}, {'Pilot': 'Nisk', 'Season': 58, 'All': {'Wins': 142, 'Losses': 72, 'Kills': 300, 'Deaths': 108, 'Games Played': 214, 'Average Score': 301}, 'Light': {'Wins': 0, 'Losses': 0, 'Kills': 0, 'Deaths': 0, 'Games Played': 0, 'Average Score': 0}, 'Medium': {'Wins': 8, 'Losses': 9, 'Kills': 15, 'Deaths': 10, 'Games Played': 17, 'Average Score': 264}, 'Heavy': {'Wins': 126, 'Losses': 61, 'Kills': 272, 'Deaths': 94, 'Games Played': 187, 'Average Score': 302}, 'Assault': {'Wins': 0, 'Losses': 0, 'Kills': 0, 'Deaths': 0, 'Games Played': 0, 'Average Score': 0}}, {'Pilot': 'ResidentCloakingCommie', 'Season': 58, 'All': {'Wins': 106, 'Losses': 65, 'Kills': 163, 'Deaths': 104, 'Games Played': 171, 'Average Score': 245}, 'Light': {'Wins': 0, 'Losses': 0, 'Kills': 0, 'Deaths': 0, 'Games Played': 0, 'Average Score': 0}, 'Medium': {'Wins': 0, 'Losses': 0, 'Kills': 0, 'Deaths': 0, 'Games Played': 0, 'Average Score': 0}, 'Heavy': {'Wins': 61, 'Losses': 31, 'Kills': 96, 'Deaths': 56, 'Games Played': 92, 'Average Score': 250}, 'Assault': {'Wins': 43, 'Losses': 31, 'Kills': 64, 'Deaths': 43, 'Games Played': 74, 'Average Score': 247}}]
```

Cleaned up the data looks something more like this:
```python
Pilot:     Nisk
Season:    58
All:       {'Wins': 142, 'Losses': 72, 'Kills': 300, 'Deaths': 108, 'Games Played': 214, 'Average Score': 301}
Light:     {'Wins': 0, 'Losses': 0, 'Kills': 0, 'Deaths': 0, 'Games Played': 0, 'Average Score': 0}
Medium:    {'Wins': 8, 'Losses': 9, 'Kills': 15, 'Deaths': 10, 'Games Played': 17, 'Average Score': 264}
Heavy:     {'Wins': 126, 'Losses': 61, 'Kills': 272, 'Deaths': 94, 'Games Played': 187, 'Average Score': 302}
Assault:   {'Wins': 0, 'Losses': 0, 'Kills': 0, 'Deaths': 0, 'Games Played': 0, 'Average Score': 0}
```

## API queries

API queries are a simple wrapper around the example query on the [MWO api page of your mwomercs.com profile](https://mwomercs.com/profile/api).

To pull data from the API, set your API key, then query the API with the GetAPIMatchStats function.
```python
# Set API key for use with mwomercs.com. This does not require logging in to the website.
stat.SetAPIKey(mwo_api_key = args.apikey)

# Query the API for private match results.
api_results = stat.GetAPIMatchStats(mwo_match_id = args.matchid)
```

Data returned is passed through in the same format the web API presents it.
```python
{'MatchDetails': {'Map': 'SteinerColiseum', 'ViewMode': 'FirstPersonOnly', 'TimeOfDay': 'Random', 'GameMode': 'Skirmish', 'Region': 'Oceanic', 'MatchTimeMinutes': '15', 'UseStockLoadout': False, 'NoMechQuirks': False, 'NoMechEfficiencies': False, 'WinningTeam': '1', 'Team1Score': 1, 'Team2Score': 0, 'MatchDuration': '100', 'CompleteTime': '2021-05-22T09:21:21+00:00'}, 'UserDetails': [{'Username': 'ResidentCloakingCommie', 'IsSpectator': False, 'Team': '2', 'Lance': '1', 'MechItemID': 318, 'MechName': 'tbr-cc', 'SkillTier': 4, 'HealthPercentage': 0, 'Kills': 0, 'KillsMostDamage': 0, 'Assists': 0, 'ComponentsDestroyed': 0, 'MatchScore': 134, 'Damage': 279, 'TeamDamage': 0, 'UnitTag': ''}, {'Username': 'Nisk', 'IsSpectator': False, 'Team': '1', 'Lance': '1', 'MechItemID': 165, 'MechName': 'tbr-s', 'SkillTier': 3, 'HealthPercentage': 64, 'Kills': 1, 'KillsMostDamage': 1, 'Assists': 0, 'ComponentsDestroyed': 3, 'MatchScore': 228, 'Damage': 388, 'TeamDamage': 0, 'UnitTag': 'ISRC'}]}
```

## Acknowledgements

This library was based on [eta0h's Python 2.7 leaderboard stats library](https://github.com/eta0h/MWO-Leaderboard-Stats). It was originally intended to be a simple Python 3 port, but has slowly grown out to where I think this could be a useful tool for the community in its own right.
