from django.conf.urls import url

from . import views

app_name = 'emr'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<table_id>[0-9]+)/(?P<record_id>[0-9]+)/detail/$', views.detail, name='detail'),	
	url(r'^(?P<table_id>[0-9]+)/(?P<record_id>[0-9]+)/edit/$', views.edit, name='edit'),	
	url(r'^results/$', views.results, name='results'),
	url(r'^save/$', views.save, name='save'),
	url(r'^addrecord/$', views.addrecord, name='addrecord'),
	url(r'^(?P<table_id>[0-9]+)/(?P<record_id>[0-9]+)/deleterecord/$', views.deleterecord, name='deleterecord'),	
	url(r'^downloadexport/$', views.downloadexport, name='downloadexport'),
]
