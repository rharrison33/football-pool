'''
Created on Oct 5, 2018

Module for parsing html.

@author: robert harrison
'''

import requests
from bs4 import BeautifulSoup

page = requests.get("http://www.vegasinsider.com/college-football/odds/offshore/")
soup = BeautifulSoup(page.text, 'lxml')

def find_favorite(team1, team2, stringsList):
    index = find_index(team1, stringsList)
    if index == -1:
        index = find_index(team2, stringsList)
        if index == -1:
            #both teams not found
            return -1
    
    #find the '-' and do some magic 
    if stringsList[index + 1][0] == '-':
        return stringsList[index - 2]
    if stringsList[index + 2][0] == '-':
        return stringsList[index]
    if stringsList[index + 3][0] == '-':
        return stringsList[index]
    if stringsList[index + 4][0] == '-':
        return stringsList[index + 2] 
    

def find_TBpoints(team1, team2, stringsList):
    index = find_index(team1, stringsList)
    if index == -1:
        index = find_index(team2, stringsList)
        if index == -1:
            #both teams not found
            return -1
    
    try:
        tbPoints = int(stringsList[index + 3][0:2])
        if tbPoints > 0:
            return tbPoints
    except ValueError:
        pass
    try:
        tbPoints = int(stringsList[index + 4][0:2])
        if tbPoints > 0:
            return tbPoints
    except ValueError:
        pass
    
def find_index(team, stringsList):
    if team.lower() == "vandy":
        team = "vanderbilt"
    elif team.lower() == "uga":
        team = "georgia"
    index = 0
    for string in stringsList:
        if team.lower() == string.lower():
            return index
        index+=1
    return -1 #string not found

stringsList = list(soup.stripped_strings)
#print(find_favorite("Missouri","South Carolina", stringsList))


from pathlib import Path

f = open(Path("C:/Users/rober/Desktop/picks.txt"), 'r')
lines = [line for line in f.readlines()]
f.close()

findTBpoints = False
count = 0
for line in lines:
    tokens = line.split("vs")
    if len(tokens) > 1 and not findTBpoints:
        #find faborite mode
        print(find_favorite(tokens[0].strip(), tokens[1].strip(), stringsList))
        count += 1
        continue
    #tb points mode  
    if len(tokens) > 1 and findTBpoints:
        print(find_TBpoints(tokens[0].strip(), tokens[1].strip(), stringsList))
    else:
        findTBpoints = True
print("Picks made: " + str(count))