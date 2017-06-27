# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from operator import itemgetter
from django.template.context_processors import request
from DAO import *
from EasyDBObjects import *
from django.utils.encoding import smart_str

def index(request):
    template_name = 'emr/index.html'
    daoobject = DAO()
    daoobject.set_tables_config()
    return render(request, template_name, {'edbtables': daoobject.tables_config_lite, 'lastId' : daoobject.getLastId('tabla_1', 'campo_1')})

def results(request):
    search_query = request.GET.get('searchstring')
    tablesearch = request.GET.get('tablesearch')
    template_name = 'emr/results.html'
    daoobject = DAO()
    daoobject.set_tables_config()
    return render(request, template_name, {'searchresults': daoobject.search(search_query, tablesearch), 'lastId' : daoobject.getLastId('tabla_1', 'campo_1')})

def detail(request, table_id, record_id):
    template_name = 'emr/detail.html'
    daoobject = DAO()
    daoobject.set_tables_config()
    daoobject.set_tables_relationships()
    return render(request, template_name, {
        'record': daoobject.get_record_with_type(table_id, record_id), 
        'relatedrecords' : daoobject.get_related_records(table_id, record_id),
        'lastId' : daoobject.getLastId('tabla_1', 'campo_1')
        })

def edit(request, table_id, record_id):
    template_name = 'emr/edit.html'
    daoobject = DAO()
    daoobject.set_tables_config()    
    return render(request, template_name, {'record': daoobject.get_record_with_type(table_id, record_id), 'lastId' : daoobject.getLastId('tabla_1', 'campo_1')})

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
    if (not related_record_entry) and (table_id == 1):
        related_record_entry = daoobject.getLastId('tabla_1', 'campo_1') + 1
        related_record_field = 'campo_1'
    if table_id != "0":
        return render(request, template_name, {
            'recordform': daoobject.getrecordform(table_id),
            'related_record_entry' : related_record_entry,
            'related_record_field' : related_record_field,
            'lastId' : daoobject.getLastId('tabla_1', 'campo_1')
            })
    return index(request)

def deleterecord(request, table_id, record_id):
    daoobject = DAO()
    daoobject.set_tables_config()
    daoobject.delete(table_id, record_id)
    return index(request)

def downloadexport(request):
    daoobject = DAO()
    daoobject.set_tables_config()
    zip = daoobject.generateExport()+'.zip'
    if os.path.exists(zip):
        with open(zip, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(zip)
            return response
    raise Http404

           
