import requests
from bs4 import BeautifulSoup

def getTeamNames(anchors):
    if len(anchors) != 2:
        print("error: getTeamNames was passed a bad argument.")
    return [anchors[0].text.strip().lower(), anchors[1].text.strip().lower()]

def getSpread(spreadtd):
    stripped_strings = spreadtd.stripped_strings
    index = 0
    for string in stripped_strings:
        if string[0] == '-':
            return [index, string.split()[0]]
        index += 1
    return [0, '0']



page = requests.get("http://www.vegasinsider.com/college-football/odds/las-vegas/")
soup = BeautifulSoup(page.text, 'lxml')
trs = soup.find_all('tr')

#each row will contain 3 items, 2 team names, and a spread list
#spread list is index of favorite plus spread
games = []

count = 0
for tr in trs:
    tds = tr.find_all('td', limit = 2)
    anchors = tds[0].find_all('a')
    if len(anchors) == 2:
        if(anchors[0].text.strip().lower() == 'regular season'):
            continue
        if(anchors[0].text.strip().lower() == 'money line'):
            continue
        if(anchors[1].text.strip().lower() == 'picks'):
            continue
        spreadtd = tds[1];
        games.append(getTeamNames(anchors) + [getSpread(spreadtd)])
        count += 1
        if(count == 55):
            #only get the first 55 games
            break

#we now have all the important games
print(games)
    
