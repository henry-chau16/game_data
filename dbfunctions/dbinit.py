import sqlite3
import pandas as pd
from dbfunctions import SQLsession

def loadDB(session: SQLsession, games_data, accounts_data):
    print('starting')
    session.create_table('Games', 
                         ("Title TEXT PRIMARY KEY unique not null, "
                          "ReleaseDate TEXT, "
                          "Team TEXT, "
                          "Rating REAL, "
                          "Listed TEXT, "
                          "Reviews TEXT, "
                          "Genres TEXT, "
                          "Summary TEXT, "
                          "Playing TEXT"
                         ),
                          "WITHOUT ROWID")
    
    session.create_table('Reviews',
                         ("Title TEXT not null, "
                          "Review Text not null, "
                          "FOREIGN KEY (Title) REFERENCES Games(Title)"
                         ),
                          "")
    
    games_db = pd.read_csv(games_data)
    games_db = games_db.drop_duplicates(subset=['Title'], keep='first')

    games_db = games_db.iloc[:,1:]
    games_db.drop(columns=['Plays', 'Backlogs', 'Wishlist'], inplace=True)

    reviews_db = pd.DataFrame(columns=['Title', 'Review'])

    for index, row in games_db.iterrows():
        title = row['Title']
        reviews = row['Reviews'].replace('[', '').replace(']', '').split(", '")
        for review in reviews:
            reviews_db = pd.concat([reviews_db, pd.DataFrame({'Title': [title], 'Review': [review]})], ignore_index=True)

    games_db.drop(columns=['Reviews'], inplace=True)
    games_db.rename(columns={'Release Date': 'ReleaseDate', 'Times Listed': 'Listed', 
                             'Number of Reviews': 'Reviews'}, inplace=True)
    

    print(games_db.dtypes)
    session.load_df('Games', games_db)
    session.load_df('Reviews', reviews_db)