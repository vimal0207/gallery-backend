from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from utilities import keys, open_api_param, response_key, utils

from .models import UserMedia
from .serializers import UserMediaSerializer
from . import caching

class UserMediaViewSet(ModelViewSet):
    model = UserMedia
    queryset = UserMedia.objects.filter(is_deleted=False)
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserMediaSerializer

    def update_caching(self, id):
        data = self.queryset.filter(user_id=id).order_by(f'-{keys.CREATED_AT}')
        caching.setKey(id, data)

    @swagger_auto_schema(manual_parameters=[open_api_param.HEADER_TOKEN, open_api_param.QUERY_PAGE])
    def list(self, request, *args, **kwargs):
        user = request.user
        user_id = user.id
        self.update_caching(request.user.id)
        data = caching.getKey(user_id)
        if not data:
            data = self.queryset.filter(user=user).order_by(f'-{keys.CREATED_AT}')
            caching.setKey(user_id, data)
        total_entities = request.GET.get(keys.TOTAL_ENTITIES, 10)
        page = request.GET.get(keys.PAGE, 1)
        data, page_detail = utils.apply_pagination(data, page=page, total_entities=total_entities)
        ser = self.serializer_class(data, many=True)
        return response_key.SUCCESS_RESPONSE(response={keys.DATA : ser.data, **page_detail})

    @swagger_auto_schema(manual_parameters=[open_api_param.HEADER_TOKEN])
    def create(self, request, *args, **kwargs):
        req_data = request.data.copy()
        req_data[keys.USER] = request.user.id
        serializer = self.serializer_class(data=req_data)
        if serializer.is_valid():
            user = serializer.save()
            self.update_caching(request.user.id)
        else:
            return response_key.ERROR_RESPONSE(msg=serializer.errors)
        return response_key.SUCCESS_CREATE_RESPONSE(response={keys.DATA : serializer.data})

    @swagger_auto_schema(manual_parameters=[open_api_param.HEADER_TOKEN])
    def partial_update(self, request, *args, **kwargs):
        req_data = request.data
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=req_data)
        serializer.is_valid(raise_exception=True)
        img = serializer.save()
        self.update_caching(request.user.id)
        return response_key.SUCCESS_RESPONSE({keys.DATA : serializer.data})

    @swagger_auto_schema(manual_parameters=[open_api_param.HEADER_TOKEN])
    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        self.update_caching(request.user.id)
        return response_key.SUCCESS_RESPONSE()