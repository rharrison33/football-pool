'''
Created on Oct 28, 2018

@author: rober
'''
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import Http
import time
from email._header_value_parser import get_group_list

class Sheet(object):
    '''
    Represents a Google Sheets object
    '''
    
    
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        self.title = 'Pick Sheet 2' #input("Enter sheet title: ")
        SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('sheets', 'v4', http=creds.authorize(Http()))
    
    def update(self, players):
        player_records_list = []
        for player in players:
            player_records_list.append([str(player.record[0]) + '-' + str(player.record[1]), player.record[-1]])
            #print(player.name + "\'s record is " + str(player.record) )
        value_range_body = {
              "values": player_records_list
        }
        self.update_sheet("M2:N", value_range_body)
        
    def color_losing_cells(self, loser_index_list, col):
        for group in self.get_groupings(loser_index_list):
            self.set_bg_color_red(group[0], group[1], col)
        
    def color_winning_cells(self, winner_index_list, col):
        for group in self.get_groupings(winner_index_list):
            self.set_bg_color_green(group[0], group[1], col)
            
    def get_groupings(self, list):
        groupings = []
        i = 0
        endRow = -1
        while i < len(list):
            startRow = list[i]
            endRow = -1 #invalid
            j = 1
            while i + j < len(list) and list[i + j] - list[i + j - 1] == 1:
                j += 1
            endRow = startRow + j
            i = i + j
            groupings.append((startRow, endRow))
        
        if endRow == -1:
            groupings.append((startRow, startRow + 1))
            
        return groupings
            
    def set_bg_color_green(self, rowStart, rowEnd, col):  
        
        body = {
          "requests": [
            {
              "repeatCell": {
                "range": {
                  "startRowIndex": rowStart,
                  "endRowIndex": rowEnd,
                  "startColumnIndex": col,
                  "endColumnIndex": col + 1
                },
                "cell": {
                  "userEnteredFormat": {
                    "backgroundColor": {
                      "red": 0.0,
                      "green": 0.5,
                      "blue": 0.0
                    },
                    "horizontalAlignment" : "CENTER",
                    "textFormat": {
                      "foregroundColor": {
                        "red": 1.0,
                        "green": 1.0,
                        "blue": 1.0
                      },
                      "fontSize": 11,
                      "bold": True
                    }
                  }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
              }
            },
            {
              "updateSheetProperties": {
                "properties": {
                  "gridProperties": {
                    "frozenRowCount": 1
                  }
                },
                "fields": "gridProperties.frozenRowCount"
              }
            }
          ]
        }
        
        self.batch_update_sheet(body)
        
    def set_bg_color_red(self, row_start, row_end, col):  
        
        body = {
          "requests": [
            {
              "repeatCell": {
                "range": {
                  "startRowIndex": row_start,
                  "endRowIndex": row_end,
                  "startColumnIndex": col,
                  "endColumnIndex": col + 1
                },
                "cell": {
                  "userEnteredFormat": {
                    "backgroundColor": {
                      "red": 0.3,
                      "green": 0.0,
                      "blue": 0.0
                    },
                    "horizontalAlignment" : "CENTER",
                    "textFormat": {
                      "foregroundColor": {
                        "red": 1.0,
                        "green": 1.0,
                        "blue": 1.0
                      },
                      "fontSize": 10,
                      "bold": False
                    }
                  }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
              }
            },
            {
              "updateSheetProperties": {
                "properties": {
                  "gridProperties": {
                    "frozenRowCount": 1
                  }
                },
                "fields": "gridProperties.frozenRowCount"
              }
            }
          ]
        }
        
        self.batch_update_sheet(body)
        
    def update_winner(self, players):
        most_wins = 0
        for player in players:
            if player.record[0] > most_wins:
                most_wins = player.record[0]
        winners = self.get_winners(most_wins, players)
        if len(winners) == 1:
            value_range_body = {
                "values" : [winners]
            }
        else:
            value_range_body = {
                "majorDimension" : "Columns",
                "values" : [winners]
            }
        self.update_sheet("O2:O", value_range_body)
        
    def get_winners(self, most_wins, players):
        best_records = []
        for player in players:
            if player.record[0] == most_wins:
                best_records.append(player)
        winners = []
        if len(best_records) > 1:
            best_tb = 1000
            for player in best_records:
                if player.record[-1] < best_tb:
                    best_tb = player.record[-1]
            for player in best_records:
                if player.record[-1] == best_tb:
                    winners.append(player.name)
        else:
            winners.append(best_records[0].name)
        return winners
            
    def update_sheet(self, update_range, value_range_body, value_input_option = 'RAW'):        
        request = self.service.spreadsheets().values().update(spreadsheetId=self.sheet_id, 
                range=update_range, valueInputOption=value_input_option,
                body=value_range_body)
        self.execute(request)
    
    def getValuesFromSheet(self, range_name):   
        RANGE_NAME = range_name
        result = self.service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range=RANGE_NAME).execute()
        return result.get('values', []) 
    
    def add_column_headings_and_format(self, num_games):
        value_range_body = {
          "values": [["Record", "TB Diff", "Winner(s)"]]
        }
        start_column = chr(ord('B') + num_games)
        end_column = chr(ord(start_column) + 3)
        UPDATE_RANGE = start_column + "1:" + end_column +"1"
        self.update_sheet(UPDATE_RANGE, value_range_body)
        
        body = {
          "requests": [
            {
              "repeatCell": {
                "range": {
                  "startRowIndex": 0,
                  "endRowIndex": 1
                },
                "cell": {
                  "userEnteredFormat": {
                    "backgroundColor": {
                      "red": 0.0,
                      "green": 0.0,
                      "blue": 0.0
                    },
                    "horizontalAlignment" : "CENTER",
                    "textFormat": {
                      "foregroundColor": {
                        "red": 1.0,
                        "green": 1.0,
                        "blue": 1.0
                      },
                      "fontSize": 10,
                      "bold": True
                    }
                  }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
              }
            },
            {
              "updateSheetProperties": {
                "properties": {
                  "gridProperties": {
                    "frozenRowCount": 1
                  }
                },
                "fields": "gridProperties.frozenRowCount"
              }
            }
          ]
        }
        
        self.batch_update_sheet(body)
        
    def batch_update_sheet(self, body):
        request = self.service.spreadsheets().batchUpdate(
            spreadsheetId = self.sheet_id,
            body = body)
        return self.execute(request)
        
    def execute(self, request):
        try:
            request.execute()
        except HttpError as err:
            if err.resp['status'] == str(429):
                #exceeded quota so take a 5 min break
                print(err)
                print('Above error was caught. Now sleeping for 5 mins')
                time.sleep(5*60)
                self.execute(request)
            else:
                raise
    