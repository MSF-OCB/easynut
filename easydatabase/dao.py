from .field_config import FieldConfig
from .table_config import TableConfig

class DAO(object):
    easydb_sqlitepath = '/home/doudou/Documents/www/test.sqlite'
    
    def __init__(self, object_sqlitepath = easydb_sqlitepath):
        object_sqlitepath = object_sqlitepath
        tables_config = []
        tables_config_lite = {}
        search_results = []
        
    def set_tables_config(self):
        conn = sqlite3.connect(self.object_sqlitepath)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        sql_tables = 'select tabla_id, presentador from tablas'
        tables_config_lite = c.execute(sql_tables)
        for k,v in tables_config_lite:
            tablec = TableConfig()
            tablec.set_id(k)
            tablec.set_name(v)
            tablec.set_sql_names()
            sql_fields = 'select _id from ' + tablec.sql_table_config_name + ''
            fields = c.execute(sql_fields)
            for field_id in fields:
                fieldc = FieldConfig()
                for attributek, attributev in fieldc.attributes:
                    sql_field_config = 'select ' + attributek + ' from '+ tablec.sql_table_field_config_name + ' where _id = ' + field_id
                    function_name = 'set_' + attributev
                    fieldc.function_name(c.execute(sql_field_config))
                tablec.add_field(fieldc)
            self.tables_config.append(tablec)
        return
    
    def search(self, entry):
        conn = sqlite3.connect(self.object_sqlitepath)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        all_results = []
        for tablec in tables_config:
            sql_search_select = '_id'
            sql_search_where = ''
            results = [tablec.name]
            columns = ['ID']
            for fieldc in tablec.fields:
                if fieldc.list == True:
                    columns.append(fieldc.name)
                    sql_search_select = sql_search_select + ', ' + fieldc.field
                if sql_search_where == '':
                    sql_search_where = 'where (' + fieldc.field + ' like %' + entry + '%)'
                else:
                    sql_search_where = sql_search_where + ' or (' + fieldc.field + ' like %' + entry + '%)'
            sql_search = 'select ' + sql_search_select + ' from ' + tablec.sql_table_config_name + ' ' + sql_search_where + ' LIMIT 50'
            results.append(columns)
            results.append(c.execute(sql_search))
            all_results.append(results)
        return all_results
        
        
        
        
        