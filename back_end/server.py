from dal import SQLsession, loadDB
import os

session = SQLsession('games.db')
session.connect()

game_data = 'games.csv'
account_data = 'accounts.csv'

loadDB(session, game_data, account_data) 
print("done")