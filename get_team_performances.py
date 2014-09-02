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

def isSeasonRow(tag):
    return tag.name == 'tr' and tag.td is not None and \
    tag.td.a is not None and tag.td.a.string is not None and \
    (re.search('[0-9]{4}-[0-9]{2}', tag.td.a.string) is not None)

# helper for finding the records after the season row
def isTd(tag):
    return tag.name == 'tr'

for url in team_urls:
    name_end = re.search('.htm', url).start()
    full_team = url[re.search('_', url).start() + 1:]
    team_name = full_team[re.search('_', full_team).start() + 1 : re.search('.htm', full_team).start()]
    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    # 0 index is the 2014-2015 season
    percs = soup.findAll(isSeasonRow)[1:9]

    inds = performance_df[performance_df['team'] == team_name].index
    counter = 0
    for p in percs:
        tds = p.findAll('td')
        reg = float(tds[3].string)
        playoff = tds[7].string
        if playoff == '-':
            playoff = float('nan')
        performance_df.iat[inds[counter], 3] = reg
        performance_df.iat[inds[counter], 4] = playoff
        counter += 1

# realized that we have like only one row for charlotte but current
# method doesn't find the specific year, just fills in 07-14