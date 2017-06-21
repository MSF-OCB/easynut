from django.conf.urls import url

from . import views

app_name = 'emr'

urlpatterns = [
	# ex: /emr/
	url(r'^$', views.index, name='index'),
	# ex: /emr/5
	#url(r'^detail/(?P<record_id>[0-9]+)$', views.detail, name='detail'),
	url(r'^?[0-9]+)/detail/$', views.detail, name='detail'),	
	
	# ex: /emr/5/results/
	url(r'^results/$', views.results, name='results'),
	# ex: /emr/search/*entry*
	# url(r'^search/?$', views.search, name='search'),
]
"""
urlpatterns = patterns('',
    url(r'^$', 'emr.views.index', name='index'),
)
"""