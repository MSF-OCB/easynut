from __future__ import print_function
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework.exceptions import APIException

import DAO

from rest_framework.response import Response

from REST import Record, RecordSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # Do not perform CSRF check for the REST API


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def only_viewable(request):
        if "showall" in request.query_params and request.query_params["showall"] == "true":
            return True
        else:
            return False


class RecordList(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def __init__(self, **kwargs):
        super(RecordList, self).__init__(**kwargs)
        self.daoobject = DAO.DAO()
        self.daoobject.set_tables_config()
        self.daoobject.set_tables_relationships()

    def get(self, request, table_id):
        for tablec in self.daoobject.tables_config:
            if tablec.id == table_id:
                where_params = dict()
                for field in tablec.fields:
                    sanitized = RecordSerializer.sanitize(field.name)
                    if sanitized in request.query_params:
                        where_clause = dict()
                        where_clause['fieldc'] = field
                        where_clause['value'] = request.query_params[sanitized]
                        where_params[field.field_id] = where_clause

                if where_params:
                    rows = self.daoobject.search_by_fields(tablec, where_params, Utils.only_viewable(request))
                    records = map(lambda r: Record(tablec, **r), rows)
                    serializer = RecordSerializer(table_config=tablec,
                                                  instance=records,
                                                  many=True,
                                                  showall=Utils.only_viewable(request))
                    return Response(serializer.data)
                else:
                    serializer = RecordSerializer(table_config=tablec,
                                                  instance=[],
                                                  many=True,
                                                  showall=Utils.only_viewable(request))
                    return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, table_id):
        for tablec in self.daoobject.tables_config:
            if tablec.id == table_id:
                serializer = RecordSerializer(table_config=tablec,
                                              data=request.data,
                                              showall=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)


class RecordDetail(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def __init__(self, **kwargs):
        super(RecordDetail, self).__init__(**kwargs)
        self.daoobject = DAO.DAO()
        self.daoobject.set_tables_config()
        self.daoobject.set_tables_relationships()

    def get(self, request, table_id, pk):
        if pk is None:
            raise APIException(detail='pk required!')

        for tablec in self.daoobject.tables_config:
            if tablec.id == table_id:
                result = self.daoobject.select_from_record_id(table_id, pk, showall=Utils.only_viewable(request))
                if result is not None:
                    serializer = RecordSerializer(table_config=tablec, instance=Record(tablec, **result), many=False, showall=Utils.only_viewable(request))
                    return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, table_id, pk):
        for tablec in self.daoobject.tables_config:
            if tablec.id == table_id:
                record = self.daoobject.select_from_record_id(table_id, pk)
                if record:
                    serializer = RecordSerializer(table_config=tablec,
                                                  instance=Record(tablec, **record),
                                                  data=request.data,
                                                  showall=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, table_id, pk):
        res = self.daoobject.delete(table_id, pk)
        if res is None:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
