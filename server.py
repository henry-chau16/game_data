from back_end.dal import *
from back_end.accounts import * 
from back_end.gamedata import *



session = SQLsession()
#session.connect()
"""
game_data = 'games.csv'
account_data = 'accounts.csv'

loadDB(session, game_data, account_data) 
#print("done")
"""

search = SearchEngine(session)
accounts = AccountManager(session)
reviews = ReviewManager(session)

print(search.filter(reset = False, Rating = '>= 4').search('Title', 'Animal', 'TEXT'))
search.filter(reset=True)
print(search.search('Title', 'Animal', 'TEXT', ['Rating']))
