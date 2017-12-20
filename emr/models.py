# -*- coding: utf-8 -*-
from collections import OrderedDict, Iterable

from .utils import DataDb, Cast, clean_sql


DB_DATA_TABLE_NAME_FORMAT = "tabla_{}"
DB_CONFIG_TABLE_NAME_FORMAT = "tabla_{}_des"
DB_FIELD_NAME_FORMAT = "campo_{}"



# MODELS CONFIG ===============================================================

class DynamicFieldConfig(object):
    """Dynamic field of a dynamic model (configured in a row of the model "config table")."""

    def __init__(self, model_config, attrs):
        self.model_config = model_config

        # Define field attributes.
        for k, v in attrs.iteritems():
            setattr(self, k, v)


class DynamicManager(object):

    def __init__(self, model=None):
        self.model = model  # The model registered with this manager.

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
        self.value = None


class DynamicModelConfig(object):
    """Config of a dynamic model (configured in its model "config table")."""

    def __init__(self, attrs, data=None):
        # Define model attributes.
        for k, v in attrs.iteritems():
            setattr(self, k, v)

        # DB tables containing the model data and the fields config.

        # Create an instance of the manager and register ourself with it.
        self.objects = DynamicManager(self)
        self._db_data_table = DB_DATA_TABLE_NAME_FORMAT.format(self.id)
        self._db_config_table = DB_CONFIG_TABLE_NAME_FORMAT.format(self.id)

        # Initialize the fields registry.
        self.fields = OrderedDict()
        self._load_fields()

        # Load initial data.
        if data is not None:
            self._load_data(data)

    def get_field(self, id):
        """Get a given dynamic field, loading it if not already available."""
        return self.fields[id]

    def save(self):
        """Save this record in DB (using an INSERT or UPDATE)."""
        raise NotImplemented()  # @TODO

    def delete(self):
        """Delete this record from DB ."""
        raise NotImplemented()  # @TODO

    def _load_fields(self):
        """Initialize model fields."""
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
                # Create an instance of ``DynamicFieldConfig`` and store it in the fields registry.
                self.fields[key] = DynamicFieldConfig(self, row)

    def _cast_field_config_row(self, row):
        """Apply data conversion on the given field config."""
        row["kind"] = Cast.field_kind(row["kind"])
        row["values_list"] = Cast.csv(row["values_list"])
        row["has_list"] = Cast.bool(row["has_list"])
        row["has_detail"] = Cast.bool(row["has_detail"])
        row["has_find"] = Cast.bool(row["has_find"])
        row["has_use"] = Cast.bool(row["has_use"])
        row["has_new_line"] = Cast.bool(row["has_new_line"])
        row["is_editable"] = Cast.bool(row["is_editable"])
        row["position"] = Cast.int(row["position"])

        # /!\ Dangerous use of ``DB_FIELD_NAME_FORMAT``.
        row["id"] = Cast.int(row["fieldname"].replace(DB_FIELD_NAME_FORMAT.format(""), ""))


class DynamicRegistry(object):
    """Registry of available dynamic models (registered in the ``tablas`` table). This is a ``Singleton``."""
    # Singleton pattern: See right after this class definition for the ``Singleton`` implementation.

    def __init__(self):
        # Initialize the models registry.
        self.models = OrderedDict()

    def load_models(self, ids=None):
        """Initialize all available dynamic models, or given ones."""
        # Build the query to retrieve the models config.
        sql = clean_sql("""
            SELECT CAST(tabla_id AS UNSIGNED) AS id, presentador AS name
            FROM tablas
            {where}
            ORDER BY id
        """.format(where=self._build_models_where(ids)))

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
                # Create an instance of ``DynamicModelConfig`` and store it in the models registry.
                key = row["id"]
                self.models[key] = DynamicModelConfig(row)

    def get_model(self, id):
        """Get a given dynamic model, loading it if not already available."""
        # If not yet available, load it.
        if id not in self.models:
            self.load_models(id)
        return self.models[id]

    def _build_models_where(self, ids):
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


# Singleton: Override class with its instance.
DynamicRegistry = DynamicRegistry()
