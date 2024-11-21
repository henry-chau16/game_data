from back_end.dal.query_builder import *
from back_end.dal.dbfunctions import *

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
        filter_list = []
        for key in filters.keys():
            filter_list.append(f' {key} {filters[key]}')
        vals = ' AND'.join(filter_list)
        self.subquery.where(vals)
        with_clause = self.subquery.build()
        self.query.alias(with_clause, 'filter')
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

    def search(self, key, value, dtype = 'TEXT', fields: list[str] = ['*'], expr = 'LIKE'):
        self.query.reset('where')
        source = 'Games'
        val = value
        if (self.filter_state):
            source = 'filter'
        
        if (expr == 'LIKE'):
            val = f'%{value}%'

        self.query.fields(fields).source(source).where(add_expr(key, val, dtype, expr))
        print(self.query.build())
        return self.session.sql_query(self.query.build())