import pandas as pd
import numpy as np
import requests
import re
import pickle
from bs4 import BeautifulSoup
from sort_helper import uniquify

import get_teams

# load in the salary df just to pull the teams/years
sal_perc_df = pickle.load(open('fixed_payroll_shamsports.p', 'rb'))

performance_df = pd.DataFrame(np.ones((sal_perc_df.shape[0], 5), 
    dtype=np.float64), columns=['team', 'year', 'skew',
    'reg_season_wp', 'playoff_wp'])

# the year is (as per ShamSports) the ending year of the season,
# so the 2013-2014 season is under 2014
performance_df['team'] = sal_perc_df['team']
performance_df['year'] = sal_perc_df['year']
performance_df['skew'] = pickle.load(open('skews.p', 'rb'))

# the URLs to each team's info page on landofbasketball 
# will be alphabetical order -- let's sort our df as well.
# because the landofbasketball links will give data for each
# franchise, we need to order by current team, so we can do the
# following:

performance_df.team[performance_df.team == 'charlotte_bobcats'] = u'charlotte_hornets_charlotte_bobcats'
performance_df.team[performance_df.team == 'seattle_supersonics'] = u'oklahoma_city_thunder_seattle_supersonics'
performance_df.team[performance_df.team == 'oklahoma_city_thunder'] = u'oklahoma_city_z'
performance_df.team[performance_df.team == 'new_orleans_hornets'] = u'new_orleans_pelicans_new_orleans_hornets'
performance_df.team[performance_df.team == 'new_orleans_pelicans'] = u'new_orleans_pelicans_z'

s_perf_df = performance_df.sort(['team', 'year'], ascending=[True, False])

base = 'http://www.landofbasketball.com/'
url = base + 'nba_teams.htm'
r = requests.get(url)
soup = BeautifulSoup(r.text)

def isTeamURL(tag):
    return tag.name == 'a' and tag.string is not None and ''.join(tag.string.lower().split()) == 'yearlyrecords'

team_urls = [base + tag['href'] for tag in soup.findAll(isTeamURL)]


def isSeasonRow(tag):
    return tag.name == 'tr' and tag.td is not None and \
    tag.td.a is not None and tag.td.a.string is not None and \
    (re.search('[0-9]{4}-[0-9]{2}', tag.td.a.string) is not None)

# helper for finding the records after the season row
def isTd(tag):
    return tag.name == 'tr'

counter = 0
for url in team_urls:
    name_end = re.search('.htm', url).start()
    full_team = url[re.search('_', url).start() + 1:-4]
    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    # 0 index is the 2014-2015 season
    percs = soup.findAll(isSeasonRow)[1:9]
    for p in percs:
        tds = p.findAll('td')
        reg = float(tds[3].string)
        playoff = tds[7].string
        if playoff == '-':
            playoff = float('nan')
        s_perf_df.iat[counter, 3] = reg
        s_perf_df.iat[counter, 4] = playoff
        counter += 1
