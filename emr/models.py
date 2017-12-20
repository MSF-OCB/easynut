# -*- coding: utf-8 -*-
from collections import OrderedDict, Iterable
import re

from .utils import DataDb, Cast, clean_sql


DB_DATA_TABLE_NAME_FORMAT = "tabla_{}"
DB_CONFIG_TABLE_NAME_FORMAT = "tabla_{}_des"
DB_FIELD_NAME_FORMAT = "campo_{}"

RE_DATA_SLUG_VALIDATION = re.compile(r"^[0-9]{2}#[0-9]{2}$")
DATA_SLUG_SEPARATOR = "#"
DATA_SLUG_FORMAT = "{table_id:02d}#{field_id:02d}"

MSF_ID = "id"
MSF_ID_FIELD_NAME = "MSF ID"



class DynamicFieldConfig(object):
    """Dynamic field of a dynamic model (configured in a row of the model "config table")."""

    def __init__(self, model_config, attrs):
        self.model_config = model_config

        # Define field attributes.
        for k, v in attrs.iteritems():
            setattr(self, k, v)

    @property
    def data_slug(self):
        if self.name == MSF_ID_FIELD_NAME:
            return MSF_ID
        return DATA_SLUG_FORMAT.format(table_id=self.model_config.id, field_id=self.id)


class DynamicModelConfig(object):
    """Config of a dynamic model (configured in its model "config table")."""

    def __init__(self, attrs, data=None):
        # Define model attributes.
        for k, v in attrs.iteritems():
            setattr(self, k, v)

        # DB tables containing the model data and the fields config.
        self._db_data_table = DB_DATA_TABLE_NAME_FORMAT.format(self.id)
        self._db_config_table = DB_CONFIG_TABLE_NAME_FORMAT.format(self.id)
        self._msf_id_field_config = None

        # Initialize the fields config registry.
        self.fields_config = OrderedDict()
        self._load_fields_config()

        # Load initial data.
        if data is not None:
            self._load_data(data)


    def get_field_id_from_name(self, fieldname):
        # /!\ Dangerous use of ``DB_FIELD_NAME_FORMAT``.
        return Cast.int(fieldname.replace(DB_FIELD_NAME_FORMAT.format(""), ""))

    def save(self):
        """Save this record in DB (using an INSERT or UPDATE)."""
        raise NotImplemented()  # @TODO

    def delete(self):
        """Delete this record from DB ."""
        raise NotImplemented()  # @TODO

    def _load_fields_config(self):
        """Initialize model fields config."""
        # Build the query to retrieve the fields config.
        sql = clean_sql("""
            SELECT campo_id AS fieldname, presentador AS name, tipo AS kind, varios AS values_list,
                listado AS has_list, detalle AS has_detail, buscar AS has_find, usar AS has_use,
                nuevaLinea AS has_new_line, editable AS is_editable, pos AS position
            FROM {table}
            ORDER BY pos
        """.format(table=self._db_config_table))

        # Execute the query.
        with DataDb.execute(sql) as c:
            # If no record found, raise Exception.
            if c.rowcount == 0:
                if ids is None:
                    raise RuntimeError("No dynamic models found in database.")
                else:
                    raise AttributeError("No dynamic model found matching '{}'.".format(ids))

            # Loop over records.
            for row in c.fetchall():
                # Apply data conversion.
                self._cast_field_config_row(row)
                key = row["id"]
                # Create an instance of ``DynamicFieldConfig`` and store it in the fields config registry.
                self.fields_config[key] = DynamicFieldConfig(self, row)

                # Register MSF ID field config.
                if row["name"] == MSF_ID_FIELD_NAME:
                    self._msf_id_field_config = self.fields_config[key]

    def _cast_field_config_row(self, row):
        """Apply data conversion on the given field config."""
        row["id"] = self.get_field_id_from_name(row["fieldname"])
        row["kind"] = Cast.field_kind(row["kind"])
        row["values_list"] = Cast.csv(row["values_list"])
        row["has_list"] = Cast.bool(row["has_list"])
        row["has_detail"] = Cast.bool(row["has_detail"])
        row["has_find"] = Cast.bool(row["has_find"])
        row["has_use"] = Cast.bool(row["has_use"])
        row["has_new_line"] = Cast.bool(row["has_new_line"])
        row["is_editable"] = Cast.bool(row["is_editable"])
        row["position"] = Cast.int(row["position"])


class DynamicRegistry(object):
    """Registry of available dynamic models config (registered in the ``tablas`` table). This is a ``Singleton``."""
    # Singleton pattern: See right after this class definition for the ``Singleton`` implementation.

    def __init__(self):
        # Initialize the models config registry.
        self.models_config = OrderedDict()

        # Whether all models config have been loaded.
        self._all_models_config_loaded = False

    def load_models_config(self, ids=None):
        """Initialize all available dynamic models config, or given ones."""
        # Don't reload all models config if it has already been done.
        if ids is None and self._all_models_config_loaded:
            return

        # Build the query to retrieve the models config.
        sql = clean_sql("""
            SELECT CAST(tabla_id AS UNSIGNED) AS id, presentador AS name
            FROM tablas
            {where}
            ORDER BY id
        """.format(where=self._build_models_config_where(ids)))

        # Execute the query.
        with DataDb.execute(sql) as c:
            # If no record found, raise Exception.
            if c.rowcount == 0:
                if ids is None:
                    raise RuntimeError("No dynamic models found in database.")
                else:
                    raise AttributeError("No dynamic model found matching '{}'.".format(ids))

            # Loop over records.
            for row in c.fetchall():
                # Apply data conversion.
                self._cast_model_config_row(row)
                # Create an instance of ``DynamicModelConfig`` and store it in the models config registry.
                key = row["id"]
                self.models_config[key] = DynamicModelConfig(row)

        if ids is None:
            self._all_models_config_loaded = True

    def get_model_config(self, id):
        """Get a given dynamic model, loading it if not already available."""
        # If not yet available, load it.
        if id not in self.models_config:
            self.load_models_config(id)
        return self.models_config[id]

    def _build_models_config_where(self, ids):
        """Build the WHERE clause to retrieve dynamic models config as requested."""
        if ids is None:
            return ""
        where = "WHERE CAST(tabla_id AS UNSIGNED) "
        if isinstance(ids, Iterable):
            where += "IN ({})".format(", ".join(ids))
        else:
            where += "= {}".format(ids)
        return where

    def _cast_model_config_row(self, row):
        """Apply data conversion on the given model config."""
        row["id"] = Cast.int(row["id"])

    @staticmethod
    def get_db_table_name(model_id):
        """Return the name of the DB data table for the given ID."""
        return DB_DATA_TABLE_NAME_FORMAT.format(model_id)

    @staticmethod
    def get_db_field_name(field_id):
        """Return the name of the DB field for the given ID."""
        return DB_FIELD_NAME_FORMAT.format(field_id)

    @staticmethod
    def split_data_slug(data_slug):
        """Split the data slug into ``(table_id, field_id)``."""
        return [int(v) for v in data_slug.split(DATA_SLUG_SEPARATOR)]


# Singleton: Override class with its instance.
DynamicRegistry = DynamicRegistry()


# MODELS ======================================================================

class DynamicManager(object):

    def set_model(self, model):
        """Register the dynamic model with this manager."""
        self.model = model

    def all(self):
        """Return all records."""
        raise NotImplemented()  # @TODO

    def filter(self, **kwargs):
        """Return all records matching the given parameters."""
        raise NotImplemented()  # @TODO

    def get(self, **kwargs):
        """Return a single record matching the given parameters."""
        raise NotImplemented()  # @TODO

    def _build_sql(self, **kwargs):
        """Build a SQL query based on the given parameters."""
        raise NotImplemented()  # @TODO

    def _execute_sql(self, sql):
        """Execute the given SQL query."""
        raise NotImplemented()  # @TODO


class DynamicModel(object):

    objects = DynamicManager()

    def __init__(self, model=None):
        # Register this model with its manager.
        self.objects.set_model(self)
