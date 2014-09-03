import requests
import re
import pickle
from bs4 import BeautifulSoup

###################
# let's figure out how to scrape the salaries for a valid page
# this is an iterative process -- we will need to check if for every valid page 
# and we have a test break down their in the df-filler
# pretty hard task when the website is designed by some idiot with a <table> formatting
# and you have "$19,000,000ish" as a data point (knicks 2009)

# also when they decide to randomly not add a new <tr></tr> tag but still count it as row
# have to hardcode in mavericks 2008 
def is_salary_table(tag):
    return tag.name == 'table' and (tag.tr is not None) and \
    (all([(t.has_attr('class') and t['class'][0] == 'blue4') for 
        t in tag.tr.findAll('td')]))
def is_total_row(tag):
    return tag.name == 'tr' and (tag.td is not None) and (tag.td.string is not None) \
    and (re.sub(':', '', ''.join(tag.td.string.split()).lower()) == 'totalsalaries') 
    # classic "Total salaries" vs "Total Salaries" vs "Total Salaries:"
def is_player_row(tag):
    return tag.name == 'tr' and (tag.td is not None) and (tag.td.find('a') is not None) and \
    (len(tag.findAll('td')) >= 6)
def float_conv(s):
    if len(s) == 0:
        return 0
    return float(s)

# given the url to the shamsports.com site
def extractSalaryPercents(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    if url == 'http://data.shamsports.com/content/pages/data/salaries/2008/mavericks.jsp':
        tot = 106948621.
    elif url == 'http://data.shamsports.com/content/pages/data/salaries/2007/jazz.jsp':
        tot = 61310247.
    else:
        total_row = soup.find(is_total_row)
        totals = [float(re.sub(',', '', t.string[1:])) for t in total_row.findAll('b')[1:] if (t.string is not None)]
        tot = totals[0]

    sal_table = soup.findAll(is_salary_table)[0]
    player_rows = sal_table.findAll(is_player_row)
    sal_strings = [p.findAll('td')[1].string for p in player_rows]
    sal_strings = [s for s in sal_strings if s != 'N/A']
    sal_strings = [re.sub(r'[a-zA-Z]', '', s) for s in sal_strings]
    sals = [float_conv(re.sub(',', '', re.sub('\$', '', s))) for s in sal_strings]
    sal_percs = [sal / tot for sal in sals]
    return sal_percs