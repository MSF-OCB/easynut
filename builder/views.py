# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from emr.models import DynamicRegistry


@login_required
def home(request):
    """Builder home page."""
    DynamicRegistry.init()
    context = {
        "models_config": DynamicRegistry.models_config.values(),
    }
    return render(request, "builder/home.html", context)


@login_required
def model_add(request):
    """Create a new model."""
    context = {}
    return render(request, "builder/model_add.html", context)


@login_required
def model_view(request, model_id):
    """View detailed information about the given model."""
    context = {
        "model_id": model_id,
    }
    return render(request, "builder/model_view.html", context)


@login_required
def model_edit(request, model_id):
    """Modify the given model."""
    context = {
        "model_id": model_id,
    }
    return render(request, "builder/model_edit.html", context)
