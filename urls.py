from django.conf.urls import include, url
from . import views

#from rest_framework import routers
from django.contrib.auth import views as auth_views

#from REST import TableViewSet

app_name = 'emr'

#router = routers.DefaultRouter()
#router.register(r'', TableViewSet, base_name='api')

urlpatterns = [
	url(r'^loginview/$', views.loginview, name='loginview'),
    #url(r'api/', include(router.urls)),
    #url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),	
	url(r'^$', views.index, name='index'),
	url(r'^(?P<record_id>[0-9]+)/patient/$', views.patient, name='patient'),	
	url(r'^(?P<table_id>[0-9]+)/(?P<record_id>[0-9]+)/detail/$', views.detail, name='detail'),	
	url(r'^(?P<table_id>[0-9]+)/(?P<record_id>[0-9]+)/edit/$', views.edit, name='edit'),
	url(r'^(?P<table_id>[0-9]+)/(?P<related_record_entry>[0-9]+)/(?P<related_record_field>[a-zA-Z_0-9]+)/addrecord/$', views.addrecord, name='addrecord'),		
	url(r'^results/$', views.results, name='results'),
	url(r'^save/$', views.save, name='save'),
	url(r'^(?P<table_id>[0-9]+)/(?P<record_id>[0-9]+)/deleterecord/$', views.deleterecord, name='deleterecord'),	
	url(r'^downloadexport/$', views.downloadexport, name='downloadexport'),
]

