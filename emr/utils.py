# -*- coding: utf-8 -*-
import json
import os
import re
from datetime import date, datetime

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.utils import six, timezone

import MySQLdb
import MySQLdb.converters
import MySQLdb.cursors


RE_CLEAN_SQL = re.compile("(\n +)+", re.MULTILINE)

# Data slug format and validation.
DATA_SLUG_SEPARATOR = "#"
DATA_SLUG_FORMAT = "{model_id:02d}#{field_id:02d}"
RE_DATA_SLUG_VALIDATION = re.compile(r"^[0-9]{2}#[0-9]{2}$")

# Format of date and date/time as returned by the database.
DB_DATE_FORMAT = "%Y-%m-%d"
DB_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

# See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Complete_list_of_MIME_types
CONTENT_TYPE_CSV = "text/csv"
CONTENT_TYPE_XLS = "application/vnd.ms-excel"
CONTENT_TYPE_XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
CONTENT_TYPE_PDF = "application/pdf"
CONTENT_TYPE_ZIP = "application/zip"


def force_list(value, string_separator=","):
    """Force the value to be a list of values."""
    if isinstance(value, six.string_types) and string_separator is not None:
        return value.split(string_separator)
    if type(value) not in (list, tuple):
        return [value]
    return value


def insert_filename_pre_extension(filename, pre_ext):
    """Insert a pre-extension in a filename, just before the file extension."""
    # Split filename and extension. /!\ The extension contains the/starts with a ".".
    filename, ext = os.path.splitext(os.path.basename(filename))

    # Ensure the pre-extension starts with a ".".
    if not pre_ext.startswith("."):
        pre_ext = "." + pre_ext

    # Insert pre-extension between the filename and the extension.
    return "{}{}{}".format(filename, pre_ext, ext)


def is_data_slug(value):
    """Return whether the value is a data slug."""
    return value is not None and RE_DATA_SLUG_VALIDATION.match(value) is not None


def now_for_filename():
    """Return a string representation of "now" for filenames."""
    return timezone.now().strftime("%y%m%d-%H%M%S")


def today_for_filename():
    """Return a string representation of "today" for filenames."""
    return timezone.now().strftime("%y%m%d")


# DATABASE ====================================================================

def get_db(name="data"):
    """Return a DB connection for the given name defined in Django settings."""
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
    """Clean a SQL statement to a one-line string."""
    return RE_CLEAN_SQL.sub(" ", sql).strip()


class DbExecute(object):
    """Allow to execute a query in a cursor using the ``with`` statement."""

    def __init__(self, db, sql):
        self._db = db
        self._sql = sql
        self._cursor = None

    def __enter__(self):
        """Initialize the ``with`` statement."""
        self._cursor = self._db.cursor()
        self._cursor.execute(self._sql)
        return self._cursor

    def __exit__(self, type, value, traceback):
        """Exit properly the ``with`` statement."""
        self._cursor.close()


class DataDb(object):
    """Default connection to the "data" DB. This is a ``Singleton``."""

    # Note: See right after this class definition for the ``Singleton`` implementation.

    def __init__(self):
        self._db = get_db("data")

    def __getattr__(self, name):
        """Provide convenient access to DB connection attributes."""
        if hasattr(self._db, name):
            return getattr(self._db, name)

    def execute(self, sql):
        """
        Execute a query on the "data DB, in a cursor, closing it afterward.

        Usage: ``with DataDb.execute(sql) as c:``
        """
        return DbExecute(self._db, sql)


# Singleton: Override class with its instance.
DataDb = DataDb()


# CAST VALUES =================================================================

class Cast(object):
    """Convert a DB value into its Python value."""

    @staticmethod
    def bool(value):
        """Convert boolean values."""
        if value is None or isinstance(value, bool):
            return value
        val = str(value).lower()
        if val in ("true", "t", "yes", "y", "1"):
            return True
        if val in ("false", "f", "no", "n", "0"):
            return False
        raise ValueError("Wrong boolean value: '{}'.".format(value))

    @staticmethod
    def csv(value, string_separator=","):
        """Convert list of values separated by a ``string_separator``."""
        if not value or type(value) in (list, tuple):
            return value
        if isinstance(value, six.string_types) and string_separator is not None:
            return [v.strip() for v in value.split(string_separator)]
        raise ValueError("Wrong CSV value: '{}'.".format(value))

    @staticmethod
    def date(value):
        """Convert date values."""
        if value is None or isinstance(value, date):
            return value
        return datetime.strptime(value, DB_DATE_FORMAT).date()

    @staticmethod
    def datetime(value):
        """Convert datetime values."""
        if value is None or isinstance(value, datetime):
            return value
        return datetime.strptime(value, DB_DATETIME_FORMAT)

    @staticmethod
    def field_kind(kind):
        """Convert field type from Spanish to English."""
        mapping = {
            "fecha": "date",
            "entero": "int",
            "texto": "text",
            "select": "select",
            "notes": "notes",
            "radio": "radio",
        }
        return mapping[kind] if kind in mapping else kind

    @staticmethod
    def int(value):
        """Convert integer values."""
        if value is None:
            return value
        return int(value)


# HTTP RESPONSES ==============================================================

def download_response_factory(filename, content="", *args, **kwargs):
    """Return an ``HttpResponse`` that triggers a file download in the browser."""
    response = HttpResponse(content, *args, **kwargs)
    response["Content-Disposition"] = "attachment; filename={}".format(filename)
    return response


def csv_download_response_factory(filename, content="", *args, **kwargs):
    """Return a downlaod response for CSV files."""
    kwargs["content_type"] = CONTENT_TYPE_CSV
    response = download_response_factory(filename, content=content, *args, **kwargs)
    return response


def xlsx_download_response_factory(filename, content="", *args, **kwargs):
    """Return a downlaod response for Excel (.xlsx) files."""
    kwargs["content_type"] = CONTENT_TYPE_XLSX
    response = download_response_factory(filename, content=content, *args, **kwargs)
    return response


def pdf_download_response_factory(filename, content="", *args, **kwargs):
    """Return a downlaod response for PDF files."""
    kwargs["content_type"] = CONTENT_TYPE_PDF
    response = download_response_factory(filename, content=content, *args, **kwargs)
    return response


# DEBUGGING ===================================================================

def debug(label, var):
    """Print debug information."""
    try:
        print label, json.dumps(var, indent=2, cls=DjangoJSONEncoder)
    except Exception:
        print label, var
