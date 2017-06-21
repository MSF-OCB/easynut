class FieldConfig(object):
    
    # Declare field types
    field_type_date = 0
    field_type_int = 1
    field_type_str = 2
    field_types = {
        'fecha' : field_type_date,
        'entero' : field_type_int,
        'texto' : field_type_str,
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
        'listado' : 'list',
        'detalle' : 'detail',
        'color' : 'color',
        'buscar' : 'find',
        'nuevaLinea' : 'new_line',
        'editable' : 'editable',
        'pos' : 'pos',
        'usar' : 'use',
        'relacionado' : 'relationship',
        }
    
    def __init__(self):
        id = 0
        field = ''
        field_id = ''
        name = ''
        type = field_types['texto']
        list = False
        detail = False
        color = 'Blanco'
        find = True
        new_line = True
        editable = True
        pos = 0
        use = True
        relationship = False
            
    def set_id(self, id):
        self.id = id
    
    def set_field(self, field):
        self.field = field
    
    def set_field_id(self, field_id):
        self.field_id = field_id        
    
    def set_name(self, name):
        self.name = name
    
    def set_type(self, type):
        self.type = field_types[type]
        
    def set_list(self, list):
        self.list = hasmapft[list]
    
    def set_detail(self, detail):
        self._detail = hasmapft[detail]
            
    def set_color(self, color):
        self.color = color

    def set_find(self, find):
        self.find = hasmapft[find]
    
    def set_new_line(self, new_line):
        self.new_line = hasmapft[new_line]
    
    def set_editable(self, editable):
        self.editable = hasmapft[editable]
        
    def set_pos(self, pos):
        self.pos = pos
            
    def set_use(self, use):
        self.use = hasmapft[use]
            
    def set_relationship(self, relationship):
        self.relationship = hasmapft[relationship]
