# -*- coding: utf-8 -*-
from collections import OrderedDict, Iterable
import re

from .utils import DataDb, Cast, clean_sql, force_list


DB_DATA_TABLE_NAME_FORMAT = "tabla_{}"
DB_CONFIG_TABLE_NAME_FORMAT = "tabla_{}_des"
DB_FIELD_NAME_FORMAT = "campo_{}"
RE_DB_FIELD_NAME_VALIDATION = re.compile(r"^campo_[0-9]+$")
NON_DYNAMIC_DB_FIELD_NAMES = ("_id", "user", "timestamp")

RE_DATA_SLUG_VALIDATION = re.compile(r"^[0-9]{2}#[0-9]{2}$")
DATA_SLUG_SEPARATOR = "#"
DATA_SLUG_FORMAT = "{table_id:02d}#{field_id:02d}"

MSF_ID = "id"
MSF_ID_FIELD_NAME = "MSF ID"


class DynamicManager(object):

    def __init__(self, model_config):
        self.model_config = model_config  # The model config registered with this manager.

    def all(self):
        """Return all records."""
        sql = self.model_config.build_sql()
        print "SQL:", sql  # @DEBUG
        return self._generate_models(sql)

    def filter(self, **kwargs):
        """Return all records matching the given parameters."""
        raise NotImplemented()  # @TODO

    def get(self, **kwargs):
        """Return a single record matching the given parameters."""
        raise NotImplemented()  # @TODO

    def _generate_models(self, sql):
        """Generate models list using the given SQL query."""
        models = []
        with DataDb.execute(sql) as c:
            for row in c.fetchall():
                print "row:", row  # @DEBUG
                model = self.model_config.model_factory(row)
                models.append(model)
        return models


class DynamicModel(object):

    def __init__(self, table_id):
        self.table_id = table_id

        self._model_config = DynamicRegistry.get_model_config(table_id)
        self.fields = OrderedDict()

        for fieldname in NON_DYNAMIC_DB_FIELD_NAMES:
            setattr(self, fieldname, None)

    def get_field(self, id):
        return self.fields[id]

    def get_field_config(self, id):
        return self._model_config.fields_config[id]

    def load_data(self, data):
        for fieldname, value in data.iteritems():
            if fieldname in NON_DYNAMIC_DB_FIELD_NAMES:
                setattr(self, fieldname, value)
            else:
                field_id = self._model_config.get_field_id_from_name(fieldname)
                if field_id in self._model_config.fields_config:
                    self.fields[field_id] = value


class DynamicFieldConfig(object):
    """Dynamic field of a dynamic model (configured in a row of the model "config table")."""

    def __init__(self, model_config, attrs):
        self.model_config = model_config

        # Define field attributes: fieldname, name, position, kind, values_list,
        #     has_list, has_detail, has_find, has_use, has_new_line, is_editable.
        # Note: Attributes are retrieved in ``DynamicModelConfig._load_fields_config()``.
        for k, v in attrs.iteritems():
            setattr(self, k, v)

    @property
    def data_slug(self):
        # if self.name == MSF_ID_FIELD_NAME:
        #     return MSF_ID
        return DATA_SLUG_FORMAT.format(table_id=self.model_config.id, field_id=self.id)


class DynamicModelConfig(object):
    """Config of a dynamic model (configured in its model "config table")."""

    def __init__(self, attrs, data=None):
        # Define model attributes: id, name.
        # Note: Attributes are retrieved in ``DynamicRegistry.load_models_config()``.
        for k, v in attrs.iteritems():
            setattr(self, k, v)

        # DB tables containing the model data and the fields config.
        self._db_data_table = DB_DATA_TABLE_NAME_FORMAT.format(self.id)
        self._db_config_table = DB_CONFIG_TABLE_NAME_FORMAT.format(self.id)
        self._msf_id_field_config = None

        # Initialize the fields config registry.
        self.fields_config = OrderedDict()
        self._load_fields_config()

        # Create an instance of the manager and register ourself with it.
        self.objects = DynamicManager(self)

        # Load initial data.
        if data is not None:
            self._load_data(data)

    @property
    def msf_id_db_field_name(self):
        if self._msf_id_field_config is None:
            return None
        return self._msf_id_field_config.fieldname

    def build_sql(self, fields=["*"], where=None, **kwargs):
        """Build a SQL query based on the given parameters."""
        where_clause = "" if where is None else "WHERE " + where
        sql = clean_sql("""
            SELECT {fields}
            FROM {table}
            {where_clause}
        """.format(
            fields=", ".join(force_list(fields)),
            table=self._db_data_table,
            where_clause=where_clause,
        ))
        sql += " LIMIT 10"  # @DEBUG
        return sql

    def delete(self):
        """Delete this record from DB ."""
        raise NotImplemented()  # @TODO

    def get_field_config(self, id):
        """Get a given dynamic field config."""
        return self.fields_config[id]

    def get_field_id_from_name(self, fieldname):
        # /!\ Dangerous use of ``DB_FIELD_NAME_FORMAT``.
        return Cast.int(fieldname.replace(DB_FIELD_NAME_FORMAT.format(""), ""))

    def model_factory(self, row):
        model = DynamicModel(self.id)
        model.load_data(row)
        return model

    def save(self):
        """Save this record in DB (using an INSERT or UPDATE)."""
        raise NotImplemented()  # @TODO

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

    def _load_fields_config(self):
        """Initialize model fields config."""
        # Build the query to retrieve the fields config.
        sql = clean_sql("""
            SELECT campo_id AS fieldname, presentador AS name,
                pos AS position, tipo AS kind, varios AS values_list,
                listado AS has_list, detalle AS has_detail, buscar AS has_find, usar AS has_use,
                nuevaLinea AS has_new_line, editable AS is_editable
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


class DynamicRegistry(object):
    """Registry of available dynamic models config (registered in the ``tablas`` table). This is a ``Singleton``."""
    # Singleton pattern: See right after this class definition for the ``Singleton`` implementation.

    def __init__(self):
        # Initialize the models config registry.
        self.models_config = OrderedDict()

        # Whether all models config have been loaded.
        self._all_models_config_loaded = False

    def build_sql(self, tables_fields):
        """Build a SQL query based on the given parameters."""
        if len(tables_fields) == 0:
            raise Exception("tables_fields is empty.")

        select_fields = []
        from_clause = ""
        main_table = None
        main_pk_field = None

        for model_id, field_ids in tables_fields.iteritems():
            table_name = self.get_db_table_name(model_id)
            pk_field = self.get_msf_id_db_field_name(model_id)
            if main_table is None:
                main_table = table_name
                main_pk_field = pk_field
                from_clause = "FROM {}".format(table_name)
            else:
                from_clause += " LEFT JOIN {table} ON {table}.{pk_field}={main_table}.{main_pk_field}".format(
                    table=table_name, pk_field=pk_field,
                    main_table=main_table, main_pk_field=main_pk_field,
                )

            for field_id in field_ids:
                field_name = self.get_db_field_name(field_id)
                data_slug = self.data_slug(model_id, field_id)
                data_slug = self.get_data_slug(model_id, field_id)
                select_fields.append("{}.{} AS `{}`".format(table_name, field_name, data_slug))

        sql = clean_sql("""
            SELECT {fields}
            {from_clause}
            ORDER BY {main_table}.{main_pk_field}
        """.format(
            fields=", ".join(select_fields), from_clause=from_clause,
            main_table=main_table, main_pk_field=main_pk_field,
        ))
        return sql

    def get_data_slug(self, model_id, field_id):
        field_config = self.get_field_config(model_id, field_id)
        return field_config.data_slug

    def get_db_field_name(self, field_id):
        """Return the name of the DB field for the given ID."""
        return DB_FIELD_NAME_FORMAT.format(field_id)

    def get_db_table_name(self, model_id):
        """Return the name of the DB data table for the given ID."""
        # return self.models_config[model_id]._db_data_table
        return DB_DATA_TABLE_NAME_FORMAT.format(model_id)

    def get_field_config(self, model_id, field_id):
        """Get a given dynamic field config."""
        model_config = self.get_model_config(model_id)
        return model_config.get_field_config(field_id)

    def get_model_config(self, id):
        """Get a given dynamic model config, loading it if not already available."""
        # If not yet available, load it.
        if id not in self.models_config:
            self.load_models_config(id)
        return self.models_config[id]

    def get_msf_id_db_field_name(self, model_id):
        """Return the name of the "MSF ID" DB field for the given model ID."""
        model_config = self.get_model_config(model_id)
        return model_config.msf_id_db_field_name

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

    def split_data_slug(self, data_slug):
        """Split the data slug into ``(table_id, field_id)``."""
        return [int(v) for v in data_slug.split(DATA_SLUG_SEPARATOR)]

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


# Singleton: Override class with its instance.
DynamicRegistry = DynamicRegistry()
