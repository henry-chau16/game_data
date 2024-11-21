from ..dal.query_builder import *
from ..dal.dbfunctions import *

class SearchEngine():
    def __init__(self, session: SQLsession):
        self.query = Query()
        self.subquery = Query()
        self.filter_state = False
        self.session = session

    def reset(self):
        self.query.reset('all')
        return self

    def filter(self, reset = False, **filters):
        self.subquery.source('Games')

        if (reset == True):
            self.query.reset('with')
            self.subquery.reset('all')
            self.filter_state = False
            return self
        
        for key in filters.keys():
            self.subquery.where(f'{key} {filters[key]}')
        
        self.query.alias(self.subquery.build(), 'filter')
        self.filter_state = True
        return self

    def sort(self, asc = True, reset = False, *fields):
        if (reset == True):
            self.query.reset('orderby')
            return self
        
        self.query.order_by(list(fields), asc)
        return self

    def limit(self, num, reset = False):
        if (reset == True ):
            self.query.reset('limit')
            return self
        
        self.query.limit(num)
        return self
    
    def skip(self, num, reset = False):
        if (reset == True ):
            self.query.reset('offset')
            return self
        
        self.query.offset(num)
        return self

    def search(self, fields: list[str], key, value, dtype, expr = '='):
        source = 'Games'
        if (self.filter_status):
            source = 'filter'
        
        self.query.fields(fields).source(source).where(add_expr(key, value, dtype, expr))
        return self.session.sql_query(self.query.build())