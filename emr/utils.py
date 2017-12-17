# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.utils import timezone


# See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Complete_list_of_MIME_types
CONTENT_TYPE_CSV = "text/csv"
CONTENT_TYPE_XLS = "application/vnd.ms-excel"
CONTENT_TYPE_XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
CONTENT_TYPE_PDF = "application/pdf"
CONTENT_TYPE_ZIP = "application/zip"


def now_for_filename():
    return timezone.now().strftime("%y%m%d-%H%M%S")


def today_for_filename():
    return timezone.now().strftime("%y%m%d")


# HTTP RESPONSES ==============================================================

def download_response_factory(filename, content="", *args, **kwargs):
    response = HttpResponse(content, *args, **kwargs)
    response["Content-Disposition"] = "attachment; filename={}".format(filename)
    return response


def csv_download_response_factory(filename, content="", *args, **kwargs):
    kwargs["content_type"] = CONTENT_TYPE_CSV
    response = download_response_factory(filename, content=content, *args, **kwargs)
    return response


def xlsx_download_response_factory(filename, content="", *args, **kwargs):
    kwargs["content_type"] = CONTENT_TYPE_XLSX
    response = download_response_factory(filename, content=content, *args, **kwargs)
    return response


def pdf_download_response_factory(filename, content="", *args, **kwargs):
    kwargs["content_type"] = CONTENT_TYPE_PDF
    response = download_response_factory(filename, content=content, *args, **kwargs)
    return response
