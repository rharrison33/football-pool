'''
Created on Oct 7, 2018

@author: rober
'''
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import results
from results import findWinner
from _sqlite3 import Row
import os
import time
import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'


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

    # Call the Sheets API
    SPREADSHEET_ID = '1V6iT67la3kkXXJKZ6-tSyDuLGfB1Fg6BObHwvEQK_gM'
    RANGE_NAME = 'B2:L16'
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME).execute()
    values = result.get('values', [])
    
    #update column headings
    value_range_body = {
      "values": [["Wins", "TB Diff"]]
    }
    
    value_input_option = 'RAW'
    
    UPDATE_RANGE = "M1:N1"
    
    request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=UPDATE_RANGE, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()
    
    # TODO: Change code below to process the `response` dict:
    print(response)
    
    num_games = 10 #change for bowl season

    while True:
        players_results = []
        all_games_are_final = False
        games_completed = 0
        for row in values:
            wins = 0
            player_results = [0, -1]
            games_completed = 0
            for cell in row:
                try:
                    if int(cell) > 0:
                        player_results[1] = abs(results.findPointsForTieBreaker(cell) - int(cell))
                except ValueError:
                    #winnerArray's first element is game status (final, in progress, or error)
                    #second element is winner name
                    winnerArray = results.findWinner(cell)
                    if winnerArray[0] == 'final':
                        games_completed += 1
                        if winnerArray[1] == cell.lower():
                            wins += 1
            if games_completed == num_games:
                all_games_are_final = True
            player_results[0] = wins
            players_results.append(player_results)       
        
        value_range_body = {
          "values": players_results
        }
        
        value_input_option = 'RAW'
        
        UPDATE_RANGE = "M2:N16"
        
        request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=UPDATE_RANGE, valueInputOption=value_input_option, body=value_range_body)
        response = request.execute()
        
        # TODO: Change code below to process the `response` dict:
        print("Sheet was updated at " + str(datetime.datetime.now()))
        print("    games completed: " + str(games_completed))
        print(response)
        
        if all_games_are_final:
            print("exiting program.")
            exit()
                       
        minutes = 5 #how often to update sheet
        time.sleep(minutes*60)
        #end loop. updates sheet every minutes
    
    os.remove('token.json')
    

if __name__ == '__main__':
    main()