# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
import MySQLdb
from MySQLdb import converters
import datetime

class ExternalFields(object):
    
    def __init__(self):
        conv=converters.conversions.copy()
        conv[246]=float    # convert decimals to floats
        conv[10]=str       # convert dates
        self.db = MySQLdb.connect(settings.DATABASES['data']['HOST'],
                                  settings.DATABASES['data']['USER'],
                                  settings.DATABASES['data']['PASSWORD'],
                                  settings.DATABASES['data']['NAME'], conv=conv)
        
        
    def addFields(self, results, tables_config):
        if results[1] == '7':
            results = self.addWeightDifference(results, tables_config)
        return results
    
    def addSingleFields(self, results, tables_config):
        if results[0] == '1':
            results = self.addLastStepSingle(results, tables_config)
            results = self.addNextAppointmentSingle(results, tables_config)
        return results    
    
    def addLastStepSingle(self, results, tables_config):
        c = self.db.cursor()
        lastStep = []
        msfId = ''
        for field in results[3]:
            if field[3] == 'MSF ID':
                msfId = field[4]
        listLength = len(results[3])
        if msfId:
            laststeps = {}
            for tablec in tables_config:
                if tablec.id != '1':
                    sql_query = 'SELECT MAX(timestamp) FROM {} WHERE campo_2 = {}'
                    params = [tablec.sql_table_config_name, msfId]
                    c.execute(sql_query.format(*params))
                    timestamp = c.fetchone()[0]
                    if timestamp:
                        laststeps[tablec.name] = timestamp
            if bool(laststeps):
                lastStep = max(laststeps, key=laststeps.get)
                Date = laststeps[lastStep].strftime('%a %d %b at %H:%M')
                Answer = lastStep + ' - ' + Date
                lastStep = [0, 0, listLength+1, 'Last step', Answer, '']
            else:
                lastStep = [0, 0, listLength+1, 'Last step', 'New', '']
            results[3].append(lastStep)
        return results
    
    def addNextAppointmentSingle(self, results, tables_config):
        c = self.db.cursor()
        lastStep = []
        msfId = ''
        for field in results[3]:
            if field[3] == 'MSF ID':
                msfId = field[4]
        listLength = len(results[3])
        if msfId:
            sql_query = 'SELECT campo_30 FROM tabla_8 WHERE campo_7 IS NOT NULL AND campo_2 = {} ORDER BY timestamp DESC LIMIT 1'
            params = [msfId,]
            c.execute(sql_query.format(*params))
            date = c.fetchone()
            if bool(date):
                datetime_object = datetime.datetime.strptime(date[0], '%Y-%m-%d')
                lastStep = [0, 0, listLength+1, 'Next visit', datetime_object.strftime('%A %d %B %Y'), '']
            else:
                lastStep = [0, 0, listLength+1, 'Next visit', 'Unknown', '']
            results[3].append(lastStep)
        return results
    
    def addWeightDifference(self, results, tables_config):
        c = self.db.cursor()
        weightInd = 0
        newColumns = []
        for counter0, column in enumerate(results[2]):
            if column == 'Weight (kg)':
                weightInd = counter0
                newColumns.append('Weight (kg)')
                newColumns.append('Weight difference')
            else:
                newColumns.append(column)
        results[2] = newColumns
        newResults = []
        for counter1, result in enumerate(results[3]):
            newIndResult = []
            for counter2, fieldr in enumerate(result):
                newIndResult.append(fieldr)
                if counter2 == weightInd + 1:
                    if counter1 != (len(results[3])-1):
                        newIndResult.append(results[3][counter1][weightInd+1] - results[3][counter1+1][weightInd+1])
                    else:
                        newIndResult.append('')
            newResults.append(newIndResult)
        results[3] = newResults  
        return results
    
    