# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views


app_name = "builder"

urlpatterns = [
    url(r"^$", views.home, name="home"),
    url(r"^add/$", views.model_add, name="model_add"),
    url(r"^(?P<model_id>[0-9]+)/$", views.model_view, name="model_view"),
    url(r"^(?P<model_id>[0-9]+)/edit/$", views.model_edit, name="model_edit"),
]
