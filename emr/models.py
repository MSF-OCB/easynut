# -*- coding: utf-8 -*-
from collections import OrderedDict

from .utils import DATA_DB, Cast, clean_sql


class DynamicField(object):
    """Dynamic field of a dynamic model (configured in a ``tabla_X_des`` row)."""

    def __init__(self, attrs):
        for k, v in attrs.iteritems():
            setattr(self, k, v)


class DynamicModel(object):
    """Dynamic model (configured in the ``tabla_X_des`` table)."""

    def __init__(self, attrs):
        for k, v in attrs.iteritems():
            setattr(self, k, v)

        # DB tables containing the data and the fields config.
        self._data_table = "tabla_{}".format(self.id)
        self._config_table = "tabla_{}_des".format(self.id)

        self._fields = OrderedDict()
        self._init_fields()

    def _init_fields(self):
        """Initialize model fields."""
        sql = clean_sql("""
            SELECT campo_id AS fieldname, presentador AS name, tipo AS kind, varios AS values_list,
                listado AS has_list, detalle AS has_detail, buscar AS has_find, usar AS has_use,
                nuevaLinea AS has_new_line, editable AS is_editable, pos AS position
            FROM {table}
            ORDER BY pos
        """.format(table=self._config_table))

        c = DATA_DB.cursor()
        c.execute(sql)
        for row in c.fetchall():
            self._cast_field_config_row(row)
            key = row["id"]
            self._fields[key] = DynamicField(row)
        c.close()

    def _cast_field_config_row(self, row):
        row["id"] = Cast.int(row["fieldname"].replace("campo_", ""))
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
    """Registry of available dynamic models (registered in the ``tablas`` table)."""

    def __init__(self):
        self._models = OrderedDict()
        self._init_models()

    def _init_models(self):
        """Initialize all available dynamic models."""
        sql = clean_sql("""
            SELECT CAST(tabla_id AS UNSIGNED) AS id, presentador AS name
            FROM tablas
            ORDER BY id
        """)

        c = DATA_DB.cursor()
        c.execute(sql)
        for row in c.fetchall():
            self._cast_model_config_row(row)
            key = row["id"]
            self._models[key] = DynamicModel(row)
        c.close()

    def _cast_model_config_row(self, row):
        row["id"] = Cast.int(row["id"])
