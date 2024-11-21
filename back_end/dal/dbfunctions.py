import sqlite3 as sq
import pandas as pd
import os

class SQLsession():
    
    def __init__(self, db_name, path = ''):
        self.db_name = db_name
        self.path = path
        self.conn = None

        self.tables = []
    
    def exists(self):
        path=os.getcwd()
        if self.db_name in os.listdir():
            return True
        return False
    
    def connect(self):
        try:
            self.conn = sq.connect(self.path+self.db_name, check_same_thread=False)
        except Exception as e:
            print(e)

    def close(self):
        try:
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print(e)
    
    def drop_table(self, table_name):
        try:
            cur=self.conn.cursor()
            cur.execute("DROP TABLE IF EXISTS "+table_name)
            print("-- deleting table: "+ table_name)
        except IOError:
                print("Error deleting: "+table_name)
                return -1
        return 0

    def create_table(self, table_name, columns, after_clause):
        try:
            cur = self.conn.cursor()
            self.drop_table(table_name)
            command = f'CREATE TABLE IF NOT EXISTS {table_name}({columns}) {after_clause}'
            print(command)
            cur.execute(command)
        except IOError:
            print("Error creating: "+table_name)
            return -1
        return 0

    def load_df(self, table_name, df: pd.DataFrame):
        try:
            df.to_sql(table_name, self.conn, if_exists='append', index=False)
        except Exception as e:
            print(e)

    def insert_row(self, table_name, columns, values):
        input = "INSERT INTO "+table_name+"("+columns+") VALUES ("+values+");"
        return self.sqlDML(self.conn, input)
    
    def deleteRow(self, table_name, field, value):
        input = "DELETE FROM "+table_name+" WHERE "+field +" = "+value+";"
        return self.sqlDML(self.conn, input)
    
    def updateRow(self, table_name, updateField, updateValue, field, value):
        input = "UPDATE "+table_name+" SET "+updateField+" = "+updateValue+ " WHERE "+field+" = "+value+";"
        return self.sqlDML(self.conn, input)

    def createTrigger(self, trigger_name, occurrence, dml_operation, table_name, statement): 
        input = "CREATE TRIGGER "+trigger_name+ " "+occurrence+" "+dml_operation + " ON " + table_name + " " +statement+";"
        return self.sqlDML(self.conn, input)

    def sqlDML(self, input):
        try:
            cur=self.conn.cursor()
            cur.execute(input)
            self.conn.commit()
        except IOError:
            print("Error processing query: "+ input)
            return -1
        return 0

    def sql_query(self, command):
        cur=self.conn.cursor()
        cur.execute(command)
        result=cur.fetchall()
        #print(result)
        self.conn.commit()
        return result
    
