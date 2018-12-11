'''
Created on Nov 4, 2018

@author: robert harrison
'''

class Game(object):
    '''
    classdocs
    '''
    def __init__(self, column_id, game_id, teams, score, status, is_tb_game, start_time = 'add later'):
        self.column_id = column_id  #this id is used as a reference to the google sheet
        self.game_id = game_id
        self.teams = teams
        self.score = score
        self.status = status
        self.start_time = start_time
        self.is_tb_game = is_tb_game
        self.been_updated = False
        
    def get_winner(self):
        if self.score[0] > self.score[1]:
            return self.teams[0]
        else:
            return self.teams[1]
        