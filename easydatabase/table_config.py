class TableConfig(object):
    
    def __init__(self):
        self.id = 0
        self.name = ''
        self.fields = []
        sql_table_field_config_name = ''
        sql_table_config_name = ''
        
    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name
    
    def set_fields(self, fields):
        self.fields = fields
    
    def add_field(self, field):
        self.fields.append(field)
    
    def set_sql_names(self):
        sql_table_config_name = 'tabla_' + self.id
        sql_table_field_config_name = sql_table_config_name + '_des'