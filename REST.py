import re

from django.http import Http404
from rest_framework.exceptions import APIException

import DAO
from EasyDBObjects import FieldConfig

from rest_framework.response import Response
from rest_framework import serializers, viewsets


class Table(object):
    def __init__(self, table_config, **kwargs):
        # For every field in the table, we inject a property in this instance
        for field in (map(lambda c: c.field_id, table_config.fields)):
            setattr(self, field, kwargs.get(field, None))


class TableSerializer(serializers.Serializer):

    def __init__(self, table_config, showall=True, **kwargs):
        super(TableSerializer, self).__init__(**kwargs)
        self.table_config = table_config
        self.daoobject = DAO.DAO()
        self.daoobject.set_tables_config()
        self.daoobject.set_tables_relationships()

        if showall:
            fields = table_config.fields
        else:
            fields = table_config.printable_fields()

        # Map the different column types to the correct serializer.
        for column in fields:
            if column.type == FieldConfig.field_type_int:
                self.fields[self.sanitize(column.name)] = serializers.IntegerField(source=column.field, default=None)
            elif column.type in (FieldConfig.field_type_str, FieldConfig.field_type_not, FieldConfig.field_type_sel):
                self.fields[self.sanitize(column.name)] = serializers.CharField(source=column.field, default=None)
            elif column.type == FieldConfig.field_type_date:
                self.fields[self.sanitize(column.name)] = serializers.DateTimeField(source=column.field, default=None)

    @staticmethod
    def sanitize(dirty):
        return re.sub('[^0-9a-zA-Z_]', '_', dirty)

    def create(self, validated_data):
        table = Table(id=None, table_config=self.table_config, **validated_data)
        to_add = []
        for field_def in self.table_config.fields:
            if field_def.field_id in validated_data:# and validated_data[field_def.field_id] is not None:
                to_add.append([field_def.field_id, validated_data[field_def.field_id], field_def.type])
        self.daoobject.insertrecord(self.table_config.id, to_add)
        return table

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance



#
# /api/
#
# /api?tableid=x  =>  list content of tabla_x
#
#
#mixins.CreateModelMixin,
class TableViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = TableSerializer

    def __init__(self, **kwargs):
        super(TableViewSet, self).__init__(**kwargs)
        self.daoobject = DAO.DAO()
        self.daoobject.set_tables_config()
        self.daoobject.set_tables_relationships()

    def list(self, request):
        #print request.user.is_authenticated
        if "tableid" not in request.query_params:
            raise APIException(detail='tableid required')

        tableid = request.query_params["tableid"]

        for tablec in self.daoobject.tables_config:
            if tablec.id == tableid:
                where_params = self.extract_where_params(tablec, request.query_params)
                where_string = ' and '.join(['%s = %s' % (key, value) for (key, value) in where_params.items()])

                print where_string

                c = self.daoobject.db.cursor()
                query = "select {} from {}"
                params = (TableViewSet.select_string(tablec), tablec.sql_table_config_name)
                c.execute(query.format(*params))
                rows = c.fetchall()
                fields = map(lambda x: x[0], c.description)
                results = [dict(zip(fields, row)) for row in rows]
                records = map(lambda r: Table(tablec, **r), results)
                c.close()

                serializer = TableSerializer(table_config=tablec, instance=records, many=True, showall=self.only_viewable(request))
                return Response(serializer.data)

        raise Http404

    def retrieve(self, request, pk=None):
        #print request.user.is_authenticated

        if pk is None:
            raise APIException(detail='pk required!')
        elif "tableid" not in request.query_params:
            raise APIException(detail='tableid required')

        tableid = request.query_params["tableid"]

        for tablec in self.daoobject.tables_config:
            if tablec.id == tableid:
                c = self.daoobject.db.cursor()
                query = "select {} from {} where _id = {}"
                params = (TableViewSet.select_string(tablec), tablec.sql_table_config_name, pk)
                c.execute(query.format(*params))
                row = c.fetchone()
                fields = map(lambda x: x[0], c.description)
                result = dict(zip(fields, row))
                c.close()

                serializer = TableSerializer(table_config=tablec, instance=Table(tablec, **result), many=False, showall=self.only_viewable(request))
                return Response(serializer.data)
        return Http404

    @staticmethod
    def select_string(table_config):
        return ', '.join(map(lambda f: f.field, table_config.printable_fields()))

    @staticmethod
    def only_viewable(request):
        if "showall" in request.query_params and request.query_params["showall"] == "true":
            return True
        else:
            return False

    @staticmethod
    def extract_where_params(table_config, query_params):
        where_params = dict()
        field_names = map(lambda f: TableSerializer.sanitize(f.name), table_config.fields)

        for (key, value) in query_params.items():
            if key in field_names:
                where_params[key] = value

        return where_params
