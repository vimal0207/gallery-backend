from drf_yasg import openapi
from utilities import keys

HEADER_TOKEN = openapi.Parameter(keys.AUTH, openapi.IN_HEADER,
                                 description="Token ex-eyJ0eXAiOiJKV1QiLCJhbGci......",
                                 type=openapi.TYPE_STRING,
                                 required=True)

QUERY_PARAM_ID = openapi.Parameter('id', openapi.IN_QUERY,
                                   description="1",
                                   type=openapi.TYPE_INTEGER,
                                   required=False)

QUERY_PAGE = openapi.Parameter('page', openapi.IN_QUERY,
                                   description="1",
                                   type=openapi.TYPE_INTEGER,
                                   required=False)

QUERY_PARAM_STATUS = openapi.Parameter('status', openapi.IN_QUERY,
                                       description="True",
                                       type=openapi.TYPE_BOOLEAN,
                                       required=False)