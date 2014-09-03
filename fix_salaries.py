import pandas as pd
import numpy as np
import requests
import re
import pickle
from bs4 import BeautifulSoup

import get_teams

# now that we are doing performance data, we should straighten out 
# the whole teams issue.  the problem "rows" (teams that have changed) 
# location or team name in our sal_perc_df are anything with name 
# 'hornets', 'pelicans', 'thunder'


sal_perc_df = pickle.load(open('payroll_shamsports.p', 'rb'))
team_counts = [(sal_perc_df[sal_perc_df['team'] == t].shape[0], t) for t in list(set(sal_perc_df['team']))]

# from the team history page for each of those team names (team names)
# for the upcoming "2015" season, we have
#
# hornets: 
# 2015 - present    NBA     Charlotte Hornets
# 2005 - 2014       NBA     Charlotte Bobcats
# 1989 - 2002       NBA     Charlotte Hornets
# 
# pelicans:
# 2014 - present    NBA     New Orleans Pelicans
# 2006 - 2013       NBA     New Orleans Hornets
# 2006 - 2007       NBA     New Orleans/Oklahoma City Hornets
# 2003 - 2006       NBA     New Orleans Hornets
#
# thunder:
# 2009 - present    NBA     Oklahoma City Thunder
# 1968 - 2008       NBA     Seattle Supersonics

# this means that we need to retrieve the following salary data to make 
# our data frame 30 (number of teams) * 8 (number of seasons we have) 
# = 240 rows, and also label the team names as 'Charlotte Hornets'
# instead of just 'hornets' so our data frame will look more like:
# new_york_knicks         2007    x0
# new_orleans_pelicans    2014    x1
# new_orleans_hornets     2013    x2, etc.

# names of current teams
teams = ['_'.join(t.lower().split()) for t in get_teams.retrieve()]

ncol = 42
sal_perc_df_full = pd.DataFrame(np.ones((240, ncol), 
    dtype=np.float64), columns=['team', 'year'] + ['p' + str(i) for i in range(1,ncol - 1)]) 
