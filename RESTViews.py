from __future__ import print_function
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework.exceptions import APIException

import DAO

from rest_framework.response import Response

from REST import Table, TableSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # Do not perform CSRF check for the REST API


class Utils:
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


class TableList(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def __init__(self, **kwargs):
        super(TableList, self).__init__(**kwargs)
        self.daoobject = DAO.DAO()
        self.daoobject.set_tables_config()
        self.daoobject.set_tables_relationships()

    def get(self, request, table_id):
        for tablec in self.daoobject.tables_config:
            if tablec.id == table_id:
                where_params = Utils.extract_where_params(tablec, request.query_params)
                where_string = ' and '.join(['%s = \'%s\'' % (key, value) for (key, value) in where_params.items()])

                print(where_string)

                c = self.daoobject.db.cursor()
                query = "select {} from {}"
                params = (self.daoobject.select_string(tablec, showall=Utils.only_viewable(request)), tablec.sql_table_config_name)
                print(query.format(*params))
                c.execute(query.format(*params))
                rows = c.fetchall()
                fields = map(lambda x: x[0], c.description)
                results = [dict(zip(fields, row)) for row in rows]
                records = map(lambda r: Table(tablec, **r), results)
                c.close()

                serializer = TableSerializer(table_config=tablec,
                                             instance=records,
                                             many=True,
                                             showall=Utils.only_viewable(request))
                return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, table_id):
        for tablec in self.daoobject.tables_config:
            if tablec.id == table_id:
                serializer = TableSerializer(table_config=tablec,
                                             data=request.data,
                                             showall=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)


class TableDetail(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def __init__(self, **kwargs):
        super(TableDetail, self).__init__(**kwargs)
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
                    serializer = TableSerializer(table_config=tablec, instance=Table(tablec, **result), many=False, showall=Utils.only_viewable(request))
                    return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, table_id, pk):
        for tablec in self.daoobject.tables_config:
            if tablec.id == table_id:
                table = self.daoobject.select_from_record_id(table_id, pk)
                print(table)
                if table:
                    serializer = TableSerializer(table_config=tablec,
                                                 instance=Table(tablec, **table),
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
