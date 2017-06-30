from django.conf.urls import include, url

from . import views

from rest_framework import routers
from django.contrib.auth import views as auth_views

from REST import TableViewSet

app_name = 'emr'

router = routers.DefaultRouter()
router.register(r'', TableViewSet, base_name='api')

urlpatterns = [
        url(r'api/', include(router.urls)),
        url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        url(r'login/$', auth_views.login, name='login'),
        url(r'logout/$', auth_views.logout, name='logout'),
	
        url(r'^$', views.index, name='index'),
	url(r'^(?P<table_id>[0-9]+)/(?P<record_id>[0-9]+)/detail/$', views.detail, name='detail'),	
	url(r'^(?P<table_id>[0-9]+)/(?P<record_id>[0-9]+)/edit/$', views.edit, name='edit'),	
	url(r'^results/$', views.results, name='results'),
	url(r'^save/$', views.save, name='save'),
	url(r'^addrecord/$', views.addrecord, name='addrecord'),
	url(r'^(?P<table_id>[0-9]+)/(?P<record_id>[0-9]+)/deleterecord/$', views.deleterecord, name='deleterecord'),	
	url(r'^downloadexport/$', views.downloadexport, name='downloadexport'),
]

