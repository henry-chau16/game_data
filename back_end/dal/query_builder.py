def add_expr(key, value, dtype = 'TEXT', expr = '=', cond = ''):
    if(dtype == 'INTEGER' or dtype == 'REAL'):
        val = str(value)
    else:
        val = f'"{value}"'
    return f'{cond} {key} {expr} {val} '

def add_join(right, left, on, join_type = ''):
    if (join_type != ''):
        join_type += ' '
    return f'{join_type}JOIN {right} ON {left}.{on} = {right}.{on} '

class Query():
    def __init__(self):
        self.command = {
            'with': None,
            'fields': 'SELECT * ',
            'source': None,
            'where': None,
            'groupby': None,
            'having': None,
            'orderby': None,
            'limit': None,
            'offset': None
        }
        

    def build(self):
        string = ''
        for key in self.command.keys():
            if (self.command[key] != None):
                string += self.command[key]
        return string

    def reset(self, clause):
        if (clause == 'all'):
            self.command = {
                'with': None,
                'fields': 'SELECT * ',
                'source': None,
                'where': None,
                'groupby': None,
                'having': None,
                'orderby': None,
                'limit': None,
                'offset': None
            }
        elif (clause == 'field'):
            self.command.update({clause: 'SELECT * '})
        else:
            self.command.update({clause: None})
        return self
    
    def alias(self, query: str, alias: str):
        self.command.update({'with': f'WITH {alias} AS ({query}) '})
        return self

    def fields(self, fields: list[str], distinct: bool = False):
        tag = ''
        fields_str = ', '.join(fields)
        if (distinct == True):
            tag = "DISTINCT "
        self.command.update({'fields': f'SELECT {tag}{fields_str} '})
        return self

    def source(self, source, subquery: bool = False, *joins):
        if (subquery):
            source = f'({source})'
        self.command.update({'source': f'FROM {source} '+''.join(joins)})
        return self

    def where(self, *args):
        if (self.command['where'] == None):
            self.command.update({'where': 'WHERE'})
        self.command['where']+= ''.join(args)
        return self
    
    def group_by(self, fields: list[str]):
        fields_str = ', '.join(fields)
        self.command.update({'groupby': f'GROUP BY {fields_str} '})
        return self
    
    def having(self, *args):
        if (self.command['having'] == None):
            self.command.update({'having': 'HAVING'})
        self.command['having']+= ''.join(args)
        return self

    def order_by(self, fields: list[str], asc = True):
        tag = ''
        if (asc == False): tag = 'DESC'
        fields_str = ', '.join(fields)
        self.command.update({'orderby': f'ORDER BY {fields_str} {tag} '})
        return self

    def limit(self, num):
        self.command.update({'limit': f'LIMIT {num} '})
        return self

    def offset(self, num):
        self.command.update({'offset': f'OFFSET {num}'})
        return self
