from dbfunctions import SQLsession, loadDB
import os

session = SQLsession('games.db')
session.connect()

game_data = os.getcwd()+'/games.csv'
loadDB(session, game_data, None)
print("done")