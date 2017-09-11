# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class TableConfig(object):
    
    def __init__(self):
        self.id = 0
        self.name = ''
        self.fields = []
        self.sql_table_field_config_name = ''
        self.sql_table_config_name = ''
        
    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name
    
    def set_fields(self, fields):
        self.fields = fields
    
    def add_field(self, field):
        self.fields.append(field)
    
    def set_sql_names(self):
        self.sql_table_config_name = 'tabla_' + str(self.id)
        self.sql_table_field_config_name = self.sql_table_config_name + '_des'

    def printable_fields(self):
        return filter(lambda f: f.list, self.fields)

        
class FieldConfig(object):
    
    # Declare field types
    field_type_date = 0
    field_type_int = 1
    field_type_str = 2
    field_type_sel = 3
    field_type_not = 4
    field_type_rad = 5    
    field_types = {
        'fecha' : field_type_date,
        'entero' : field_type_int,
        'texto' : field_type_str,
        'select' : field_type_sel,    
        'notes' : field_type_not, 
        'radio': field_type_rad,            
        }
    
    # hash map false / true
    hasmapft = {
        'true' : True,
        'false' : False,
        '' : False,
        }
    
    # Dictionary of field'attributes to check in sql and related to here
    attributes = {
        '_id' : 'id',
        'campo' : 'field',
        'campo_id' : 'field_id',
        'presentador' : 'name',
        'tipo' : 'type',
        'varios' : 'select',        
        'listado' : 'list',
        'detalle' : 'detail',
        'buscar' : 'find',
        'nuevaLinea' : 'new_line',
        'editable' : 'editable',
        'pos' : 'pos',
        'usar' : 'use',
        'relacionado' : 'relationship',
        }
    
    def __init__(self):
        self.id = 0
        self.field = ''
        self.field_id = ''
        self.name = ''
        self.type = self.field_types['texto']
        self.list = False
        self.select = []
        self.detail = False
        self.color = 'Blanco'
        self.find = True
        self.new_line = True
        self.editable = True
        self.pos = 0
        self.use = True
        self.relationship = False
