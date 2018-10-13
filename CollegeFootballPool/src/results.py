'''
Created on Oct 5, 2018

@author: robert harrison
'''

import requests
from bs4 import BeautifulSoup
import re

page = requests.get("https://www.cbssports.com/college-football/scoreboard/")
soup = BeautifulSoup(page.text, 'lxml')

divs = soup.find_all("div", id=re.compile("game-*"))

def foundInDiv(searchString, div):
    anchors = div.find_all('a', class_="team")
    for a in anchors:
        if searchString.lower() == a.text.strip().lower():
            return True
    return False

def findWinnerInDiv(div):
    teams = list(div.find_all('a', class_="team"))
    scores = list(div.find_all('td', class_='total-score'))
    status_elements = list(div.find('div', class_ = re.compile('game-status*')))
    try:
        if status_elements[0].text.strip().lower() == 'final':
            try:
                if int(scores[0].text) > int(scores[1].text):
                    return teams[0].text.strip().lower()
                else:
                    return teams[1].text.strip().lower()
            except ValueError:
                print("Text not a number")
    except AttributeError:
        #game is not over so just return
        pass
        
def findWinner(team):
    for div in divs:
        if foundInDiv(team, div):
            return findWinnerInDiv(div)
    return False

def findPointsForTieBreaker(team):
    for div in divs:
        if foundInDiv(team, div):
            return findTotalPointsInDiv(div)
    return -1

def findTotalPointsInDiv(div):
    scores = list(div.find_all('td', class_='total-score'))
    if(len(scores) == 0):
        return 0
    try:
        totalPointsScored = int(scores[0].text) + int(scores[1].text)
        return totalPointsScored
    except ValueError:
        print("Text not a number")
        
def printTeamNames():
    for div in divs:
        anchors = div.find_all('a', class_="team")
        for a in anchors:
            print(a.text.strip().lower())

#printTeamNames()
            