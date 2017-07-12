# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render, render_to_response,redirect
from django.template import loader, RequestContext
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from operator import itemgetter
from django.template.context_processors import request
from DAO import *
from EasyDBObjects import *
from django.utils.encoding import smart_str
from django.http import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator

def loginview(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/nut/')
            else:
                return render(request, 'emr/login.html', {'wrongcrendentials' : 'Your account is disabled.'})
        else:
            return render(request, 'emr/login.html', {'wrongcrendentials' : 'Invalid username / password combination provided'})
    else:
        return render(request, 'emr/login.html', {'wrongcrendentials' : ''})


def logoutbutton(request):
    logout(request)    
    return render(request, 'emr/login.html', {'wrongcrendentials' : ''})
    
@login_required
def index(request):
    template_name = 'emr/index.html'
    daoobject = DAO()
    daoobject.set_tables_config()
    daoobject.setEasyUser(request.user)
    return render(request, template_name, {
        'edbtables': daoobject.tables_config_lite, 
        'lastId' : daoobject.getLastId('tabla_1', 'campo_1'),
        'easyUser': daoobject.easy_user
        })

@login_required
def results(request):
    template_name = 'emr/results.html'
    search_query = request.GET.get('searchstring')
    daoobject = DAO()
    daoobject.set_tables_config()    
    daoobject.setEasyUser(request.user)
    if daoobject.doesIdExist(search_query):
        return patient(request, daoobject.doesIdExist(search_query))    
    else:
        return render(request, template_name, {
            'searchresults': daoobject.search(search_query, '1'), 
            'lastId' : daoobject.getLastId('tabla_1', 'campo_1'),
            'easyUser': daoobject.easy_user
            })

@login_required
def patient(request, record_id):
    template_name = 'emr/patient.html'    
    daoobject = DAO()
    daoobject.set_tables_config()
    daoobject.set_tables_relationships()
    daoobject.setEasyUser(request.user)
    return render(request, template_name, {
        'record': daoobject.get_record_with_type('1', record_id, True), 
        'relatedrecords' : daoobject.get_related_records(record_id),
        'lastId' : daoobject.getLastId('tabla_1', 'campo_1'),
        'easyUser': daoobject.easy_user
        })
    
@login_required
def detail(request, table_id, record_id):
    template_name = 'emr/detail.html'
    daoobject = DAO()
    daoobject.set_tables_config()
    daoobject.setEasyUser(request.user)
    if daoobject.backEndUserRolesCheck(table_id, 'view_table'):
        return render(request, template_name, {
            'record': daoobject.get_record_with_type(table_id, record_id, False), 
            'lastId' : daoobject.getLastId('tabla_1', 'campo_1'),
            'easyUser': daoobject.easy_user
            })
    return index(request)

@login_required
def edit(request, table_id, record_id):
    template_name = 'emr/edit.html'
    daoobject = DAO()
    daoobject.set_tables_config()   
    daoobject.setEasyUser(request.user)
    if daoobject.backEndUserRolesCheck(table_id, 'edit_table'):
        return render(request, template_name, {
            'record': daoobject.get_record_with_type(table_id, record_id, False), 
            'lastId' : daoobject.getLastId('tabla_1', 'campo_1'),
            'easyUser': daoobject.easy_user
            })
    return index(request)

@login_required
def save(request):
    record_id = request.GET.get('record_id')
    table_id = request.GET.get('table_id')
    daoobject = DAO()
    daoobject.set_tables_config()
    daoobject.setEasyUser(request.user)
    fieldstochange = []
    patientId = 0
    for tablec in daoobject.tables_config:
        if tablec.id == table_id:
            for fieldc in tablec.fields:
                if fieldc.name == 'MSF ID':
                    patientId = daoobject.getPatientIdFromMsfId(request.GET.get(fieldc.field_id))
                fieldstochange.append([fieldc.field_id, request.GET.get(fieldc.field_id), fieldc.type])
            fieldstochange.append(['user', request.user.username, '2'])            
    if record_id != "0":
        if daoobject.backEndUserRolesCheck(table_id, 'edit_table'):
            daoobject.editrecord(table_id, record_id, fieldstochange)
    else:
        if daoobject.backEndUserRolesCheck(table_id, 'add_table'):
            record_id = daoobject.insertrecord(table_id, fieldstochange)
            if table_id == '1':
                patientId = record_id
    return patient(request, patientId)

@login_required
def addrecord(request, table_id, related_record_entry):
    template_name = 'emr/addrecord.html'
    daoobject = DAO()
    daoobject.set_tables_config()
    daoobject.set_tables_relationships() 
    daoobject.setEasyUser(request.user)
    if daoobject.backEndUserRolesCheck(table_id, 'add_table'):
        if (related_record_entry == '0') and (table_id == '1'):
            related_record_field = 'campo_1'
        else:
            related_record_field = 'campo_2'
        if table_id != "0":
            return render(request, template_name, {
                'recordform': daoobject.getrecordform(table_id),
                'related_record_entry' : related_record_entry,
                'related_record_field' : related_record_field,
                'lastId' : daoobject.getLastId('tabla_1', 'campo_1'),
                'easyUser': daoobject.easy_user
                })
    return index(request)

@login_required
def deleterecord(request, table_id, record_id):
    daoobject = DAO()
    daoobject.set_tables_config()
    daoobject.setEasyUser(request.user)
    if daoobject.backEndUserRolesCheck(table_id, 'delete_table'):
        daoobject.delete(table_id, record_id)
    return index(request)

@login_required
def downloadexport(request):
    daoobject = DAO()
    daoobject.set_tables_config()
    daoobject.setEasyUser(request.user)
    if request.user.groups.filter(id=2).exists():
        zip = daoobject.generateExport()+'.zip'
        if os.path.exists(zip):
            with open(zip, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/zip")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(zip)
                return response
        raise Http404
    else:
        return index(request)

           
