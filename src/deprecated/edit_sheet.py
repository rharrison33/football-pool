'''
Created on Oct 7, 2018

@author: rober
'''
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import results
import os
import time
import datetime
import requests
from bs4 import BeautifulSoup
import re

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
URL = 'https://www.cbssports.com/college-football/scoreboard/'
#SPREADSHEET_ID = '1pUd8YEdkCUSG9WG3XrkYC1zw4e1o3LdUXluFarwr3mg'
SPREADSHEET_ID = '1Ui9DqzgqfhDGHrAWyHesGwT46SuuG-PLKGsAPAAog8U'

def updateHTML():
    #use the function to update divs
    try:
        print("updating html")
        page = requests.get(URL)
        soup = BeautifulSoup(page.text, 'lxml')
        divs = soup.find_all("div", id=re.compile("game-*"))
        return divs
    except:
        print('Connection Error. Check your internet connection.')
        minutes = 5 #how often to update sheet
        time.sleep(int(minutes * 60))
        updateHTML()
    
def updateSheetWithWinner(service):
    values = getValuesFromSheet(service, 'M2:M16')
    most_wins = 0
    
    #find the most wins
    for cell in values:
        wins = cell[0].split('-')[0]
        if int(wins) >= int(most_wins):
            most_wins = int(wins)
    
    #find index of best record(s) and add those to a list    
    index = 2
    winnersList = []
    
    #find the best record
    for cell in values:
        wins = cell[0].split('-')[0]
        if int(wins) == most_wins:
            winnersList.append(index)
        index += 1
    
    winnersNames = []
    if len(winnersList) == 1:
        #no need for tie breaker
        range_name = 'A' + str(winnersList[0])
        values = getValuesFromSheet(service, range_name)
        winnersNames.append(values[0])
    else:
        best_tb = 100 #initialize to something everyone will beat
        for index in winnersList:
            #go to tie breaker
            range_name = 'N' + str(index) + ':N' + str(index)
            values = getValuesFromSheet(service, range_name)
            this_tb = int(values[0][0])
            if this_tb <= best_tb:
                best_tb = this_tb
        #find index of best tb
        for index in winnersList:
            #go to tie breaker
            range_name = 'N' + str(index) + ':N' + str(index)
            values = getValuesFromSheet(service, range_name)
            if (int(values[0][0]) == best_tb):
                range_name = 'A' + str(index)
                values = getValuesFromSheet(service, range_name)
                winnersNames.append(values[0])
    #add names to sheet
    value_range_body = {
      "values": winnersNames
    }
    value_input_option = 'RAW'
    UPDATE_RANGE = "O2"
    service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, 
            range=UPDATE_RANGE, valueInputOption=value_input_option,
            body=value_range_body).execute()
    
def getValuesFromSheet(service, range_name):   
    RANGE_NAME = range_name
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME).execute()
    return result.get('values', []) 

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    values = getValuesFromSheet(service, 'B2:L16')
    
    #update column headings
    value_range_body = {
      "values": [["Record", "TB Diff", "Winner(s)"]]
    }
    
    value_input_option = 'RAW'
    UPDATE_RANGE = "M1:O1"
    request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=UPDATE_RANGE, valueInputOption=value_input_option, body=value_range_body)
    
    try:
        response = request.execute()
    except TimeoutError:
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=UPDATE_RANGE, valueInputOption=value_input_option, body=value_range_body)
        service = build('sheets', 'v4', http=creds.authorize(Http()))
        response = request.execute()
    
    # TODO: Change code below to process the `response` dict:
    print(response)
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'lxml')
    
    divs = soup.find_all("div", id=re.compile("game-*"))
    
    num_games = 10 #change for bowl season

    while True:
        players_results = []
        all_games_are_final = False
        tb_game_is_finished = False
        games_completed = 0
        divs = updateHTML()
        if divs != -1:
            tbgame_results = results.findPointsForTieBreaker(divs)
            tb_status = tbgame_results[0]
            if 'final' in tb_status:
                tb_game_is_finished = True
            tie_breaker_points = int(tbgame_results[1])
            for row in values:
                wins = 0
                player_results = ["a-b", -1]
                games_completed = 0
                for cell in row:
                    #winnerArray's first element is game status (final, in progress, or error)
                    #second element is winner name
                    if results.is_integer(cell):
                        player_results[1] = abs(tie_breaker_points - int(cell))
                    winnerArray = results.findWinner(divs, cell)
                    if winnerArray[0] == 'final':
                        games_completed += 1
                        winner = winnerArray[1]
                        pick = results.formatTeam(cell.lower())
                        if winner.strip().lower() == pick.strip().lower():
                            wins += 1
                if games_completed == num_games and tb_game_is_finished:
                    all_games_are_final = True
                player_results[0] = str(wins) + '-' + str(games_completed - wins)
                players_results.append(player_results)       
            
            value_range_body = {
              "values": players_results
            }
            
            value_input_option = 'RAW'
            
            UPDATE_RANGE = "M2:N16"
            request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=UPDATE_RANGE, valueInputOption=value_input_option, body=value_range_body)
            
            try:
                response = request.execute()
            except TimeoutError:
                store = file.Storage('token.json')
                creds = store.get()
                if not creds or creds.invalid:
                    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
                    creds = tools.run_flow(flow, store)
                request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=UPDATE_RANGE, valueInputOption=value_input_option, body=value_range_body)
                service = build('sheets', 'v4', http=creds.authorize(Http()))
                response = request.execute()
            
            # TODO: Change code below to process the `response` dict:
            print("Sheet was updated at " + str(datetime.datetime.now()))
            #print("    games completed: " + str(games_completed))
            #print(response)
            
            t = datetime.datetime.today()
            #print(str(t))
            #if t.hour >= 20 and t.minute > 45:
             #   print("Going to sleep at " + str(t.hour)
              #        +':' + str(t.minute))
               # time.sleep(10*3600)
            
            if all_games_are_final:
                updateSheetWithWinner(service)
                #break
        else:
            #connection error
            pass
                       
        minutes = 2 #how often to update sheet
        time.sleep(int(minutes * 60))
        #end loop. updates sheet every minutes
    
    #os.remove('token.json')
    exit()
    

if __name__ == '__main__':
    main()