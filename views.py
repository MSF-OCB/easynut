# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sqlite3
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from .models import Choice, Question
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from sqlite3.dbapi2 import paramstyle
from operator import itemgetter

def index(request):
    template_name = 'emr/index.html'
    daoobject = DAO()
    daoobject.set_tables_config()
    return render(request, template_name, {'edbtables': daoobject.tables_config_lite})

def results(request):
    search_query = request.GET.get('searchstring')
    tablesearch = request.GET.get('tablesearch')
    template_name = 'emr/results.html'
    daoobject = DAO()
    daoobject.set_tables_config()
    return render(request, template_name, {'searchresults': daoobject.search(search_query, tablesearch)})

def detail(request, table_id, record_id):
    template_name = 'emr/detail.html'
    daoobject = DAO()
    daoobject.set_tables_config()    
    return render(request, template_name, {'record': daoobject.get_record_with_type(table_id, record_id)})

def edit(request, table_id, record_id):
    template_name = 'emr/edit.html'
    daoobject = DAO()
    daoobject.set_tables_config()    
    return render(request, template_name, {'record': daoobject.get_record_with_type(table_id, record_id)})

class DAO(object):
    easydb_sqlitepath = '/home/doudou/Documents/www/test.sqlite'
    
    def __init__(self):
        #object_sqlitepath = object_sqlitepath
        self.tables_config = []
        self.tables_config_lite = {}
        self.search_results = []
        
    def set_tables_config(self):
        conn = sqlite3.connect(self.easydb_sqlitepath)
        conn.row_factory = sqlite3.Row
        conn.text_factory = str
        c = conn.cursor()
        sql_tables = 'select tabla_id, presentador from tablas'
        self.tables_config_lite = c.execute(sql_tables).fetchall()
        for k,v in self.tables_config_lite:
            tablec = TableConfig()
            tablec.set_id(k)
            tablec.set_name(v)
            tablec.set_sql_names()
            sql_fields = 'SELECT _id FROM %s'
            params = (tablec.sql_table_field_config_name,)
            fields = c.execute(sql_fields % params)
            for field_id in fields.fetchall():
                fieldc = FieldConfig()
                for attributek, attributev in fieldc.attributes.items():
                    sql_field_config = 'select %s from %s where _id = %s'
                    params = (attributek, tablec.sql_table_field_config_name, field_id[0],)
                    sqlresult = c.execute(sql_field_config % params).fetchone()[0]
                    if sqlresult in fieldc.hasmapft.keys():
                        setattr(fieldc, attributev, fieldc.hasmapft[sqlresult])
                    elif sqlresult in fieldc.field_types.keys():
                        setattr(fieldc, attributev, fieldc.field_types[sqlresult])
                    else:
                        setattr(fieldc, attributev, sqlresult)
                tablec.add_field(fieldc)
                del fieldc
            self.tables_config.append(tablec)
            del tablec
        c.close()
        conn.close()
        return
    
    def search(self, entry, tablesearch):
        conn = sqlite3.connect(self.easydb_sqlitepath)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        returnList = [entry,]
        all_results = []
        filtered_tables = []
        if tablesearch != '0':
            for tablec in self.tables_config:
                if tablec.id == tablesearch:
                    filtered_tables = [tablec,]
        else:
            filtered_tables = self.tables_config
        for tablec in filtered_tables:
            sql_search_select = "select {}"
            params = ['_id']
            paramswhere = []
            sql_search_where = ' from {} where '
            results = [tablec.name, tablec.id]
            columns = []
            for fieldc in tablec.fields:
                if fieldc.list == True:
                    if fieldc.type == fieldc.field_type_date:
                        columns.append(fieldc.name + ' (mm/dd/yyyy)')
                        sql_search_select = sql_search_select + ", strftime('%m/%d/%Y', datetime({}, 'unixepoch'))"
                    else:
                        columns.append(fieldc.name)
                        sql_search_select = sql_search_select + ", {}"
                    params.append(fieldc.field)
                if sql_search_where == ' from {} where ':
                    sql_search_where = sql_search_where + '({} like {})'
                else:
                    sql_search_where = sql_search_where + ' or ({} like {})'
                paramswhere.append(fieldc.field)
                paramswhere.append('"%{}%"'.format(entry))
            params.append(tablec.sql_table_config_name)
            params.extend(paramswhere)
            sql_search = sql_search_select + sql_search_where + ' LIMIT 50'
            results.append(columns)
            results.append(c.execute(sql_search.format(*params)).fetchall())
            all_results.append(results)
        returnList.append(all_results)
        c.close()
        conn.close()
        return returnList
                
    def get_record_with_type(self, table_id, record_id):
        conn = sqlite3.connect(self.easydb_sqlitepath)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        record = []
        recorddetails = []
        for tablec in self.tables_config:
            if tablec.id == table_id:
                record.append(tablec.name)
                for fieldc in tablec.fields:
                    if fieldc.type == fieldc.field_type_date:
                        sqlquery = "select strftime('%m/%d/%Y', datetime({}, 'unixepoch')) from {} where _id = {}"
                    else:
                        sqlquery = 'select {} from {} where _id = {}'
                    params = [fieldc.field, tablec.sql_table_config_name, record_id]
                    recorddetails.append([
                        fieldc.field_id, 
                        fieldc.type,
                        fieldc.pos,
                        fieldc.name, 
                        c.execute(sqlquery.format(*params)).fetchone()[0],
                        ])
        record.append(sorted(recorddetails, key=itemgetter(2)))
        c.close()
        conn.close()
        return record
                    
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
        self.id = 0
        self.field = ''
        self.field_id = ''
        self.name = ''
        self.type = self.field_types['texto']
        self.list = False
        self.detail = False
        self.color = 'Blanco'
        self.find = True
        self.new_line = True
        self.editable = True
        self.pos = 0
        self.use = True
        self.relationship = False
        
