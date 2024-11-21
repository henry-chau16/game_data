from ..dal.dbfunctions import *
from ..dal.query_builder import *

class ReviewManager():
    def __init__(self, session: SQLsession):
        self.query = Query()
        self.session = session

    def getUserReviews(self, accountID):
        self.query.reset('all')
        command = (
            self.query
            .fields(['Title', 'Review'])
            .source('Reviews')
            .where(f'AccountID = {str(accountID)}')
            .build()
        )
        return(self.session.sql_query(command))

    def createReviews(self, title, review, accountID):
        command = f'INSERT INTO Reviews(Title, Review, AccountID) VALUES ("{title}", "{review}", "{str(accountID)}");'
        return(self.session.sql_query(command))

    def fetchReviews(self, title):
        self.query.reset('all')
        command = (
            self.query
            .fields(['Username', 'Review'])
            .source('Reviews', False,
                    add_join('Accounts', 'Reviews', 'AccountID', join_type = 'LEFT'))
            .where(f'Title = "{title}"')
            .build()
        )
        return self.session.sql_query(command)

    def updateReview(self, accountID, title, review):
        command = f'UPDATE Reviews SET Review = "{review}" WHERE AccountID = {str(accountID)} AND Title = "{title}";'
        return self.session.sql_query(command)

    def deleteReview(self, accountID, title):
        command = f'DELETE FROM Reviews WHERE AccountID = "{str(accountID)}" AND Title = "{title}";'
        return self.session.sql_query(command)