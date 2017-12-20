# -*- coding: utf-8 -*-
# from django.conf.urls import include
from django.conf.urls import url

# from RESTViews import RecordList, RecordDetail
from . import views


app_name = 'emr'

urlpatterns = [
    url(r'^login/$', views.loginview, name='login'),
    url(r'^logoutbutton/$', views.logoutbutton, name='logoutbutton'),
    # url(r'^api/(?P<table_id>[0-9]+)/$', RecordList.as_view()),
    # url(r'^api/(?P<table_id>[0-9]+)/(?P<pk>(NULL|[0-9]+))/$', RecordDetail.as_view()),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<record_id>[0-9]+)/patient/$', views.patient, name='patient'),
    url(r'^(?P<table_id>[0-9]+)/(?P<record_id>[0-9]+)/detail/$', views.detail, name='detail'),
    url(r'^(?P<table_id>[0-9]+)/(?P<record_id>[0-9]+)/edit/$', views.edit, name='edit'),
    url(
        r'^(?P<table_id>[0-9]+)/(?P<related_record_entry>(NULL|[0-9]+))/addrecord/$',
        views.addrecord,
        name='addrecord',
    ),
    url(r'^results/$', views.results, name='results'),
    url(r'^save/$', views.save, name='save'),
    url(r'^(?P<table_id>[0-9]+)/(?P<record_id>[0-9]+)/deleterecord/$', views.deleterecord, name='deleterecord'),
    url(r'^downloadexport/$', views.downloadexport, name='downloadexport'),
    url(r'^downloadbackup/$', views.downloadbackup, name='downloadbackup'),
    url(r'^downloadabsents/$', views.downloadabsents, name='downloadabsents'),
    url(r'^downloaddefaulters/$', views.downloaddefaulters, name='downloaddefaulters'),

    url(r'^export/excel$', views.export_excel, name='export_excel'),
    url(r'^export/data-model$', views.export_data_model, name='export_data_model'),
]
