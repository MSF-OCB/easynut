from __future__ import print_function
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from django.http import Http404
from rest_framework.exceptions import APIException

import DAO

from rest_framework.response import Response

from REST import Table, TableSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # Do not perform CSRF check for the REST API


class TableList(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def __init__(self, **kwargs):
        super(TableList, self).__init__(**kwargs)
        self.daoobject = DAO.DAO()
        self.daoobject.set_tables_config()
        self.daoobject.set_tables_relationships()

    def get(self, request):
        # print request.user.is_authenticated
        if "tableid" not in request.query_params:
            raise APIException(detail='tableid required')

        tableid = request.query_params["tableid"]

        for tablec in self.daoobject.tables_config:
            if tablec.id == tableid:
                where_params = self.extract_where_params(tablec, request.query_params)
                where_string = ' and '.join(['%s = \'%s\'' % (key, value) for (key, value) in where_params.items()])

                print(where_string)

                c = self.daoobject.db.cursor()
                query = "select {} from {}"
                params = (self.select_string(tablec), tablec.sql_table_config_name)
                c.execute(query.format(*params))
                rows = c.fetchall()
                fields = map(lambda x: x[0], c.description)
                results = [dict(zip(fields, row)) for row in rows]
                records = map(lambda r: Table(tablec, **r), results)
                c.close()

                serializer = TableSerializer(table_config=tablec,
                                             instance=records,
                                             many=True,
                                             showall=self.only_viewable(request))
                return Response(serializer.data)

        raise Http404

    def post(self, request):
        if "tableid" not in request.query_params:
            raise APIException(detail='tableid required')

        tableid = request.query_params["tableid"]

        for tablec in self.daoobject.tables_config:
            if tablec.id == tableid:
                serializer = TableSerializer(table_config=tablec,
                                             data=request.data,
                                             showall=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise Http404

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
