# -*- coding: utf-8 -*-
"""
Dynamic database structure.

Terminology:
- Table/Column: Used when we talk about DB objects.
- Model/Field: Used when we talk about Python objects.
- Model/Table ID: Unique identifier of a model/table (they both have the same value).
- Field/Column ID: Unique identifier of a field/column (they both have the same value).
- Dynamic model/field: Model/field having its structure defined in the database.
- Non dynamic field: A field that is not dynamic, that is hardcoded in the DB table.
- DynamicRegistry: Centralize operations related to dynamic models stored in the database.
- DynamicModelConfig: Config information of a dynamic model.
- DynamicFieldConfig: Config information of a dynamic field.
- DynamicModel: Simulate a Django Model (i.e. fields and behaviors of the data stored in the database).
- DynamicManager: Simulate a Django Manager (i.e. interface through which database operations are provided to models).
- Data slug: A unique identifier for a ``model.field`` (used in Excel templates).
- Special fields: Dynamic DB columns that have special meaning/usage.
"""
from collections import Iterable, OrderedDict
from copy import copy

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from .utils import DATA_SLUG_FORMAT, DATA_SLUG_SEPARATOR, Cast, DataDb, clean_sql, force_list


# Format of dynamic tables (data and config) and dynamic columns.
DYNAMIC_REGISTRY_DB_CONFIG_TABLE_NAME_FORMAT = "tablas"
DYNAMIC_MODEL_DB_DATA_TABLE_NAME_FORMAT = "tabla_{}"
DYNAMIC_MODEL_DB_CONFIG_TABLE_NAME_FORMAT = "tabla_{}_des"
DYNAMIC_FIELD_DB_COL_NAME_FORMAT = "campo_{}"

# DB column names of non dynamic fields.
NON_DYNAMIC_FIELDS_DB_COL_NAMES = ("_id", "user", "timestamp")

# DB column name of the primary key in DB tables ``tabla_X``).
PK_DB_COL_NAME = "_id"


# MODELS ======================================================================

class DynamicManager(object):
    """
    Simulate Django Managers for ``DynamicModel``.

    From Django: A Manager is the interface through which database query operations are provided to Django models.
    """

    def __init__(self, model_config):
        self.model_config = model_config  # The model config registered with this manager.

    def all(self):
        """Return all records."""
        sql = self._build_sql()
        return self._generate_models(sql)

    def filter(self, msf_id):
        """Return all records matching the given MSF ID."""
        where = "{}='{}'".format(self.model_config.msf_id_db_col_name, msf_id)
        sql = self._build_sql(where=where)
        return self._generate_models(sql)

    def get(self, pk=None, msf_id=None):
        """Return a single record matching the pk or MSF ID."""
        # Build the WHERE content (without the actual "WHERE", see ``self._build_sql()``).
        if pk:
            where = "{}={}".format(PK_DB_COL_NAME, pk)
        elif msf_id:
            where = "{}='{}'".format(self.model_config.msf_id_db_col_name, msf_id)
        else:
            raise Exception("You must provide either a pk or MSFID.")

        # Build the SQL statement.
        sql = self._build_sql(where=where)

        # Execute the query.
        with DataDb.execute(sql) as c:
            # Raise an exception if no record found or multiple records found.
            if c.rowcount == 0:
                raise ObjectDoesNotExist()
            if c.rowcount > 1:
                raise MultipleObjectsReturned()

            row = c.fetchone()

        return self._generate_model(row)

    def _build_sql(self, db_cols=["*"], where=None, **kwargs):
        """Build a SQL query based on the given parameters."""
        # Build the WHERE clause.
        where_clause = ""
        if where is not None:
            where_clause = "WHERE {}".format(where)

        # Sort results by MSF ID, then by date if that column exists.
        # Remark: We don't use the sorting defined in the ``DYNAMIC_REGISTRY_DB_CONFIG_TABLE_NAME_FORMAT``.
        # That table defines the ORDER BY in its DB columns ``orden`` (DB col name) and ``orden_sen`` (ASC/DESC).
        order_by = [self.model_config.msf_id_db_col_name]
        if self.model_config.date_db_col_name is not None:
            order_by.append("{} DESC".format(self.model_config.date_db_col_name))

        # Build the SQL statement.
        sql = clean_sql("""
            SELECT {cols}
            FROM {table}
            {where_clause}
            ORDER BY {order_by}
        """.format(
            cols=", ".join(force_list(db_cols)),
            table=self.model_config.db_data_table,
            where_clause=where_clause,
            order_by=", ".join(order_by),
        ))
        return sql

    def _generate_model(self, data_row):
        """Generate a model using the given data."""
        return self.model_config.model_factory(data_row=data_row)

    def _generate_models(self, sql):
        """Generate models list using the given SQL query."""
        models = []
        with DataDb.execute(sql) as c:
            for row in c.fetchall():
                models.append(self._generate_model(row))
        return models


class DynamicModel(object):
    """
    Simulate Django Models for dynamic DB tables.

    From Django: A model is the single, definitive source of information about your data. It contains the essential
    fields and behaviors of the data you're storing. Generally, each model maps to a single database table.
    """

    def __init__(self, model_id):
        self.model_id = model_id  # ID of the ``DynamicModelConfig``.

        self.model_config = DynamicRegistry.get_model_config(model_id)  # Link to the ``DynamicModelConfig``.
        self.fields_value = OrderedDict()  # Fields value.
        self.related_models = {}  # Cache of related models.

        # Initialize non dymanic fields to ``None``.
        for db_col_name in NON_DYNAMIC_FIELDS_DB_COL_NAMES:
            setattr(self, db_col_name, None)

    @property
    def pk(self):
        """Provide convenient access to the DB primary key."""
        return getattr(self, PK_DB_COL_NAME)

    @property
    def msf_id(self):
        """Provide convenient access to the special field ``MSF ID``."""
        return self.get_field_value(self.model_config.msf_id_field_id)

    @property
    def date(self):
        """Provide convenient access to the special field ``Date``."""
        return self.get_field_value(self.model_config.date_field_id)

    def get_field_value(self, field_id):
        """Return the value of a field based on its ID."""
        return self.fields_value[field_id]

    def get_field_config(self, field_id):
        """Return the ``DynamicFieldConfig`` of a field based on its ID."""
        return self.model_config.fields_config[field_id]

    def get_related_models(self, model_id):
        """Return related models for the given model ID, loading it if not already available."""
        if model_id not in self.related_models:
            self.load_related_models(model_id)
        return self.related_models[model_id]

    def get_value_from_data_slug(self, data_slug):
        """Return the field value based on a data slug, for this model or a related one."""
        model_id, field_id = DynamicRegistry.split_data_slug(data_slug)
        if model_id == self.model_id:
            return self.get_field_value(field_id)

        # Retrieve data for the related model (as a list of ``DynamicModel``).
        related_models = self.get_related_models(model_id)

        # Return a simple list of values for the given field.
        return [m.get_field_value(field_id) for m in related_models]

    def load_data(self, data_row):
        """Initialize model fields value based on a DB row."""
        # Convert DB values to Python values.
        cleaned_data = self._from_db_values(data_row)

        # Loop over cleaned data.
        for db_col_name, value in cleaned_data.iteritems():
            # Retrieve the field ID based on the DB col name.
            field_id = self.model_config.get_field_id_from_db_col_name(db_col_name)

            # Set non dynamic field.
            if field_id is None:
                setattr(self, db_col_name, value)
            # Set dynamic field.
            else:
                self.fields_value[field_id] = value

    def load_related_models(self, model_id):
        """Load data for the same MSF ID from another model."""
        model_config = DynamicRegistry.get_model_config(model_id)
        self.related_models[model_id] = model_config.objects.filter(msf_id=self.msf_id)

    def set_field_value(self, field_id, value):
        """Set the value of a field based on its ID."""
        self.fields_value[field_id] = value

    def _from_db_values(self, data_row):
        """Convert values of a DB record into Python values."""
        clean_data = {}
        for db_col_name, value in data_row.iteritems():
            field_id = self.model_config.get_field_id_from_db_col_name(db_col_name)

            # Convert non dynamic field (via ``DynamicModelConfig``).
            if field_id is None:
                clean_data[db_col_name] = self.model_config.from_db_value_non_dynamic(db_col_name, value)
            # Convert dynamic field (via ``DynamicFieldConfig``).
            else:
                field_config = self.get_field_config(field_id)
                clean_data[db_col_name] = field_config.from_db_value(value)
        return clean_data


# MODELS CONFIG ===============================================================

class DynamicFieldConfig(object):
    """
    Config of a dynamic field, of a dynamic model.

    Config information stored in the ``DYNAMIC_MODEL_DB_CONFIG_TABLE_NAME_FORMAT`` DB table.
    """

    # Available field types.
    KIND_BOOL = "bool"
    KIND_DATE = "date"
    KIND_INT = "int"
    KIND_NOTES = "notes"
    KIND_RADIO = "radio"
    KIND_SELECT = "select"
    KIND_TEXT = "text"

    def __init__(self, field_id, model_config, attrs):
        self.id = field_id
        self.model_config = model_config  # Link to the parent ``DynamicModelConfig``.

        # Define field attributes: db_col_name, name, position, kind, values_list,
        #     has_list, has_detail, has_find, has_use, has_new_line, is_editable, is_sensitive.
        # Note: Attributes are retrieved in ``DynamicModelConfig._load_fields_config()``.
        for k, v in attrs.iteritems():
            setattr(self, k, v)

        # Define special fields flag.
        self.is_msf_id = self.model_config.msf_id_field_id == field_id
        self.is_date = self.model_config.date_field_id == field_id

    @property
    def data_slug(self):
        """Return the data slug of the current ``model.field``."""
        return DATA_SLUG_FORMAT.format(model_id=self.model_config.id, field_id=self.id)

    @property
    def full_db_col_name(self):
        """Return the full DB col name for SQL queries (as ``table.column``)."""
        return "{}.{}".format(self.model_config.db_data_table, self.db_col_name)

    def from_db_value(self, value):
        """Convert a DB value for this field into its Python value."""
        if value is None:
            return value
        # Type ``radio`` with Yes/No values should be defined as ``bool``.
        if self.kind == self.KIND_BOOL:
            return Cast.bool(value)
        if self.kind == self.KIND_DATE:
            return Cast.date(value)
        if self.kind == self.KIND_INT:
            return Cast.int(value)
        return value

    def to_db_value(self, value):
        """Convert a Python value for this field into its DB value."""
        raise NotImplemented()


class DynamicModelConfig(object):
    """
    Config of a dynamic model.

    Config information stored in the ``DYNAMIC_REGISTRY_DB_CONFIG_TABLE_NAME_FORMAT`` DB table.
    """

    def __init__(self, model_id, attrs, data_row=None):
        self.id = model_id  # Model ID.

        # Define model attributes: name, position, is_main_table, is_main_join_table, msf_id_field_id, date_field_id.
        # Note: Attributes are retrieved in ``DynamicRegistry.load_models_config()``.
        for k, v in attrs.iteritems():
            setattr(self, k, v)

        # DB tables containing the model fields config and the data.
        self.db_config_table = DynamicRegistry.get_db_config_table_name(self.id)
        self.db_data_table = DynamicRegistry.get_db_data_table_name(self.id)

        # Initialize the fields config registry.
        self.fields_config = OrderedDict()
        self.db_col_names_mapping = {}  # DB col name to field ID mapping.
        self._load_fields_config()

        # Create an instance of the manager and register this model config with it.
        self.objects = DynamicManager(self)

        # Load initial data.
        if data_row is not None:
            self._load_data(data_row)

    @property
    def date_db_col_name(self):
        """Provide convenient access to the DB col name of the special field ``Date``."""
        field_config = self.date_field_config
        if field_config is None:
            return None
        return field_config.db_col_name

    @property
    def date_field_config(self):
        """Provide convenient access to the ``FieldConfig`` of the special field ``Date``."""
        if self.date_field_id is None:
            return None
        return self.get_field_config(self.date_field_id)

    @property
    def msf_id_db_col_name(self):
        """Provide convenient access to the DB col name of the special field ``MSF ID``."""
        field_config = self.msf_id_field_config
        if field_config is None:
            return None
        return field_config.db_col_name

    @property
    def msf_id_field_config(self):
        """Provide convenient access to the ``FieldConfig`` of the special field ``MSF ID``."""
        if self.msf_id_field_id is None:
            return None
        return self.get_field_config(self.msf_id_field_id)

    def delete(self):
        """Delete this record from DB."""
        raise NotImplemented()  # @TODO

    def from_db_value_non_dynamic(self, db_col_name, value):
        """Convert the DB value of a non dynamic field into its Python value."""
        if value is None:
            return value

        if db_col_name == "_id":
            return Cast.int(value)
        if db_col_name == "user":
            return value
        if db_col_name == "timestamp":
            return Cast.datetime(value)

        raise ValueError("'{}' is not a non dynamic field.".format(db_col_name))

    def get_field_config(self, field_id):
        """Return the config of a field based on its ID."""
        return self.fields_config[field_id]

    def get_field_id_from_db_col_name(self, db_col_name):
        """
        Return the field ID from its DB col name.

        If the DB col name is not in the mapping, it means it's a non dynamic field.
        """
        return self.db_col_names_mapping.get(db_col_name, None)

    def get_order_by_cols_names(self):
        """Return the full DB cols names to be used in ORDER BY clause for this model."""
        db_cols_names = [self.msf_id_field_config.full_db_col_name]
        if self.date_field_id is not None:
            db_cols_names.append(self.date_field_config.full_db_col_name)
        return db_cols_names

    def get_sql_join_clause(self, main_model_config, main_join_model_config, kind="LEFT JOIN"):
        """Return the SQL JOIN clause for this model."""
        condition_cols = []

        # Build the mapping for MSF ID.
        condition_cols.append(
            "{}={}".format(
                self.msf_id_field_config.full_db_col_name,
                main_model_config.msf_id_field_config.full_db_col_name,
            )
        )

        # If there's a Date, build the mapping for it.
        if self.date_field_id is not None:
            condition_cols.append(
                "{}={}".format(
                    self.date_field_config.full_db_col_name,
                    main_join_model_config.date_field_config.full_db_col_name,
                )
            )

        # Build the JOIN clause.
        join_clause = clean_sql("""
            {kind} {table} ON ({condition})
        """.format(
            kind=kind.upper(),
            table=self.db_data_table,
            condition=" AND ".join(condition_cols),
        ))

        return join_clause

    def model_factory(self, data_row=None):
        """Create a dynamic model for this model config, and load data if provided."""
        model = DynamicModel(self.id)
        if data_row is not None:
            model.load_data(data_row)
        return model

    def save(self):
        """Save this record in DB (using an INSERT or UPDATE)."""
        raise NotImplemented()  # @TODO

    def _from_db_values_field_config(self, row):
        """Convert DB values of a field config into their Python values."""
        cleaned_data = copy(row)
        cleaned_data["id"] = Cast.int(row["id"])
        cleaned_data["position"] = Cast.int(row["position"])
        cleaned_data["kind"] = Cast.field_kind(row["kind"])
        cleaned_data["values_list"] = Cast.csv(row["values_list"])
        cleaned_data["has_list"] = Cast.bool(row["has_list"])
        cleaned_data["has_detail"] = Cast.bool(row["has_detail"])
        cleaned_data["has_find"] = Cast.bool(row["has_find"])
        cleaned_data["has_use"] = Cast.bool(row["has_use"])
        cleaned_data["has_new_line"] = Cast.bool(row["has_new_line"])
        cleaned_data["is_editable"] = Cast.bool(row["is_editable"])
        cleaned_data["is_sensitive"] = Cast.bool(row["is_sensitive"])
        return cleaned_data

    def _load_fields_config(self):
        """Initialize model fields config."""
        # Build the query to retrieve the fields config.
        sql = clean_sql("""
            SELECT campo_id AS id,
                campo AS db_col_name,
                presentador AS name,
                pos AS position,
                tipo AS kind,
                varios AS values_list,
                listado AS has_list,
                detalle AS has_detail,
                buscar AS has_find,
                usar AS has_use,
                nuevaLinea AS has_new_line,
                editable AS is_editable,
                is_sensitive
            FROM {table}
            ORDER BY pos
        """.format(table=self.db_config_table))

        # Execute the query.
        with DataDb.execute(sql) as c:
            # If no record found, raise Exception.
            if c.rowcount == 0:
                raise RuntimeError(
                    "No dynamic fields config found in database for this model (ID: {}).".format(self.id)
                )

            # Loop over records.
            for row in c.fetchall():
                # Convert DB values into their Python values.
                cleaned_data = self._from_db_values_field_config(row)

                # Create an instance of ``DynamicFieldConfig`` and store it in the fields config registry.
                field_id = cleaned_data.pop("id")
                self.fields_config[field_id] = DynamicFieldConfig(field_id, self, cleaned_data)

                # Register DB col name to field ID mapping.
                db_col_name = self.fields_config[field_id].db_col_name
                self.db_col_names_mapping[db_col_name] = field_id


class DynamicRegistry(object):
    """Registry of available dynamic models. This is a ``Singleton``."""

    # Note: See right after this class definition for the ``Singleton`` implementation.

    def __init__(self):
        # Initialize the models config registry.
        self.models_config = OrderedDict()

        # Model config of the main tables.
        self.main_model_config = None
        self.main_join_model_config = None

        # Whether all models config have been loaded.
        self._all_models_config_loaded = False

    def build_sql(self, models_fields):
        """
        Build a SQL query based on the given list of required models and fields.

        Args:
            models_fields: Format = ``{model_id: [field_id, ...]}``.
        """
        # Check that the given config is not empty.
        if len(models_fields) == 0:
            raise Exception("The `models_fields` config is empty.")

        # Ensure the dynamic registry is initialized.
        self.init()

        # Column names for the SELECT clause.
        select_cols = []

        # If the main model is in the required models, use it, else use the first model.
        if self.main_model_config.id in models_fields:
            main_model_config = self.main_model_config
        else:
            main_model_config = self.get_model_config(models_fields.keys()[0])

        # If the main join model is in the required models, use it, else…
        main_join_model_config = None
        if self.main_join_model_config.id in models_fields:
            main_join_model_config = self.main_join_model_config
        # …use the main model if it also has a ``Date`` field, else…
        elif main_model_config.date_field_id is not None:
            main_join_model_config = main_model_config
        # …use the first model having a ``Date`` field.
        else:
            for model_id in models_fields.keys():
                model_config = self.get_model_config(model_id)
                if model_config.date_field_id is not None:
                    main_join_model_config = model_config
                    break

        # The whole FROM clause (including the FROM and optional JOINs).
        from_clause = "FROM {}".format(main_model_config.db_data_table)

        # Add a JOIN to the main join table, if available.
        if main_join_model_config not in (None, main_model_config):
            from_clause += " LEFT JOIN {} ON {}".format(
                main_join_model_config.db_data_table,
                main_join_model_config.msf_id_field_config.full_db_col_name,
            )

        # DB cols names for the ORDER BY clause.
        order_by_cols = main_model_config.get_order_by_cols_names()

        # Check if the special field ``Date`` is in the ORDER BY.
        # If not and there is a main join model, use that one. If no required model has that field, it's normal to
        # not have it in the ORDER BY.
        # /!\ Risky check! Using the number of cols works as we have only 2 special fields and the first one is
        # always the ``MSF ID``.
        is_missing_date_order_col = len(order_by_cols) < 2
        if is_missing_date_order_col and main_join_model_config is not None:
            order_by_cols.append(main_join_model_config.date_field_config.full_db_col_name)

        # Loop over models from the given config.
        for model_id, field_ids in models_fields.iteritems():
            model_config = self.get_model_config(model_id)

            # Add the JOIN clause for this model, if it's not the main model nor the main join model.
            if model_id not in (main_model_config.id, getattr(main_join_model_config, "id", None)):
                from_clause += " " + model_config.get_sql_join_clause(main_model_config, main_join_model_config)

            # Loop over fields.
            for field_id in field_ids:
                field_config = model_config.get_field_config(field_id)

                # Add the column to the SELECT columns.
                select_cols.append("{} AS `{}`".format(field_config.full_db_col_name, field_config.data_slug))

        # Build the SQL statement.
        sql = clean_sql("""
            SELECT {cols}
            {from_clause}
            ORDER BY {order_by}
        """.format(
            cols=", ".join(select_cols),
            from_clause=from_clause,
            order_by=", ".join(order_by_cols),
        ))
        return sql

    def get_data_slug(self, model_id, field_id):
        """Return the data slug for given model and field IDs."""
        field_config = self.get_field_config(model_id, field_id)
        return field_config.data_slug

    def get_db_col_name(self, field_id):
        """Return the name of the DB column for the given field ID."""
        return DYNAMIC_FIELD_DB_COL_NAME_FORMAT.format(field_id)

    def get_db_config_table_name(self, model_id):
        """Return the name of the DB config table for the given model ID."""
        return DYNAMIC_MODEL_DB_CONFIG_TABLE_NAME_FORMAT.format(model_id)

    def get_db_data_table_name(self, model_id):
        """Return the name of the DB data table for the given model ID."""
        return DYNAMIC_MODEL_DB_DATA_TABLE_NAME_FORMAT.format(model_id)

    def get_field_config(self, model_id, field_id):
        """Get a given dynamic field config."""
        model_config = self.get_model_config(model_id)
        return model_config.get_field_config(field_id)

    def get_model(self, model_id, **kwargs):
        """Get a dynamic model populated with its data."""
        model_config = DynamicRegistry.get_model_config(model_id)
        return model_config.objects.get(**kwargs)

    def get_model_config(self, model_id):
        """Return the model config for the given model ID, loading it if not already available."""
        if model_id not in self.models_config:
            self.load_models_config(model_id)
        return self.models_config[model_id]

    def get_msf_id_db_col_name(self, model_id):
        """Return the DB col name of the special field ``MSF ID`` for the given model ID."""
        model_config = self.get_model_config(model_id)
        return model_config.msf_id_db_col_name

    def get_date_db_col_name(self, model_id):
        """Return the DB col name of the special field ``Date`` for the given model ID."""
        model_config = self.get_model_config(model_id)
        return model_config.date_db_col_name

    def init(self):
        """Initialize the registry."""
        self.load_models_config()

    def load_models_config(self, ids=None):
        """Initialize all available dynamic models config, or given ones."""
        # Don't reload all models config if it has already been done.
        if ids is None and self._all_models_config_loaded:
            return

        # Build the SQL statement.
        sql = clean_sql("""
            SELECT tabla_id AS id,
                presentador AS name,
                registros AS position,
                main_table AS is_main_table,
                main_join_table AS is_main_join_table,
                msf_id_field_id,
                date_field_id
            FROM tablas
            {where_clause}
            ORDER BY registros
        """.format(where_clause=self._build_models_config_where_clause(ids)))

        # Execute the query.
        with DataDb.execute(sql) as c:
            # Raise an exception if no record found.
            if c.rowcount == 0:
                if ids is None:
                    raise RuntimeError("No dynamic models found in database.")
                else:
                    raise AttributeError("No dynamic model found matching IDs '{}'.".format(ids))

            # Loop over records.
            for row in c.fetchall():
                # Convert DB values into their Python values.
                cleaned_data = self._from_db_values_model_config(row)

                # Create an instance of ``DynamicModelConfig`` and store it in the models config registry.
                model_id = cleaned_data.pop("id")
                model_config = DynamicModelConfig(model_id, cleaned_data)
                self.models_config[model_id] = model_config

                # Check for main tables.
                if cleaned_data["is_main_table"]:
                    self.main_model_config = model_config
                if cleaned_data["is_main_join_table"]:
                    self.main_join_model_config = model_config

        # Register all models config as loaded.
        if ids is None:
            self._all_models_config_loaded = True

    def split_data_slug(self, data_slug):
        """Split the data slug into ``(model_id, field_id)``."""
        return [int(v) for v in data_slug.split(DATA_SLUG_SEPARATOR)]

    def _build_models_config_where_clause(self, ids):
        """Build the WHERE clause to retrieve dynamic models config as requested."""
        if ids is None:
            return ""

        where = "WHERE tabla_id"
        if isinstance(ids, Iterable):
            where += " IN ({})".format(", ".join(ids))
        else:
            where += " = {}".format(ids)

        return where

    def _from_db_values_model_config(self, row):
        """Convert DB values of a model config into their Python values."""
        cleaned_data = copy(row)
        cleaned_data["id"] = Cast.int(row["id"])
        cleaned_data["position"] = Cast.int(row["position"])
        cleaned_data["is_main_table"] = Cast.bool(row["is_main_table"])
        cleaned_data["is_main_join_table"] = Cast.bool(row["is_main_join_table"])
        cleaned_data["msf_id_field_id"] = Cast.int(row["msf_id_field_id"])
        cleaned_data["date_field_id"] = Cast.int(row["date_field_id"])
        return cleaned_data


# Singleton: Override class with its instance.
DynamicRegistry = DynamicRegistry()
