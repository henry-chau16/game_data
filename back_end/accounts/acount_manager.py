from back_end.dal.dbfunctions import *
from back_end.dal.query_builder import *
import os
import hashlib

class AccountManager():
    def __init__(self, session: SQLsession):
        self.query = Query()
        self.session = session

    def createAccount(self, username, password):
        salt = self.generate_salt()
        hashed_password = self.encrypt(password, salt)
        command = f'INSERT INTO Accounts(Username, HashPassword, Salt) VALUES ("{username}", "{hashed_password}", "{salt}");'

        return self.session.sql_query(command)

    def searchAccountID(self, username):
        self.query.reset('all')
        command = (
            self.query
            .fields(['AccountID'])
            .source('Accounts')
            .where(f' Username = "{username}"')
            .build()
        )
        results = self.session.sql_query(command, fetchall=False)
        if not results:
            return None
        return results[0]

    def verifyLogin(self, username, password):
        self.query.reset('all')
        command = (
            self.query
            .fields(['HashPassword', 'Salt'])
            .source('Accounts')
            .where(f' Username = "{username}"')
            .build()
        )
        result = self.session.sql_query(command)

        if(result is not None and len(result) > 0):
            database_password = result[0][0]
            salt = result[0][1]
            hashed_password = self.encrypt(password, salt) #add in the salt from the database to compare
            
            if database_password == hashed_password:
                return True
        return False

    def generate_salt(self):
        return os.urandom(16).hex()

    def encrypt(self, password, salt):
        salted_password = password + salt
        hash_object = hashlib.sha256()
        hash_object.update(salted_password.encode())

        return hash_object.hexdigest()