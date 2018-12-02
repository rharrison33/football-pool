'''
Created on Nov 4, 2018

@author: rober
'''

from pathlib import Path
import requests
from bs4 import BeautifulSoup
import re


class Website(object):
    '''
    classdocs
    '''

    def __init__(self, url):
        self.url = url
        self.soup = BeautifulSoup(requests.get(url).text, 'lxml')
        self.divs = self.soup.find_all("div", id=re.compile("game-*"))
        
    def get_game_attrs(self, team_name):
        is_tb_game = False
        if(is_int(team_name)):
            f = open('tie_break_teams.txt', 'r')
            lines = [line for line in f.readlines()]
            f.close()            
            teamsList = lines[0].split('vs')
            team_name = teamsList[0]
            is_tb_game = True
        team_name = self.formatTeam(team_name)
        for div in self.divs:
            anchors = div.find_all('a', class_="team")
            if len(anchors) != 2:
                return False
            for a in anchors:
                try:
                    if team_name.strip().lower() == a.text.strip().lower():
                        #found correct div
                        game_id = div['id']
                        divs_anchors = div.find_all('a', class_="team")
                        teams = [divs_anchors[0].text.strip().lower(),
                                 divs_anchors[1].text.strip().lower()]
                        score = [0, 0]
                        divs_status = div.find("div", class_=re.compile("game-status*"))
                        status = divs_status.text.strip().lower()
                        #start_time = add later on 
                        return [game_id, teams, score, status, is_tb_game]
                except:
                    print("error in method: website.get_game_id")
                    print('probably need to standardize name: ' + team_name)
                    print('or this team doesn\'t have a game this week.')
        
        print("error in method: website.get_game_id")
        print('probably need to standardize name: ' + team_name)
    
    def get_div(self, div_id):    
        div = self.soup.find("div", id=re.compile(div_id))
        return div
    
    def update_game(self, game):
        div = self.get_div(game.game_id)
        divs_status = div.find("div", class_=re.compile("game-status*"))
        game.status = divs_status.text.strip().lower()
        scores = list(div.find_all('td', class_='total-score'))
        if len(scores) == 2:
            game.score = [int(scores[0].text), int(scores[1].text)]
            
    def update_divs(self):
        self.soup = BeautifulSoup(requests.get(self.url).text, 'lxml')
        self.divs = self.soup.find_all("div", id=re.compile("game-*"))
    
    #method to make team names standardized to match the cbs sports html
    def formatTeam(self, team):
        if team.lower() == "vandy":
            team = "vanderbilt"
        if team.lower() == "fsu":
            team = "florida state"
        elif team.lower() == "uga":
            team = "georgia"
        elif team.lower() == "gt":
            team = "georgia tech"
        elif team.lower() == "wisc":
            team = "wisconsin"
        elif team.lower() == "s carolina":
            team = "south carolina"
        elif team.lower() == "iowa st":
            team = "iowa state"
        elif team.lower() == "w virginia":
            team = "west virginia"
        elif team.lower() == "ok state":
            team = "oklahoma state"
        elif team.lower() == "ok st":
            team = "oklahoma state"
        elif team.lower() == "k state":
            team = "kansas state"
        elif team.lower() == "wash":
            team = "washington"
        elif team.lower() == "wash st":
            team = "washington st."
        elif team.lower() == "ok":
            team = "oklahoma"
        elif team.lower() == "mich st":
            team = "michigan state"
        elif team.lower() == "minn":
            team = "minnesota"
        elif team.lower() == "miss st":
            team = "miss. state"
        elif team.lower() == "n texas":
            team = "north texas"
        elif team.lower() == "nc st":
            team = "nc state"
        elif team.lower() == "p state":
            team = "penn state"
        elif team.lower() == "tenn":
            team = "tennessee"
        elif team.lower() == "s florida":
            team = "south florida"
        elif team.lower() == "pitt":
            team = "pittsburgh"
        elif team.lower() == "miami":
            team = "miami (fl)"
        elif team.lower() == "bc":
            team = "boston college"
        elif team.lower() == "nd":
            team = "notre dame"
        elif team.lower() == "s miss":
            team = "southern miss"
        elif team.lower() == "v tech":
            team = "virginia tech"
        elif team.lower() == "af":
            team = "air force"
        elif team.lower() == "nw":
            team = "northwestern"
        elif team.lower() == "sc":
            team = "south carolina"
        elif team.lower() == "gata":
            team = "ga. southern"
        elif team.lower() == "ohio st":
            team = "ohio state"
        elif team.lower() == "t tech":
            team = "texas tech"
        elif team.lower() == "cali":
            team = "california"
        elif team.lower() == "vt":
            team = "virginia tech"
        elif team.lower() == "mizzou":
            team = "missouri"
        elif team.lower() == "az st":
            team = "arizona state"
        elif team.lower() == "cinci":
            team = "cincinnati"
        elif team.lower() == 'asu':
            team = 'arizona state'
        elif team.lower() == 'a&m':
            team = 'texas a&m'
        return team

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False