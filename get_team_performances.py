import pandas as pd
import numpy as np
import requests
import re
import pickle
from bs4 import BeautifulSoup

import get_teams

sal_perc_df = pickle.load(open('payroll_shamsports.p', 'rb'))

performance_df = pd.DataFrame(np.ones((sal_perc_df.shape[0], 3), 
    dtype=np.float64), columns=['team', 'year', 'win_perc'])

# the year is (as per ShamSports) the ending year of the season,
# so the 2013-2014 season is under 2014
performance_df['team'] = sal_perc_df['team']
performance_df['year'] = sal_perc_df['year']
