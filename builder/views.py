# -*- coding: utf-8 -*-
from django.shortcuts import render

from emr.models import DynamicRegistry


def home(request):
    """Builder home page."""
    DynamicRegistry.load_models_config()
    context = {
        "models_config": DynamicRegistry.models_config.values(),
    }
    return render(request, "builder/home.html", context)


def model_add(request):
    """Create a new model."""
    context = {}
    return render(request, "builder/model_add.html", context)


def model_view(request, model_id):
    """View detailed information about the given model."""
    context = {
        "model_id": model_id,
    }
    return render(request, "builder/model_view.html", context)


def model_edit(request, model_id):
    """Modify the given model."""
    context = {
        "model_id": model_id,
    }
    return render(request, "builder/model_edit.html", context)
