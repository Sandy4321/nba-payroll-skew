import pandas as pd
import numpy as np
import pickle

sal_perc_df = pickle.load(open('payroll_shamsports.p', 'rb'))

# check that each row sums (approximately) to 1 to see that we didn't mess up a ton
better_equal_one = sal_perc_df.iloc[:, 2:].sum(axis=1)
print better_equal_one[better_equal_one != 1]
print sal_perc_df.iloc[195,:]

# looks like nuggets 2009 was a mess up that didn't give an error - 
# after examining the actual page via browser, we see that due to 
# more inconsistencies in the data display, all the percents are 
# multiplied by 1000
sal_perc_df.iloc[195,2:] = sal_perc_df.iloc[195,2:] / 1000.

# skew array to be filled
skews = np.zeros(shape=(sal_perc_df.shape[0], 1))
for i in range(0, sal_perc_df.shape[0]):
    # subtract two for the team name and year
    n = float(sal_perc_df[i:i+1][sal_perc_df[i:i+1] != 0].transpose().count() - 2)
    eq = 1 / n
    these_sal = sal_perc_df.iloc[i, 2:]

    # filter out the zeroes before calculating starpower
    sp = sum(abs(these_sal[these_sal != 0] - eq))
    skews[i] = float(sp)

pickle.dump(skews, open('skews.p', 'wb'))