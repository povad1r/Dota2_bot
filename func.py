import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from keyboards.game_choice import limit
url = 'https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches'

source = requests.get(url)
def convert_to_eest(date):
    date_format = datetime.strptime(date, '%B %d, %Y - %H:%M %Z')
    date_result = date_format + timedelta(hours=3)
    result = date_result.strftime('%B %d, %Y - %H:%M %Z')
    return result
def get_content(limit):
    source = requests.get(url)
    soup = BeautifulSoup(source.content, 'html.parser')
    exact_time = soup.find_all('span', class_="timer-object timer-object-countdown-only")
    left_team = soup.find_all('td', class_="team-left")
    right_team = soup.find_all('td', class_="team-right")
    tournament = soup.find_all('td', class_="match-filler")
    score = soup.find_all('td', class_="versus")
    matches = []
    for i in range(limit):
        exactly = convert_to_eest(exact_time[i].text)
        # team_1 = left_team[i].find('a')['title'].split('(')
        # team_2 = right_team[i].find('a')['title'].split('(')
        team_2 = right_team[i].find('a')
        if team_2 is not None:
            team_2 = team_2['title'].split('(')
        else:
            team_2 = ['TBD']
        team_1 = left_team[i].find('a')
        if team_1 is not None:
            team_1 = team_1['title'].split('(')
        else:
            team_1 = ['TBD']

        tourn = tournament[i].find('a')['title']
        scoreq = score[i].find('div').text.strip()
        date = exactly.split(',')[0]
        match = {
            'time': exactly,
            'team_1': team_1[0],
            'team_2': team_2[0],
            'tournament': tourn,
            'score': scoreq,
            'date': date
        }
        if match not in matches:
            matches.append(match)
    return matches
get_content(limit)

def get_tournament():
    content = get_content(50)
    Tournaments = []
    for match in content:
        Tournament = match['tournament']
        if Tournament not in Tournaments:
            Tournaments.append(Tournament) 
    return Tournaments
get_tournament()

def get_date():
    content = get_content(50)
    Dates = []
    for match in content:
        Date = match['date']
        if Date not in Dates:
            Dates.append(Date) 
    return Dates
get_tournament()