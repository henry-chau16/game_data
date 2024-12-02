from back_end.dal import *
from back_end.accounts import * 
from back_end.gamedata import *



session = SQLsession()

game_data = 'games.csv'
account_data = 'accounts.csv'

loadDB(session, game_data, account_data) 
print("done")

