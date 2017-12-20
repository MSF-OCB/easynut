# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone

import MySQLdb
import MySQLdb.converters
import MySQLdb.cursors


RE_CLEAN_SQL = re.compile("[ \n]+", re.MULTILINE)

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


# DATABASE ====================================================================

def get_db(name="data"):
    if name not in settings.DATABASES:
        raise AttributeError("Database '{}' is not defined in settings.".format(name))

    conv = MySQLdb.converters.conversions.copy()
    conv[246] = float  # Convert decimals to floats.
    conv[10] = str  # Convert dates.

    db = MySQLdb.connect(
        settings.DATABASES[name]["HOST"],
        settings.DATABASES[name]["USER"],
        settings.DATABASES[name]["PASSWORD"],
        settings.DATABASES[name]["NAME"],
        conv=conv,
        cursorclass=MySQLdb.cursors.DictCursor,
    )
    return db


def clean_sql(sql):
    return RE_CLEAN_SQL.sub(" ", sql).strip()


# CAST VALUES =================================================================

class Cast(object):

    @staticmethod
    def bool(value):
        return value == "true"

    @staticmethod
    def int(value):
        return int(value)

    @staticmethod
    def csv(values):
        if values:
            return [v.strip() for v in values.split(",")]
        return None

    @staticmethod
    def field_kind(kind):
        mapping = {
            "fecha": "date",
            "entero": "int",
            "texto": "text",
            "select": "select",
            "notes": "notes",
            "radio": "radio",
        }
        return mapping[kind] if kind in mapping else kind


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


# Default instance of connection to the "data" database.
DATA_DB = get_db()
