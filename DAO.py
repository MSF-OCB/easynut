# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from sqlite3.dbapi2 import paramstyle
from operator import itemgetter
from EasyDBObjects import *
from datetime import date
import datetime
import time
import csv
import os, re
import sqlite3
import shutil

class DAO(object):
    easydb_sqlitepath = os.getcwd() + '/easydb.sqlite'
    
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
        
    def getNextId(self, table_id, column_name):
        conn = sqlite3.connect(self.easydb_sqlitepath)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        sqlquery = 'SELECT MAX({}) FROM {}'
        params = [column_name, table_id]
        highestId = c.execute(sqlquery.format(*params)).fetchone()[0]
        c.close()
        conn.close()             
        return int(highestId) +1
    
    def generateExport(self):
        conn = sqlite3.connect(self.easydb_sqlitepath)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        for tablec in self.tables_config:
            with open(os.getcwd()+'/export/CSVFiles/'+tablec.name+'.csv', 'wb') as mycsv:
                wr = csv.writer(mycsv, quoting=csv.QUOTE_ALL)                
                columns = []
                sqlquery= 'SELECT '
                params = []
                for counter, field in enumerate(tablec.fields):
                    if counter == 0:
                        if field.type == field.field_type_date:
                            sqlquery = sqlquery + ' strftime("%m/%d/%Y", datetime({}, "unixepoch"))'
                        else:
                            sqlquery = sqlquery + ' {}' 
                    else:
                        if field.type == field.field_type_date:
                            sqlquery = sqlquery + ', strftime("%m/%d/%Y", datetime({}, "unixepoch"))'
                        else:
                            sqlquery = sqlquery + ', {}'
                    params.append(field.field_id)
                    columns.append(str(field.name))
                sqlquery = sqlquery + ' FROM {}'
                params.append(tablec.sql_table_config_name)
                wr.writerow(columns)
                for row in c.execute(sqlquery.format(*params)).fetchall():
                    wr.writerow(row)
        filename = 'EasyNutExport'+date.today().strftime('%d%b%Y')
        zipPath = os.getcwd()+'/export/'
        toZip = os.getcwd()+'/export/CSVFiles'
        for f in os.listdir(os.getcwd()+'/export/'):
            if re.search('^EasyNutExport([0-9a-zA-Z]+).zip', f):
                os.remove(os.path.join(os.getcwd()+'/export/', f))
        shutil.make_archive(zipPath + filename, 'zip', toZip)
        c.close()
        conn.close()   
        return zipPath + filename 
