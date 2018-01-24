# -*- coding: utf-8 -*-
# Data access object for the easynutdata DB and controller of the app

from __future__ import print_function, unicode_literals
from collections import defaultdict
from datetime import date
from operator import itemgetter
import csv
import os
import re
import shutil

from django.conf import settings

from MySQLdb import converters
import MySQLdb

from .EasyDBObjects import TableConfig, FieldConfig
from .ExternalExport import ExternalExport
from .ExternalFields import ExternalFields

class DAO(object):

    @classmethod
    def factory(cls, user=None):
        """Create a ready to use instance of this class."""
        obj = cls()
        obj.set_tables_config()
        if user:
            obj.setEasyUser(user)
        return obj

    def __init__(self):
        
        # List of the configuration of each form ("table")
        self.tables_config = []
        # List of the forms
        self.tables_config_lite = {}
        # List of relationships between tables
        self.tables_relationships = []
        # Dictionnary of the user permissions
        self.easy_user = {}
        # graphs
        self.graphs = []

        # Initiate DB
        conv = converters.conversions.copy()
        conv[246] = float  # convert decimals to floats
        conv[10] = str  # convert dates
        self.db = MySQLdb.connect(settings.DATABASES['data']['HOST'],
                                  settings.DATABASES['data']['USER'],
                                  settings.DATABASES['data']['PASSWORD'],
                                  settings.DATABASES['data']['NAME'], conv=conv)

    # Create list of configurations of each forms
    def set_tables_config(self):
        # Get a list of all tables
        c = self.db.cursor()
        sql_tables = 'select tabla_id, presentador from tablas'
        c.execute(sql_tables)
        self.tables_config_lite = c.fetchall()
        # Loop through them to prepare the list
        for k, v in self.tables_config_lite:
            # Initiate form object and get its respective fields
            tablec = {}
            tablec['id'] = k
            tablec['name'] = v
            tablec['sql_table_config_name'] = 'tabla_' + str(k)
            tablec['sql_table_field_config_name'] = tablec['sql_table_config_name'] + '_des'
            tablec['fields'] = []
            sql_fields = 'SELECT _id FROM {}'  # FROM table{tabla_id}_des
            params = (tablec['sql_table_field_config_name'],)
            c.execute(sql_fields.format(*params))
            # Loop through the fields
            fieldc = FieldConfig()
            for field_id in c.fetchall():
                # Initiate field object and loop through its atributes
                fielddic = {}
                for attributek, attributev in fieldc.attributes.items():
                    sql_field_config = 'select {} from {} where _id = {}'  # FROM table{tabla_id}_des
                    params = (attributek, tablec['sql_table_field_config_name'], field_id[0],)
                    c.execute(sql_field_config.format(*params))
                    sqlresult = c.fetchone()[0]
                    # *TBC*#
                    # Convert the attributes for the field object
                    # This stupid conversion is due to a change of DB model
                    # Needs to be cleaned
                    if sqlresult in fieldc.hasmapft.keys():
                        fielddic[attributev] = fieldc.hasmapft[sqlresult]
                    elif sqlresult in fieldc.field_types.keys():
                        fielddic[attributev] = fieldc.field_types[sqlresult]
                    elif attributev == 'select':
                        selectlist = []
                        if sqlresult is not None:
                            for tostrip in sqlresult.split(','):
                                selectlist.append(tostrip.strip())
                        fielddic[attributev] = selectlist
                    else:
                        fielddic[attributev] = sqlresult
                tablec['fields'].append(fielddic)
                del fielddic
            self.tables_config.append(tablec)
            del tablec
        c.close()
#        with open('/opt/easynut/dicConfig.txt', 'w') as myFile:
#            myFile.write(json.dumps(self.tables_config, indent=4))
        return self.tables_config

    # Get graphos-ready data for graphed fields
    def set_graphs(self, record_id):
        c = self.db.cursor()
        graphlist = []

        for tb in self.tables_config:
            for fi in tb['fields']:
                if not (fi['type'] == FieldConfig.field_type_int and fi['select'] and 'grafico:' in fi['select'][0]):
                    continue  # only int fields with select

                xaxisfield = fi['select'][0][8:]
                xaxisname = [fix['name'] for fix in tb['fields'] if fix['field'] == fi['select'][0][8:]][0]
                yaxisfield = fi['field']
                yaxisname = fi['name']
                sqlquery = 'SELECT 1000 * UNIX_TIMESTAMP({}), {} FROM {} ' \
                           'WHERE campo_2 IN ( SELECT campo_1 FROM tabla_1 WHERE _id = {} ) ' \
                           'ORDER BY ' + xaxisfield
                params = [xaxisfield, yaxisfield, tb['sql_table_config_name'], record_id]
                c.execute(sqlquery.format(*params))

                graphlist = [[xaxisname, yaxisname]]  # first row contains column names, per django-graphos convention
                for rec in c.fetchall():
                    graphlist.append(list(rec))  # add rest of data columns
                self.graphs.append([tb['id'], xaxisname, yaxisname, graphlist])  # add graph
        c.close()
        return graphlist

    # *TBC*#
    # Defines the replationships between the tables
    # Not sure if it is still useful... Now it is always the same one:
    # All forms linked by the MSF ID towards Bio Data ('tabla_1')
    def set_tables_relationships(self):
        c = self.db.cursor()
        sqlquery = 'select tabla1_id, campo1_id, tabla2_id, campo2_id from tablas_relaciones'
        c.execute(sqlquery)
        self.tables_relationships = c.fetchall()
        c.close()
        return

    # Search function
    def search(self, entry, tablesearch):
        c = self.db.cursor()
        usersearch = [entry]
        returnList = []
        all_results = []
        filtered_tables = []
        # *TBC*#
        # Prepare list of tables to search in. 0 means all.
        # However it searches always only in the bio data.
        # The other tables are now searched with the function "get related records"
        if tablesearch != '0':
            for tablec in self.tables_config:
                if tablec['id'] == tablesearch:
                    filtered_tables = [tablec]
                    usersearch.append(tablec['name'])
        else:
            filtered_tables = self.tables_config
            usersearch.append('all tables')
        # To keep memory of the search entry
        returnList.append(usersearch)
        # Clean and split then entry to search in possible multiple keywords
        entryClean = re.sub(' +', ' ', entry)
        entryList = entryClean.split(' ')
        # *TBC*#
        # No need of the loop anymore
        for tablec in filtered_tables:
            query = self.search_query(entryList, tablec) + ' ORDER BY campo_1 DESC, timestamp DESC limit 100'
            results = [tablec['name'], tablec['id']] + [map(lambda f: f['name'], filter(lambda f: f['list'], tablec['fields']))]
            c.execute(query)
            results.append(c.fetchall())
            all_results.append(self.launchExternalFields(results))
        returnList.append(all_results)
        c.close()
        return returnList

    # Define the sql query for the search function
    def search_query(self, search_params, tablec):
        query = 'select {} from {} where '.format(
            ', '.join(['_id'] + (map(lambda f: f['field'], filter(lambda f: f['list'], tablec['fields'])))),
            tablec['sql_table_config_name']
        )
        where_string = []
        for search_param in search_params:
            param_clause = '(' \
                + ' or '.join(map(lambda f: self.search_condition(f, search_param), tablec['fields'])) \
                + ')'
            where_string.append(param_clause)

        query += ' and '.join(where_string)

        return query

    # Define the SQL fields to search in
    def search_by_fields(self, tablec, search_params, showall):
        where_string = []
        for search_param in search_params:
            where_string.append(
                self.search_condition(search_params[search_param]['fieldc'],
                search_params[search_param]['value'])
            )

        query = "select {} from {} where {}".format(self.select_string(tablec, showall),
                                                    tablec['sql_table_config_name'],
                                                    ' and '.join(where_string))

        c = self.db.cursor()
        c.execute(query)
        rows = c.fetchall()
        fields = map(lambda x: x[0], c.description)
        results = [dict(zip(fields, row)) for row in rows]
        c.close()
        return results

    # Define the sql conditions to search in
    @staticmethod
    def search_condition(fieldc, value):
        if fieldc['type'] == 1 and value and isinstance(value, (int, long)):
            return '{} = {}'.format(fieldc['field_id'], value)
        elif fieldc['type'] == 0 and value != 'NULL':
            return '{} = STR_TO_DATE(\'{}\', "%Y-%m-%d")'.format(fieldc['field_id'], value)
        else:
            return '{} like \'%{}%\''.format(fieldc['field_id'], value)

    # Gest a specific record (form answers) with additional info
    def get_record_with_type(self, table_id, record_id, listFields):
        c = self.db.cursor()
        record = [table_id, record_id]
        recorddetails = []
        patientId = '0'
        # *TBC*#
        # Lot of nested loops. Ugly
        for tablec in self.tables_config:
            if tablec['id'] == table_id:
                record.append(tablec['name'])
                for fieldc in tablec['fields']:
                    if (listFields and fieldc['list']) or (not listFields):
                        sqlquery = 'select {} from {} where _id = {}'
                        params = [fieldc['field'], tablec['sql_table_config_name'], record_id]
                        c.execute(sqlquery.format(*params))
                        result = c.fetchone()[0]
                        if fieldc['name'] == 'MSF ID':
                            patientId = self.getPatientIdFromMsfId(result)
                        recorddetails.append([
                            fieldc['field_id'],
                            fieldc['type'],
                            fieldc['pos'],
                            fieldc['name'],
                            result,
                            fieldc['select'],
                            ])
        record.append(sorted(recorddetails, key=itemgetter(2)))
        record.append(patientId)
        c.close()
        # *TBC*#
        # If this is not a form but just displaying the data,
        # launch the custom calculations.
        # There might be a much better way to have custom calculations...
        if listFields:
            return self.launchSingleExternalFields(record)
        return record

    # Basic function to obtain the DB ID of the patient from the MSF ID
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

    # Insert a record (answers from a form)
    def insertrecord(self, table_id, fieldstoadd):
        record_id = None
        # *TBC*#
        # The MSF ID is not at the same position in the table 1, Bio data (first position)
        # and the other tables (second position).
        # stupid
        if table_id == '1':
            for field in fieldstoadd:
                if field[0] == 'campo_1':
                    field[1] = self.getNewId('tabla_1', 'campo_1')
        # *TBC*#
        # Lost of nested loops
        for tablec in self.tables_config:
            if tablec['id'] == table_id:
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
                        values.append('\'{}\''.format(self.datacleansingle(field[1])))
                query = 'insert into {} ({}) values ({})'.format(tablec['sql_table_config_name'],
                                                                 ', '.join(fields),
                                                                 ', '.join(values))
                c = self.db.cursor()
                c.execute(query)
                record_id = c.lastrowid
                self.db.commit()
                # record_id2 = c.lastrowid
                c.close()
                # record_id_3 = record_id
        return record_id

    # Edit a record (form answers)
    def editrecord(self, table_id, record_id, fieldstochange):
        sqlquery = 'UPDATE {} SET'
        c = self.db.cursor()
        # *TBC*#
        # Loop just to obtain the name of the table in the DB
        for tablec in self.tables_config:
            if tablec['id'] == table_id:
                params = [tablec['sql_table_config_name'], ]
        # *TBC*#
        # According to the type of the field
        # There should be a proper way to handle that
        for counter, field in enumerate(fieldstochange):
            if field[1]:
                value1 = field[1].replace("'", "")
                value2 = value1.replace('"', '')
            else:
                value2 = field[1]
            if value2 == '':
                value2 = 'NULL'
            if counter == 0:
                if field[2] == 1:
                    sqlquery += ' {} = {}'
                elif field[2] == 0:
                    if value2 != 'NULL':
                        sqlquery += ' {} = STR_TO_DATE("{}", "%Y-%m-%d")'
                    else:
                        sqlquery += ' campo_1 = NULL'
                else:
                    sqlquery += ' {} = "{}"'
            else:
                if field[2] == 1:
                    sqlquery += ', {} = {}'
                elif field[2] == 0:
                    if value2 != 'NULL':
                        sqlquery += ', {} = STR_TO_DATE("{}", "%Y-%m-%d")'
                else:
                    sqlquery += ', {} = "{}"'
            if field[2] == 0:
                if value2 != 'NULL':
                    params.append(field[0])
                    params.append(self.datacleansingle(value2))
            else:
                params.append(field[0])
                params.append(self.datacleansingle(value2))
        sqlquery += ' WHERE _id = {}'
        params.append(record_id)
        c.execute(sqlquery.format(*params))
        self.db.commit()
        c.close()
        return

    # Get the form to apply for the specified table
    # Used when adding a new record
    def getrecordform(self, table_id):
        recordform = []
        fields = []
        for tablec in self.tables_config:
            if tablec['id'] == table_id:
                recordform = [tablec['id'], tablec['name']]
                for fieldc in tablec['fields']:
                    fields.append([
                        fieldc['field_id'],
                        fieldc['type'],
                        fieldc['pos'],
                        fieldc['name'],
                        fieldc['select'],
                        ])
        recordform.append(sorted(fields, key=itemgetter(2)))
        return recordform

    # Delete a specific record
    def delete(self, table_id, record_id):
        c = self.db.cursor()
        sqlquery = 'DELETE FROM {} WHERE _id = {}'
        for tablec in self.tables_config:
            if tablec['id'] == table_id:
                params = [tablec['sql_table_config_name'], record_id]
        c.execute(sqlquery.format(*params))
        self.db.commit()
        c.close()
        return

    # Used in REST Api
    def select_from_record_id(self, table_id, record_id, showall=True):
        c = self.db.cursor()
        sqlquery = 'select {} from {} where _id = {}'
        for tablec in self.tables_config:
            if tablec['id'] == table_id:
                params = [self.select_string(tablec, showall), tablec['sql_table_config_name'], record_id]
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
            fields = filter(lambda f: f['list'], table_config.fields)

        return ', '.join(['_id'] + map(lambda f: f['field'], fields))

    # *TBC*#
    # Get the records of a specific patient that are not bio data
    def get_related_records(self, record_id):
        c = self.db.cursor()
        relatedrecords = []
        templist = []
        for tablec in self.tables_config:
            if self.easy_user['tables'][tablec['id']]['view_table'] and tablec['id'] != '1':
                sqlquery = 'SELECT campo_1 FROM tabla_1 WHERE _id = {}'
                params = [record_id]
                c.execute(sqlquery.format(*params))
                msfId = c.fetchone()[0]
                sqlquery = 'SELECT registros FROM tablas WHERE tabla_id = {}'
                params = [tablec['id']]
                c.execute(sqlquery.format(*params))
                position = c.fetchone()[0]
                templist.append([self.getRelatedSearch(msfId, tablec['id']), int(position)])
        c.close()
        for recordsList in sorted(templist, key=itemgetter(1)):
            relatedrecords.append(recordsList[0])
        return relatedrecords

    # See up
    def getRelatedSearch(self, entry, table_id):
        c = self.db.cursor()
        usersearch = [entry]
        returnList = []
        all_results = []
        search_query = ''
        for tablec in self.tables_config:
            if table_id == tablec['id']:
                usersearch.append(tablec['name'])
                search_query = 'SELECT _id'
                for field in tablec['fields']:
                    if field['list'] is True:
                        relatedrecords = [tablec['name'], tablec['id']] \
                            + [map(lambda f: f['name'], filter(lambda f: f['list'], tablec['fields']))]
                        search_query += ','+field['field_id']
                search_query += ' FROM ' + tablec['sql_table_config_name'] \
                    + ' WHERE campo_2 = "' + entry + '" ORDER BY campo_1 DESC'
        if search_query != '':
            c.execute(search_query)
            relatedrecords.append(c.fetchall())
            all_results.append(self.launchExternalFields(relatedrecords))
            returnList.append(usersearch)
            returnList.append(all_results)
        return returnList

    # Get last ID inserted
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

    # Create a new ID
    def getNewId(self, table_id, column_name):
        lastId = self.getLastId(table_id, column_name)
        newIdInt = int(lastId) + 1
        newIdStr = str(newIdInt)
        zerosToAdd = 6 - len(newIdStr)
        IdToReturn = ''
        for i in xrange(zerosToAdd):
            IdToReturn = IdToReturn + '0'
        return IdToReturn + newIdStr

    # Check if an ID already exists
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

    # Generate a raw export of the DB: a zip file containing csv of all tables
    def generateExport(self):
        c = self.db.cursor()
        exportDir = os.path.join(settings.BASE_DIR, 'export/')
        for tablec in self.tables_config:
            with open(exportDir+'CSVFiles/'+re.sub('[^\w\-_\. ]', '', tablec['name'])+'.csv', 'wb') as mycsv:
                wr = csv.writer(mycsv, quoting=csv.QUOTE_ALL)                
                columns = []
                sqlquery= 'SELECT '
                params = []
                for counter, field in enumerate(tablec['fields']):
                    if counter == (len(tablec['fields']) - 1):
                        sqlquery = sqlquery + ', user, timestamp'
                    else:
                        if counter == 0:
                            sqlquery = sqlquery + ' {}'
                        else:
                            sqlquery = sqlquery + ', {}'
                        params.append(field['field_id'])
                        columns.append(str(field['name']))
                columns.append('User')
                columns.append('Timestamp')
                sqlquery = sqlquery + ' FROM {}'
                params.append(tablec['sql_table_config_name'])
                wr.writerow(self.dataclean(columns))
                c.execute(sqlquery.format(*params)) 
                for row in c.fetchall():
                    wr.writerow(self.dataclean(row))
        filename = 'EasyNutExport'+date.today().strftime('%d%b%Y')                     
        zipPath = exportDir
        toZip = exportDir + 'CSVFiles'
        for f in os.listdir(exportDir):
            if re.search('^EasyNutExport([0-9a-zA-Z]+).zip', f):
                os.remove(os.path.join(exportDir, f))
        shutil.make_archive(zipPath + filename, 'zip', toZip)
        c.close()
        return zipPath + filename

    # *TBC*#
    # Doesnt seem to be used anymore
    def getAbsents(self):
        # c = self.db.cursor()
        # exportDir = os.path.join(settings.BASE_DIR, 'export/')
        zippath = '.home/doudou/Documents/www/Django/export'
        return zippath

    # Define the permissions of a user
    def setEasyUser(self, user):
        # User groups (careful, this has to be linked with the Django group table)
        # Here it uses both DB, easynut and easynutdata
        # *TBC*#
        # The groups (or "roles") should not be defined here
        group_reg = 1
        group_adm = 2
        group_flo = 3
        group_nur = 4
        group_idc = 5
        group_pha = 6

        c = self.db.cursor()
        sql_query = 'SELECT group_id, table_id, view_table, add_table, edit_table, delete_table FROM easy_roles'
        c.execute(sql_query)
        easy_roles = c.fetchall()
        user_tables = {}

        # Consider first that the user has no roles
        for tclk, tclv in self.tables_config_lite:
            user_tables[str(tclk)] = {
                'view_table': False,
                'add_table': False,
                'edit_table': False,
                'delete_table': False
                }

        # Loop first through the available roles (or "groups")
        for role in easy_roles:
            # Then loop through the roles the user possesses
            for group in user.groups.all():
                if group.id == role[0]:
                    for utk, utv in user_tables[str(role[1])].iteritems():
                        if utk == 'view_table' and utv is False and role[2] == 1:
                            user_tables[str(role[1])][str(utk)] = True
                        if utk == 'add_table' and utv is False and role[3] == 1:
                            user_tables[str(role[1])][str(utk)] = True
                        if utk == 'edit_table' and utv is False and role[4] == 1:
                            user_tables[str(role[1])][str(utk)] = True
                        if utk == 'delete_table' and utv is False and role[5] == 1:
                            user_tables[str(role[1])][str(utk)] = True
        # Only for admin
        canExport = False
        canLastId = False

        if user.groups.filter(id=group_adm).exists():
            canExport = True
            canLastId = True
            for tclk, tclv in self.tables_config_lite:
                user_tables[str(tclk)] = {
                    'view_table': True,
                    'add_table': True,
                    'edit_table': True,
                    'delete_table': True
                    }
        # *TBC*#
        # Not sure if the last ID is used anymore now that the system automatically provides an ID to the patient
        if user.groups.filter(id=group_idc).exists():
            canLastId = True

        self.easy_user = {
            'canExport': canExport,
            'canLastId': canLastId,
            'tables': user_tables
            }
        c.close()
        return self.easy_user

    # Check if the user has the permission to execture a function or access a page
    def backEndUserRolesCheck(self, table_id, type):
        for k, v in self.easy_user['tables'].iteritems():
            if k == table_id and v[type]:
                return True
        return False

    # Connector to the custom functions
    def launchExternalFields(self, results):
        extF = ExternalFields()
        return extF.addFields(results, self.tables_config)

    # Same
    def launchSingleExternalFields(self, results):
        extF = ExternalFields()
        return extF.addSingleFields(results, self.tables_config)

    # Same
    def launchExternalExport(self):
        extE = ExternalExport()
        return extE.addCSVs()

    # Clean the data before saving them (or in bulk, or only one)
    # *TBC*#
    # Should be the same type of cleaning, so weird to have 2 functions similar
    def dataclean(self, row):
        returnedRow = []
        for field in row:
            if field:
                field1 = str(field).replace(',', ' ')
                field2 = field1.replace('"', '')
                field3 = field2.replace("'", "")
            else:
                field3 = ""
            returnedRow.append(field3)
        return returnedRow

    # Same
    def datacleansingle(self, field):
        if field:
            return re.sub(r'[^a-zA-Z0-9-+_<>.\s]', '', field)
        else:
            return ""
