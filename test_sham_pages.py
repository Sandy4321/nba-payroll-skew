import pandas as pd
import numpy as np
import requests
import re
import pickle
from bs4 import BeautifulSoup

import get_teams

teams = get_teams.retrieve()

# salary data:
# http://hoopshype.com/salaries.htm
# http://hoopshype.com/salaries/golden_state.htm
# http://www.draftexpress.com/nba-player-salaries/year/2007/
# http://www.spotrac.com/nba/golden-state-warriors/yearly/

# http://data.shamsports.com/content/pages/data/salaries/2012/warriors.jsp

# 2d np array to store whether or not the given url (combo of the team "name"
# and the year)
base = 'http://data.shamsports.com/content/pages/data/salaries/'
years = range(2000, 2015)
x = np.ones((len(teams), len(years)), dtype=np.int)
test_url = [t.split()[-1].lower() for t in teams]

# if one of our rows is all 0s, that means the team url is actually wrong
i = 0
for tu in test_url:
    j = 0
    for year in years:
        url = base + str(year) + '/' + tu + '.jsp'
        r = requests.get(url)
        if r.status_code == 404:
            x[i, j] = 0 # mark it as a failed request
            print '404 for team "' + tu + '" and year ' + str(year)
        else:
            print 'URL valid for team "' + tu + '" and year ' + str(year)
        j += 1
    i += 1

df = pd.DataFrame(x, index=test_url, columns=years)
print df

# which rows are all zero? (teams that we got the wrong url for)
print df[(df.T == 0).all()]

# 76ers is wrong, let's try "sixers"
tu = u'sixers'
i = 3 ## << index of the sixers
j = 0
for year in years:
    url = base + str(year) + '/' + tu + '.jsp'
    r = requests.get(url)
    if r.status_code != 404:
        df.iloc[i, j] = 1 # score (jk Sixers don't know how to do that)
        print 'URL valid for team "' + tu + '" and year ' + str(year)
    else:
        print '404 for team "' + tu + '" and year ' + str(year)
    j += 1

test_url[3] = tu

# which columns are all zero?
print df.columns[(df == 0).all()]
# so the earliest the site has for any given year is 2007

df = df.loc[:, ~(df == 0).all()]

# we also have to watch for new/teams that switched aka the Pelicans
# (renamed from New Orleans Hornets)
# and the Hornets (renamed from Charlotte Bobcats)
# and the Brooklyn Nets ("renamed" from New Jersey Nets)
# and the Oklahoma City Thunder (renamed frmo the Seattle Supersonics)

pickle.dump(df, open('valid_pages.p', 'wb'))