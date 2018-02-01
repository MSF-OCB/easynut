# Not used so far
# Was planned for future android app
import re

from rest_framework import serializers

from .DAO import DAO
from .EasyDBObjects import FieldConfig


class Record(object):
    def __init__(self, table_config, **kwargs):
        # For every field in the table, we inject a property in this instance
        for field in (['_id'] + map(lambda c: c.field, table_config.fields)):
            setattr(self, field, kwargs.get(field, None))


class RecordSerializer(serializers.Serializer):

    def __init__(self, table_config, showall=True, **kwargs):
        super(RecordSerializer, self).__init__(**kwargs)
        self.table_config = table_config
        self.daoobject = DAO.DAO()
        self.daoobject.set_tables_config()
        self.daoobject.set_tables_relationships()

        if showall:
            fields = table_config.fields
        else:
            fields = filter(lambda f: f.list, table_config.fields)

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
        record = Record(id=None, table_config=self.table_config, **validated_data)
        to_add = []
        for field_def in self.table_config.fields:
            if field_def.field in validated_data:
                to_add.append([field_def.field, validated_data[field_def.field], field_def.type])
        record_id = self.daoobject.insertrecord(self.table_config.id, to_add)
        record._id = record_id
        return record

    def update(self, instance, validated_data):
        print(validated_data)
        to_edit = []
        for field_def in self.table_config.fields:
            if (field_def.field in validated_data and
                    validated_data[field_def.field] is not None and
                    validated_data[field_def.field] != ''):
                to_edit.append([field_def.field, validated_data[field_def.field], field_def.type])
        self.daoobject.editrecord(self.table_config.id, instance._id, to_edit)
        return Record(self.table_config, **self.daoobject.select_from_record_id(self.table_config.id, instance._id))
