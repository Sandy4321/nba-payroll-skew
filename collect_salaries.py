import pandas as pd
import numpy as np

import collect_salaries_helper as cs

df = pickle.load(open('valid_pages.p', 'rb'))

base = 'http://data.shamsports.com/content/pages/data/salaries/'
for year in df.columns:
    url = base + str(year) + '/sixers.jsp'
    print extractSalaryPercents(url)

###################
# columns: team | year | player 1 salary percentage | player 2 salary percentage ...
# say that maximum of 40 players are being paid (should be ~ 12)
ncol = 42
sal_perc_df = pd.DataFrame(np.ones((df.values[df.values == 1].size, ncol), dtype=np.float64), columns=['team', 'year'] + ['p' + str(i) for i in range(1,41)])
rc = 0

# fill the salary df
scrape_bad = False
for i in range(0, df.shape[0]):
    for j in range(0, df.shape[1]):
        if df.iloc[i, j] == 1:
            sal_perc_df['team'][rc] = df.index[i]
            sal_perc_df['year'][rc] = df.columns[j]
            # scrape salary data
            url = base + str(df.columns[j]) + '/' + df.index[i] + '.jsp'
            try:
                sal_percs = cs.extractSalaryPercents(url)
            except:
                print 'Scraping error on url <' + url + '>'
                print 'Improve your extract function, you noob.'
                scrape_bad = True
                break
            sal_percs += [0] * ((ncol - 2) - len(sal_percs)) # pad the zeros
            sal_perc_df.iloc[rc, 2:] = sal_percs # fill that row in         
            rc += 1
            print 'Finished payroll for ' + df.index[i] + ', ' + str(df.columns[j])
        else:
            print 'Skipping 404 page'
    if scrape_bad:
        break   

pickle.dump(sal_perc_df, open('payroll_shamsports.p', 'wb'))
