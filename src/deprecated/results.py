'''
Created on Oct 5, 2018

@author: robert harrison
'''

import re

def foundInDiv(searchString, div):
    anchors = div.find_all('a', class_="team")
    if len(anchors) != 2:
        return False
    for a in anchors:
        try:
            if searchString.strip().lower() == a.text.strip().lower():
                return True
        except:
            print("error in method: results.foundInDiv")
    return False

def findWinnerInDiv(div):
    teams = list(div.find_all('a', class_="team"))
    scores = list(div.find_all('td', class_='total-score'))
    if len(scores) != 2:
        return ['not started', 0]
    status_elements = list(div.find('div', class_ = re.compile('game-status*')))
    try:
        status = status_elements[0].strip().lower()
        if 'final' in status:
            try:
                if int(scores[0].text) > int(scores[1].text):
                    return ['final', teams[0].text.strip().lower()]
                else:
                    return ['final', teams[1].text.strip().lower()]
            except ValueError:
                print("Text not a number")
                return ['error', -1]
        else:
            return ['in progress' , 0]
    except ValueError:
        #game is not over so just return
        return ["in progress", 0]
        
def findWinner(divs, team):
    if is_integer(team):
        #print('error message: ' + str(team) + " is not a valid team name.")
        return ['error', -2]
    team = formatTeam(team)
    for div in divs:
        if foundInDiv(team, div):
            return findWinnerInDiv(div)
    print(team + "needs to be standardized.")
    return ['error', -2]

#method to make team names standardized to match the cbs sports html
def formatTeam(team):
    if team.lower() == "vandy":
        team = "vanderbilt"
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
    return team

def findPointsForTieBreaker(divs):
    from pathlib import Path

    f = open('tie_break_teams.txt', 'r')
    lines = [line for line in f.readlines()]
    f.close()
    
    teamsList = lines[0].split('vs')
    team1 = teamsList[0]
    team2 = teamsList[1]
     
    for div in divs:
        if foundInDiv(team1, div):
            return findTotalPointsInDiv(div)
        elif foundInDiv(team2, div):
            return findTotalPointsInDiv(div)
    return -100

def findTotalPointsInDiv(div):
    scores = list(div.find_all('td', class_='total-score'))
    if(len(scores) == 0):
        return ['not started', 0]
    status_elements = list(div.find('div', class_ = re.compile('game-status*')))
    try:
        status = status_elements[0].strip().lower()
        totalPointsScored = int(scores[0].text) + int(scores[1].text)
        return [status, totalPointsScored]
    except ValueError:
            return ['text is not a number', 0]
            
def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#printTeamNames()
            