#*TBC*#
# Allow to add some customization
# But this should not be hardcoded
# A better system to add cusomization features should be found
# An idea could be to to enter SQL queries in the DB via a user interface for the admin
# But not sure how to avoid knowing perfectly the DB (having to know the table name and field name),
# or if we could obtain such a precision

from __future__ import unicode_literals
from django.conf import settings
import MySQLdb
from MySQLdb import converters
import datetime
import os,re
import csv

class ExternalExport(object):

    def __init__(self):
        conv=converters.conversions.copy()
        conv[246]=float    # convert decimals to floats
        conv[10]=str       # convert dates
        self.db = MySQLdb.connect(settings.DATABASES['data']['HOST'],
                                  settings.DATABASES['data']['USER'],
                                  settings.DATABASES['data']['PASSWORD'],
                                  settings.DATABASES['data']['NAME'], conv=conv)

    def getAbsents(self):
        c = self.db.cursor()
        listOfAbsents = []
        sql_select = ("SELECT bd.campo_1,bd.campo_2,bd.campo_14,c.campo_30 "
                      "FROM tabla_1 bd LEFT JOIN tabla_8 c ON (bd.campo_1 = c.campo_2) "
                      "WHERE bd.campo_14 IS NOT NULL AND bd.campo_14 <> 'NULL' "
                      "AND c.campo_30 IS NOT NULL AND c.campo_30 <> 'NULL' "
                      "ORDER BY c.campo_1 "
                      )
        c.execute(sql_select)
        listOfAbsents = c.fetchall()
        reducedLists = {}
        today = datetime.datetime.now()
        for absent in listOfAbsents:
            visitdate = datetime.datetime.strptime(absent[3], '%Y-%m-%d')
            vistDate7 = visitdate + datetime.timedelta(days=7)
            visitDate14 = visitdate + datetime.timedelta(days=14)
            if (today >= vistDate7) and (today <= visitDate14):
                sql_query = ('SELECT campo_1 FROM tabla_8 '
                             'WHERE campo_2 = "' + absent[0] + '" AND campo_1 IS NOT NULL AND campo_1 <> "NULL" '
                             'ORDER BY campo_1 DESC LIMIT 1')
                c.execute(sql_query)
                lastVisitStringL = c.fetchone()
                if lastVisitStringL:
                    lastVisitString = lastVisitStringL[0]
                    if lastVisitString and lastVisitString != '':
                        lastVisit = datetime.datetime.strptime(lastVisitString, '%Y-%m-%d')
                        if lastVisit < visitdate:
                            canContinueIM = True
                            canContinueDis = True
                            canContinueAbs = True
                            canContinue = True
                            # Checking Internal movements to ITFC
                            sql_im = ('SELECT campo_1 FROM tabla_5 WHERE campo_2 = "' + absent[0] + '" '
                                      'AND campo_3 = "Transfer out" '
                                      'AND campo_1 IS NOT NULL AND campo_1 <> "NULL" '
                                      'ORDER BY campo_1 DESC LIMIT 1')
                            c.execute(sql_im)
                            lastIML = c.fetchone()
                            if not lastIML:
                                canContinueIM = False
                            if canContinueIM:
                                lastIM = lastIML[0]
                            if canContinueIM and lastIM and lastIM != 'NULL':
                                lastIMDate = datetime.datetime.strptime(lastIM, '%Y-%m-%d')
                                if lastIMDate > visitdate:
                                    canContinue = False
                            # Checking Discharges
                            if canContinue:        
                                sql_dis = ('SELECT COUNT(*) FROM tabla_4 WHERE campo_2 = "' + absent[0] + '" ')
                                c.execute(sql_dis)
                                countDis = c.fetchone()
                                if not countDis:
                                    canContinueDis = False
                                if canContinueDis:
                                    lastDis = int(countDis[0])
                                    if lastDis > 0:
                                        canContinue = False
                            # Checking absent called made
                            if canContinue:        
                                sql_abs = ('SELECT campo_1 FROM tabla_17 WHERE campo_2 = "' + absent[0] + '" '
                                          'AND campo_1 IS NOT NULL AND campo_1 <> "NULL" '
                                          'ORDER BY campo_1 DESC LIMIT 1')
                                c.execute(sql_abs)
                                lastAbsL = c.fetchone()
                                if not lastAbsL:
                                    canContinueAbs = False
                                if canContinueAbs:
                                    lastAbs = lastAbsL[0]
                                if canContinueAbs and lastAbs and lastAbs != 'NULL':
                                    lastAbsDate = datetime.datetime.strptime(lastAbs, '%Y-%m-%d')
                                    if lastAbsDate > visitdate:
                                        canContinue = False
                            
                            if canContinue:
                                if absent[0] not in reducedLists:
                                    reducedLists[absent[0]] = [absent[1],absent[2],absent[3]]
                                else:
                                    compaDate = datetime.datetime.strptime(reducedLists[absent[0]][2], '%Y-%m-%d')
                                    newDate = datetime.datetime.strptime(absent[3], '%Y-%m-%d')
                                    if newDate > compaDate:
                                        reducedLists[absent[0]] = [absent[1],absent[2],absent[3]]        
        exportDir = os.path.join(settings.BASE_DIR, 'export/')
        with open(exportDir+'Absents'+'.csv', 'wb') as mycsv:
            wr = csv.writer(mycsv, quoting=csv.QUOTE_ALL)   
            wr.writerow(['MSF ID','Name','Phone number','Last expected visit'])
            for k,v in reducedLists.iteritems():
                wr.writerow(self.dataclean([k,v[0],v[1],v[2]]))
        c.close()
        return exportDir + 'Absents.csv'
    
    def getDefaulters(self):
        c = self.db.cursor()
        listOfAbsents = []
        sql_select = ("SELECT bd.campo_1,bd.campo_2,c.campo_30 "
                      "FROM tabla_1 bd LEFT JOIN tabla_8 c ON (bd.campo_1 = c.campo_2) "
                      "WHERE c.campo_30 IS NOT NULL AND c.campo_30 <> 'NULL' "
                      "ORDER BY c.campo_1 "
                      )
        c.execute(sql_select)
        listOfAbsents = c.fetchall()
        reducedLists = {}
        today = datetime.datetime.now()
        for absent in listOfAbsents:
            visitdate = datetime.datetime.strptime(absent[2], '%Y-%m-%d')
            visitDate14 = visitdate + datetime.timedelta(days=14)
            if today >= visitDate14:
                sql_query = ('SELECT campo_1 FROM tabla_8 '
                             'WHERE campo_2 = "' + absent[0] + '" AND campo_1 IS NOT NULL AND campo_1 <> "NULL" '
                             'ORDER BY campo_1 DESC LIMIT 1')
                c.execute(sql_query)
                lastVisitStringL = c.fetchone() 
                if lastVisitStringL:
                    lastVisitString = lastVisitStringL[0]
                    if lastVisitString and lastVisitString != '':
                        lastVisit = datetime.datetime.strptime(lastVisitString, '%Y-%m-%d')
                        if lastVisit < visitdate:
                            canContinueIM = True
                            canContinueDis = True
                            canContinueAbs = True
                            canContinue = True
                            # Checking Internal movements to ITFC
                            sql_im = ('SELECT campo_1 FROM tabla_5 WHERE campo_2 = "' + absent[0] + '" '
                                      'AND campo_3 = "Transfer out" '
                                      'AND campo_1 IS NOT NULL AND campo_1 <> "NULL" '
                                      'ORDER BY campo_1 DESC LIMIT 1')
                            c.execute(sql_im)
                            lastIML = c.fetchone()
                            if not lastIML:
                                canContinueIM = False
                            if canContinueIM:
                                lastIM = lastIML[0]
                            if canContinueIM and lastIM and lastIM != 'NULL':
                                lastIMDate = datetime.datetime.strptime(lastIM, '%Y-%m-%d')
                                if lastIMDate > visitdate:
                                    canContinue = False
                            # Checking Discharges
                            if canContinue:        
                                sql_dis = ('SELECT COUNT(*) FROM tabla_4 WHERE campo_2 = "' + absent[0] + '" ')
                                c.execute(sql_dis)
                                countDis = c.fetchone()
                                if not countDis:
                                    canContinueDis = False
                                if canContinueDis:
                                    lastDis = int(countDis[0])
                                    if lastDis > 0:
                                        canContinue = False
                            # Checking absent called made
                            if canContinue:        
                                sql_abs = ('SELECT campo_1 FROM tabla_17 WHERE campo_2 = "' + absent[0] + '" '
                                          'AND campo_1 IS NOT NULL AND campo_1 <> "NULL" '
                                          'ORDER BY campo_1 DESC LIMIT 1')
                                c.execute(sql_abs)
                                lastAbsL = c.fetchone()
                                if not lastAbsL:
                                    canContinueAbs = False
                                if canContinueAbs:
                                    lastAbs = lastAbsL[0]
                                if canContinueAbs and lastAbs and lastAbs != 'NULL':
                                    lastAbsDate = datetime.datetime.strptime(lastAbs, '%Y-%m-%d')
                                    if lastAbsDate > visitdate:
                                        canContinue = False
                            
                            if canContinue:
                                if absent[0] not in reducedLists:
                                    reducedLists[absent[0]] = [absent[1],absent[2]]
                                else:
                                    compaDate = datetime.datetime.strptime(reducedLists[absent[0]][1], '%Y-%m-%d')
                                    newDate = datetime.datetime.strptime(absent[2], '%Y-%m-%d')
                                    if newDate > compaDate:
                                        reducedLists[absent[0]] = [absent[1],absent[2]]        
        exportDir = os.path.join(settings.BASE_DIR, 'export/')
        with open(exportDir+'Defaulters'+'.csv', 'wb') as mycsv:
            wr = csv.writer(mycsv, quoting=csv.QUOTE_ALL)                
            wr.writerow(['MSF ID','Name','Last expected visit'])
            for k,v in reducedLists.iteritems():
                wr.writerow(self.dataclean([k,v[0],v[1]]))
        c.close()
        return exportDir + 'Defaulters.csv'
    
    def dataclean(self, row):
        returnedRow = []
        for field in row:
            if field:
                field1 = str(field).replace(',',' ')
                field2 = field1.replace('"','')
                field3 = field2.replace("'","")
            else:
                field3 = ""
            returnedRow.append(field3)
        return returnedRow
