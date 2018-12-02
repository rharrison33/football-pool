'''
Created on Oct 27, 2018

@author: rober
'''

from Sheet import Sheet
from Player import Player
from Game import Game
from src.make_picks import is_int

class Manager(object):
    '''
    classdocs
    '''


    def __init__(self, website, sheet_id):
        self.website = website
        self.sheet = Sheet(sheet_id)
        
    def get_players(self):
        rows = self.sheet.getValuesFromSheet("A2:Z99")
        player_list = []
        index = 1
        for row in rows:
            if len(row) == 0:
                break
            i = 0
            if len(row) == 1:
                index +=1
                continue
            for cell in row:
                i += 1
                if is_int(cell):
                    break
            player_list.append(Player(index, row[0], row[1:i]))
            index += 1
        return player_list
        
    def format_all_team_names(self):
        team_lists = self.sheet.getValuesFromSheet("B2:L99")
        for team_list in team_lists:
            if len(team_list) == 0:
                continue
            for team_name in team_list:
                if not team_name.strip():
                    continue
                self.website.get_game_attrs(team_name)
    
    def get_games(self):
        team_names = self.sheet.getValuesFromSheet("B2:L2")[0]
        game_list = []
        column_index = 1
        for team_name in team_names:
            if not team_name:
                continue
            game_attrs = self.website.get_game_attrs(team_name)
            game = Game(column_index, game_attrs[0], game_attrs[1], game_attrs[2], game_attrs[3], game_attrs[4])
            game_list.append(game)
            if game.is_tb_game:
                break
            column_index += 1
        return game_list
    
    def update_records(self, players, game):
        winner_row_index_list = []
        num_players = len(players)
        for player in players:
            if  not game.is_tb_game:
                for pick in player.picks:
                    if game.get_winner().lower() == self.website.formatTeam(pick.lower()):
                        player.record[0] += 1
                        winner_row_index_list.append(player.id)
                        break
                else:
                    player.record[1] += 1
            else:
                #is tb
                player.record[2] = abs((int)(game.score[0]) + (int)(game.score[1]) - (int)(player.tbpts))
        game.been_updated = True
        if not game.is_tb_game:
            if len(winner_row_index_list) == 0:
                print("Error updating game: " + game.teams[0] + ' vs ' + game.teams[1])
                raise Exception('Error updating game')
            self.sheet.color_winning_cells(winner_row_index_list, game.column_id)
            self.sheet.color_losing_cells(self.get_loser_index_list(winner_row_index_list, num_players), game.column_id)
        
    def get_loser_index_list(self, winner_row_index_list, num_players):
        loser_row_list = [False for i in range(num_players + 1)]
        for i in range(len(loser_row_list)):
            loser_row_list[i] = False if i in winner_row_index_list else True
        return [i for i, x in enumerate(loser_row_list) if x and i > 0]
        
    def update_sheet_winner(self, players):
        self.sheet.update_winner(players)    
        
    def update_sheet(self, players, game):
        self.update_records(players, game)
        self.sheet.update(players)  
        
    def add_column_headings_and_format(self, num_games):
        self.sheet.add_column_headings_and_format(num_games)   
        
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
        