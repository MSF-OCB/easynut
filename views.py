# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sqlite3
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from sqlite3.dbapi2 import paramstyle
from operator import itemgetter
import datetime
import time

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
    daoobject.set_tables_relationships()
    return render(request, template_name, {
        'record': daoobject.get_record_with_type(table_id, record_id), 
        'relatedrecords' : daoobject.get_related_records(table_id, record_id),
        })

def edit(request, table_id, record_id):
    template_name = 'emr/edit.html'
    daoobject = DAO()
    daoobject.set_tables_config()    
    return render(request, template_name, {'record': daoobject.get_record_with_type(table_id, record_id)})

def save(request):
    record_id = request.GET.get('record_id')
    table_id = request.GET.get('table_id')
    daoobject = DAO()
    daoobject.set_tables_config()
    fieldstochange = []
    for tablec in daoobject.tables_config:
        if tablec.id == table_id:
            for fieldc in tablec.fields:
               fieldstochange.append([fieldc.field_id, request.GET.get(fieldc.field_id), fieldc.type])
    if record_id != "0":
        daoobject.editrecord(table_id, record_id, fieldstochange)
    else:
        record_id = daoobject.insertrecord(table_id, fieldstochange)
    return detail(request, table_id, record_id)

def addrecord(request):
    template_name = 'emr/addrecord.html'
    table_id = request.GET.get('recordtable')
    related_record_entry = request.GET.get('related_record_entry')
    related_record_field = request.GET.get('related_record_field')
    daoobject = DAO()
    daoobject.set_tables_config()
    daoobject.set_tables_relationships()  
    if table_id != "0":
        return render(request, template_name, {
            'recordform': daoobject.getrecordform(table_id),
            'related_record_entry' : related_record_entry,
            'related_record_field' : related_record_field
            })
    return index(request)

def deleterecord(request, table_id, record_id):
    daoobject = DAO()
    daoobject.set_tables_config()
    daoobject.delete(table_id, record_id)
    return index(request)

class DAO(object):
    easydb_sqlitepath = '/home/doudou/Documents/www/test.sqlite'
    
    def __init__(self):
        self.tables_config = []
        self.tables_config_lite = {}
        self.tables_relationships = []
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
                    elif attributev == 'select':
                        selectlist = []
                        for tostrip in sqlresult.split(','):
                            selectlist.append(tostrip.strip())
                        setattr(fieldc, attributev, selectlist)
                    else:
                        setattr(fieldc, attributev, sqlresult)
                tablec.add_field(fieldc)
                del fieldc
            self.tables_config.append(tablec)
            del tablec
        c.close()
        conn.close()
        return
    
    def set_tables_relationships(self):
        conn = sqlite3.connect(self.easydb_sqlitepath)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        sqlquery = 'select tabla1_id, campo1_id, tabla2_id, campo2_id from tablas_relaciones'
        self.tables_relationships = c.execute(sqlquery).fetchall()
    
    def search(self, entry, tablesearch):
        conn = sqlite3.connect(self.easydb_sqlitepath)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        usersearch = [entry,]
        returnList = []
        all_results = []
        filtered_tables = []
        if tablesearch != '0':
            for tablec in self.tables_config:
                if tablec.id == tablesearch:
                    filtered_tables = [tablec,]
                    usersearch.append(tablec.name)
        else:
            filtered_tables = self.tables_config
            usersearch.append('all tables')
        returnList.append(usersearch)
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
        record = [table_id, record_id,]
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
                        fieldc.select,
                        ])
        record.append(sorted(recorddetails, key=itemgetter(2)))
        c.close()
        conn.close()
        return record
    
    def insertrecord(self, table_id, fieldstoadd):
        conn = sqlite3.connect(self.easydb_sqlitepath)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        sqlquery = 'INSERT INTO {}'
        sqlvalues = ' VALUES'
        params = []
        paramsvalues = []
        for tablec in self.tables_config:
            if tablec.id == table_id:
                params = [tablec.sql_table_config_name, ]
        for counter, field in enumerate(fieldstoadd):
            if counter == 0:
                sqlquery = sqlquery + ' ({}'
                sqlvalues = sqlvalues + ' ("{}"'
            elif counter == (len(fieldstoadd) -1):
                sqlquery = sqlquery + ', {})'
                sqlvalues = sqlvalues + ', "{}")'
            else:
                sqlquery = sqlquery + ', {}'
                sqlvalues = sqlvalues + ', "{}"'  
            params.append(field[0])            
            if field[2] == 0:
                paramsvalues.append(time.mktime(datetime.datetime.strptime(field[1], "%m/%d/%Y").timetuple()))
            else:
                paramsvalues.append(field[1])
        sqlcomplete = sqlquery + sqlvalues
        paramstotal = params + paramsvalues  
        c.execute(sqlcomplete.format(*paramstotal))
        conn.commit()
        record_id = c.lastrowid
        c.close()
        conn.close()
        return record_id
    
    def editrecord(self, table_id, record_id, fieldstochange):
        conn = sqlite3.connect(self.easydb_sqlitepath)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        sqlquery = 'UPDATE {} SET'
        for tablec in self.tables_config:
            if tablec.id == table_id:
                params = [tablec.sql_table_config_name, ]
        for counter, field in enumerate(fieldstochange):
            if counter == 0:
                sqlquery = sqlquery + ' {} = "{}"'
            else:
                sqlquery = sqlquery + ', {} = "{}"'
            params.append(field[0])
            if field[2] == 0:
                params.append(time.mktime(datetime.datetime.strptime(field[1], "%m/%d/%Y").timetuple()))
            else:
                params.append(field[1])            
        sqlquery = sqlquery + ' WHERE _id = {}'
        params.append(record_id)
        c.execute(sqlquery.format(*params))
        conn.commit()
        c.close()
        conn.close()
        return
               
    def getrecordform(self, table_id):
        recordform = []
        fields = []
        for tablec in self.tables_config:
            if tablec.id == table_id:
                recordform = [tablec.id, tablec.name,]
                for fieldc in tablec.fields:
                    fields.append([
                        fieldc.field_id, 
                        fieldc.type,
                        fieldc.pos,
                        fieldc.name, 
                        fieldc.select,                    
                        ])
        recordform.append(sorted(fields, key=itemgetter(2)))
        return recordform

    def delete(self, table_id, record_id):
        conn = sqlite3.connect(self.easydb_sqlitepath)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        sqlquery = 'DELETE FROM {} WHERE _id = {}'
        for tablec in self.tables_config:
            if tablec.id == table_id:
                params = [tablec.sql_table_config_name, record_id]
        c.execute(sqlquery.format(*params))
        conn.commit()
        c.close()
        conn.close()
        return
    
    def get_related_records(self, table_id, record_id):
        conn = sqlite3.connect(self.easydb_sqlitepath)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()        
        relatedrecords = []
        for relationship in self.tables_relationships:
            if (relationship[0] == table_id) or (relationship[2] == table_id):
                sqlquery = 'SELECT {} FROM {} WHERE _id = {}'
                if relationship[0] == table_id:
                    fieldtosearch = relationship[1]
                    relatedtable = relationship[2]
                    relatedfield = relationship[3]
                elif relationship[2] == table_id:       
                    fieldtosearch = relationship[3]
                    relatedtable = relationship[0]
                    relatedfield = relationship[1]                    
                for tablec in self.tables_config:
                    if tablec.id == table_id:
                        tabletosearch = tablec.sql_table_config_name
                params = [fieldtosearch, tabletosearch, record_id]
                relatedrecords.append((relatedfield, self.search(c.execute(sqlquery.format(*params)).fetchone()[0], relatedtable)))
        c.close()
        conn.close()
        return relatedrecords
                
                    
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
    field_type_sel = 3
    field_types = {
        'fecha' : field_type_date,
        'entero' : field_type_int,
        'texto' : field_type_str,
        'select' : field_type_sel,        
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
        self.select = []
        self.detail = False
        self.color = 'Blanco'
        self.find = True
        self.new_line = True
        self.editable = True
        self.pos = 0
        self.use = True
        self.relationship = False
        
