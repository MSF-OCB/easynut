# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from django.utils import timezone
from operator import itemgetter
from EasyDBObjects import *
from datetime import date
from django.conf import settings
import MySQLdb
import datetime
import time
import csv
import os, re
import shutil
from MySQLdb import converters


class DAO(object):

    def __init__(self):
        self.tables_config = []
        self.tables_config_lite = {}
        self.tables_relationships = []
        self.easy_user = []
        
        conv=converters.conversions.copy()
        conv[246]=float    # convert decimals to floats
        conv[10]=str       # convert dates
        self.db = MySQLdb.connect(settings.DATABASES['data']['HOST'],
                                  settings.DATABASES['data']['USER'],
                                  settings.DATABASES['data']['PASSWORD'],
                                  settings.DATABASES['data']['NAME'], conv=conv)
        
    def set_tables_config(self):
        c = self.db.cursor()
        sql_tables = 'select tabla_id, presentador from tablas'
        c.execute(sql_tables)
        self.tables_config_lite = c.fetchall()
        for k,v in self.tables_config_lite:
            tablec = TableConfig()
            tablec.set_id(k)
            tablec.set_name(v)
            tablec.set_sql_names()
            sql_fields = 'SELECT _id FROM {}'
            params = (tablec.sql_table_field_config_name,)
            c.execute(sql_fields.format(*params))
            for field_id in c.fetchall():
                fieldc = FieldConfig()
                for attributek, attributev in fieldc.attributes.items():
                    sql_field_config = 'select {} from {} where _id = {}'
                    params = (attributek, tablec.sql_table_field_config_name, field_id[0],)
                    c.execute(sql_field_config.format(*params))
                    sqlresult = c.fetchone()[0]
                    if sqlresult in fieldc.hasmapft.keys():
                        setattr(fieldc, attributev, fieldc.hasmapft[sqlresult])
                    elif sqlresult in fieldc.field_types.keys():
                        setattr(fieldc, attributev, fieldc.field_types[sqlresult])
                    elif attributev == 'select':
                        selectlist = []
                        if sqlresult is not None:
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
        return
    
    def set_tables_relationships(self):
        c = self.db.cursor()
        sqlquery = 'select tabla1_id, campo1_id, tabla2_id, campo2_id from tablas_relaciones' 
        c.execute(sqlquery)
        self.tables_relationships = c.fetchall()
        c.close()
        return
    
    def search(self, entry, tablesearch):
        c = self.db.cursor()
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
        entryClean = re.sub(' +',' ',entry)
        entryList = entryClean.split(' ')
        for tablec in filtered_tables:
            query = self.search_query(entryList, tablec) + ' limit 100'
            results = [tablec.name, tablec.id] + [map(lambda f: f.name, filter(lambda f: f.list, tablec.fields))]
            c.execute(query)
            results.append(c.fetchall())
            all_results.append(results)
        returnList.append(all_results)
        c.close()
        return returnList

    def search_query(self, search_params, tablec):
        query = 'select {} from {} where '.format(', '.join(['_id'] + (map(lambda f: f.field, filter(lambda f: f.list, tablec.fields)))),
                                                  tablec.sql_table_config_name)
        where_string = []
        for search_param in search_params:
            param_clause = '(' + ' or '.join(map(lambda f: self.search_condition(f, search_param), tablec.fields)) + ')'
            where_string.append(param_clause)

        query += ' and '.join(where_string)

        return query

    @staticmethod
    def search_condition(fieldc, value):
        if fieldc.type == 1:
            return '{} = {}'.format(fieldc.field_id, value)
        elif fieldc.type == 0 and value != 'NULL':
            return '{} = STR_TO_DATE(\'{}\', "%Y-%m-%d")'.format(fieldc.field_id, value)
        else:
            return '{} like \'%{}%\''.format(fieldc.field_id, value)

    def get_record_with_type(self, table_id, record_id, listFields):
        c = self.db.cursor()
        record = [table_id, record_id,]
        recorddetails = []
        patientId = '0'
        for tablec in self.tables_config:
            if tablec.id == table_id:
                record.append(tablec.name)
                for fieldc in tablec.fields:
                    if (listFields and fieldc.list) or (not listFields):
                        sqlquery = 'select {} from {} where _id = {}'
                        params = [fieldc.field, tablec.sql_table_config_name, record_id]
                        c.execute(sqlquery.format(*params))
                        result = c.fetchone()[0]
                        if fieldc.name == 'MSF ID':
                            patientId = self.getPatientIdFromMsfId(result)
                        recorddetails.append([
                            fieldc.field_id, 
                            fieldc.type,
                            fieldc.pos,
                            fieldc.name, 
                            result,
                            fieldc.select,
                            ])
        record.append(sorted(recorddetails, key=itemgetter(2)))
        record.append(patientId)
        c.close()
        return record
    
    def getPatientIdFromMsfId(self, msfid):
        c = self.db.cursor()
        sqlquery = 'SELECT _id FROM tabla_1 WHERE campo_1 LIKE {}'
        params = ['"%{}%"'.format(msfid)]
        c.execute(sqlquery.format(*params))
        result = c.fetchone()
        if result:
            ID = result[0]
        else:
            ID = '0'
        c.close()
        return ID
    
    def insertrecord(self, table_id, fieldstoadd):
        for tablec in self.tables_config:
            if tablec.id == table_id:
                # insert into {table} (<fields>) values (<values>)
                fields = []
                values = []

                for field in fieldstoadd:
                    fields.append(field[0])

                    if field[1] == '' or field[1] is None:
                        values.append('NULL')
                    elif field[2] == 1:
                        values.append('{}'.format(field[1]))
                    elif field[2] == 0 and field[1] != 'NULL':
                        values.append('STR_TO_DATE("{}", "%Y-%m-%d")'.format(field[1]))
                    else:
                        values.append('\'{}\''.format(field[1]))

                query = 'insert into {} ({}) values ({})'.format(tablec.sql_table_config_name,
                                                                 ', '.join(fields),
                                                                 ', '.join(values))
                c = self.db.cursor()
                c.execute(query)
                self.db.commit()
                record_id = c.lastrowid
                c.close()
                return record_id
        return None
    
    def editrecord(self, table_id, record_id, fieldstochange):
        for tablec in self.tables_config:
            if tablec.id == table_id:

#                params = [tablec.sql_table_config_name, ]
#        for counter, field in enumerate(fieldstochange):
#            if field[1] == '':
#                field[1] = 'NULL'
#            if counter == 0:
#                if field[2] == 1:
#                    sqlquery = sqlquery + ' {} = {}'
#                elif field[2] == 0 and field[1] != 'NULL':
#                    sqlquery = sqlquery + ' {} = STR_TO_DATE("{}", "%Y-%m-%d")'
#                else:
#                    sqlquery = sqlquery + ' {} = "{}"'
#            else:
#                if field[2] == 1:
#                    sqlquery = sqlquery + ', {} = {}'
#                elif field[2] == 0 and field[1] != 'NULL':
#                    sqlquery = sqlquery + ', {} = STR_TO_DATE("{}", "%Y-%m-%d")'
#                else:
#                    sqlquery = sqlquery + ', {} = "{}"'
#            params.append(field[0])
#            params.append(field[1])            
#        sqlquery = sqlquery + ' WHERE _id = {}'
#        params.append(record_id)
#        c.execute(sqlquery.format(*params))
#        self.db.commit()
#        c.close()
#        return
    
                # update {table} set <f1> = <v1>, <f2> = <v2>, ...
                assignments = []

                for field in fieldstochange:
                    if field[1] == '' or field[1] is None:
                        assignments.append('{} = NULL'.format(field[0]))
                    elif field[2] == 1:
                        assignments.append('{} = {}'.format(field[0], field[1]))
                    elif field[2] == 0:
                        assignments.append('{} = STR_TO_DATE("{}", "%Y-%m-%d")'.format(field[0], field[1]))
                    else:
                        assignments.append('{} = \'{}\''.format(field[0], field[1]))

                query = 'update {} set {} where _id = {}'.format(tablec.sql_table_config_name, ', '.join(assignments), record_id)

                c = self.db.cursor()
                print(query)
                c.execute(query)
                self.db.commit()
                c.close()
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
        c = self.db.cursor()        
        sqlquery = 'DELETE FROM {} WHERE _id = {}'
        for tablec in self.tables_config:
            if tablec.id == table_id:
                params = [tablec.sql_table_config_name, record_id]
        c.execute(sqlquery.format(*params))
        self.db.commit()
        c.close()
        return

    def select_from_record_id(self, table_id, record_id, showall=True):
        c = self.db.cursor()
        sqlquery = 'select {} from {} where _id = {}'
        for tablec in self.tables_config:
            if tablec.id == table_id:
                params = [self.select_string(tablec, showall), tablec.sql_table_config_name, record_id]
                c.execute(sqlquery.format(*params))
                record = c.fetchone()
                if record is not None:
                    fields = map(lambda x: x[0], c.description)
                    result = dict(zip(fields, record))
                    c.close()
                    return result

    @staticmethod
    def select_string(table_config, showall):
        if showall:
            fields = table_config.fields
        else:
            fields = table_config.printable_fields()

        return ', '.join(['_id'] + map(lambda f: f.field, fields))
    
    def get_related_records(self, table_id, record_id):
        c = self.db.cursor()   
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
                c.execute(sqlquery.format(*params))
                relatedrecords.append((relatedfield, self.search(c.fetchone()[0], relatedtable)))
        c.close()
        return relatedrecords
        
    def getLastId(self, table_id, column_name):
        c = self.db.cursor()
        sqlquery = 'SELECT MAX({}) FROM {}'
        params = [column_name, table_id]
        c.execute(sqlquery.format(*params))
        highestId = c.fetchone()[0]
        c.close()
        if highestId:
            return highestId
        else:
            return 0

    def getNewId(self, table_id, column_name):
        lastId = self.getLastId(table_id, column_name)
        newIdInt = int(lastId) + 1
        newIdStr = str(newIdInt)
        zerosToAdd = 6-len(newIdStr)
        IdToReturn = ''
        for i in xrange(zerosToAdd):
            IdToReturn = IdToReturn + '0'
        return IdToReturn + newIdStr

    def doesIdExist(self, entry):
        c = self.db.cursor()
        sqlquery = 'SELECT _id FROM tabla_1 WHERE campo_1 = {} LIMIT 1'
        params = ['"{}"'.format(entry)]
        c.execute(sqlquery.format(*params))
        result = c.fetchone()
        c.close()
        if result:
            return result[0]
        else:
            return False
                
    def generateExport(self):
        c = self.db.cursor()
        for tablec in self.tables_config:
            with open(os.getcwd()+'/export/CSVFiles/'+tablec.name+'.csv', 'wb') as mycsv:
                wr = csv.writer(mycsv, quoting=csv.QUOTE_ALL)                
                columns = []
                sqlquery= 'SELECT '
                params = []
                for counter, field in enumerate(tablec.fields):
                    if counter == 0:
                        sqlquery = sqlquery + ' {}' 
                    else:
                        sqlquery = sqlquery + ', {}'
                    params.append(field.field_id)
                    columns.append(str(field.name))
                sqlquery = sqlquery + ' FROM {}'
                params.append(tablec.sql_table_config_name)
                wr.writerow(columns)
                c.execute(sqlquery.format(*params))
                for row in c.fetchall():
                    wr.writerow(row)
        filename = 'EasyNutExport'+date.today().strftime('%d%b%Y')
        zipPath = os.getcwd()+'/export/'
        toZip = os.getcwd()+'/export/CSVFiles'
        for f in os.listdir(os.getcwd()+'/export/'):
            if re.search('^EasyNutExport([0-9a-zA-Z]+).zip', f):
                os.remove(os.path.join(os.getcwd()+'/export/', f))
        shutil.make_archive(zipPath + filename, 'zip', toZip)
        c.close()
        return zipPath + filename 
    
    
    def setEasyUser(self, user):
        canExport = False
        canLastId = False
        addPatient = False
        tableRules = {}
        if user.groups.filter(name='Admin').exists():
            canExport = True
            canLastId = True
            addPatient = True

        if user.groups.filter(name='Registration').exists():
            addPatient = True
            
        if user.groups.filter(name='ID Check').exists():
            canLastId = True
            
        self.easy_user = {
            'canExport': canExport,
            'canLastId': canLastId,
            'addPatient': addPatient
            }
        
        
        
        
        
