import requests
from bs4 import BeautifulSoup

def is_team(tag):
    return tag.has_attr('class') and tag.name == 'a' and ('bi' in tag['class'])

def retrieve():
    url = 'http://espn.go.com/nba/teams'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    teams = [team_tag.string for team_tag in soup.find_all(is_team)]
    return teams