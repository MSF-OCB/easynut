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
        for field in (['_id'] + map(lambda c: c.field_id, table_config.fields)):
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
        self.fields['_id'] = serializers.IntegerField(default=None)
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
            if field_def.field_id in validated_data:
                to_add.append([field_def.field_id, validated_data[field_def.field_id], field_def.type])
        id = self.daoobject.insertrecord(self.table_config.id, to_add)
        table._id = id
        return table

    def update(self, instance, validated_data):
        print(validated_data)
        to_edit = []
        for field_def in self.table_config.fields:
            if field_def.field_id in validated_data and validated_data[field_def.field_id] is not None and validated_data[field_def.field_id] != '':
                to_edit.append([field_def.field_id, validated_data[field_def.field_id], field_def.type])
        self.daoobject.editrecord(self.table_config.id, instance._id, to_edit)
        return Table(self.table_config, **self.daoobject.select_from_record_id(self.table_config.id, instance._id))
