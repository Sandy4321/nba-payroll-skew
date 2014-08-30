import pandas as pd
import numpy as np
import pickle

sal_perc_df = pickle.load(open('payroll_shamsports.p', 'rb'))

# check that each row sums (approximately) to 1 to see that we didn't mess up a ton
better_equal_one = sal_perc_df.iloc[:, 2:].sum(axis=1)
print better_equal_one[better_equal_one != 1]
print sal_perc_df.iloc[195,:]

# looks like nuggets 2009 was a mess up that didn't give an error - after examining the actual page via browser, we see that due to more inconsistencies in the data display, all the percents are multiplied by 1000
sal_perc_df.iloc[195,2:] = sal_perc_df.iloc[195,2:] / 1000.

# for each row in sal_perc_df:
    # how many players with non-zero percentages = n

    # exactly equal % is 1 / n 

    # starpower stat is the sum of each percent's squared difference from the exactly equal %