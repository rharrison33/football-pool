'''
Created on Oct 27, 2018

@author: rober
'''

import time
from tracker_manager import Manager
from Website import Website
import random
  
    
    
if __name__ == '__main__':
    website = Website("https://www.cbssports.com/college-football/scoreboard/")
    manager = Manager(website, "1oBVJChfUCfxFvNkfdf79g6CU9pDGgYXMmRHAbxBJwpE")
    players = manager.get_players()
    manager.format_all_team_names()
    games_list = manager.get_games()
    manager.add_column_headings_and_format(len(games_list))
    games_completed = 0
    while(True):
        website.update_divs()
        for game in games_list:
            website.update_game(game)
            if('final' in game.status.lower() and not game.been_updated):
                print('updating game: ' + game.teams[0] +
                      ' vs ' + game.teams[1])
                games_completed += 1
                manager.update_sheet(players, game)
        if (games_completed == len(games_list)):
            break
        time.sleep(random.randint(120, 300))
    manager.update_sheet_winner(players)
    print('exiting program.')
    
    #while games_over < total_tracked_games:
        #update_state()
        



