import pandas as pd
import numpy as np
import requests
import re
import pickle
from bs4 import BeautifulSoup

import get_teams

# load in the salary df just to pull the teams/years
sal_perc_df = pickle.load(open('payroll_shamsports.p', 'rb'))

performance_df = pd.DataFrame(np.ones((sal_perc_df.shape[0], 5), 
    dtype=np.float64), columns=['team', 'year', 'skew',
    'reg_season_wp', 'playoff_wp'])

# the year is (as per ShamSports) the ending year of the season,
# so the 2013-2014 season is under 2014
performance_df['team'] = sal_perc_df['team']
performance_df['year'] = sal_perc_df['year']
performance_df['skew'] = pickle.load(open('skews.p', 'rb'))

base = 'http://www.landofbasketball.com/'
url = base + 'nba_teams.htm'
r = requests.get(url)
soup = BeautifulSoup(r.text)

def isTeamURL(tag):
    return tag.name == 'a' and tag.string == 'Yearly Records'

team_urls = [base + tag['href'] for tag in soup.findAll(isTeamURL)]

def isRecordPerc(tag):
    return tag.name == 'td' and re.match('.[0-9][0-9][0-9]', tag.string)

for url in team_urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    name_end = re.search('.htm', url).start()
    full_team = url[re.search('_', url).start() + 1:]
    team = full_team[re.search('_', full_team).start() + 1 : re.search('.htm', full_team).start()]
    