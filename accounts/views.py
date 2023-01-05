from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from accounts.models import User
from utilities import keys, open_api_param, response_key
from accounts.serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserViewSet(ModelViewSet):
    model = User
    queryset = User.objects.filter(active=True)
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in [keys.CREATE, keys.FORGOT_PASS]:
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

    def check_email_ans_pass(self, phone, user_id=None):
        exc = {}
        if user_id:
            exc[keys.ID] = user_id
        return User.objects.filter(phone=phone).exclude(**exc).exists()

    def get_object(self):
        query = {'active': True}
        obj = get_object_or_404(self.queryset.filter(id=self.kwargs.get('pk')), **query)
        self.check_object_permissions(self.request, obj)
        return obj

    @swagger_auto_schema(manual_parameters=[open_api_param.HEADER_TOKEN])
    def list(self, request, *args, **kwargs):
        user = request.user
        data = {
            keys.DATA: self.serializer_class(user).data
        }
        return response_key.SUCCESS_RESPONSE(response=data)

    def create(self, request, *args, **kwargs):
        req_data = request.data
        if self.check_email_ans_pass(req_data[keys.PHONE]):
            return response_key.PHONE_ALREADY_USED
        serializer = self.serializer_class(data=req_data)
        if serializer.is_valid():
            user = serializer.save()
        else:
            return response_key.ERROR_RESPONSE(msg=serializer.errors)
        return response_key.SUCCESS_CREATE_RESPONSE(response = {keys.DATA : serializer.data})

    @action(methods=["PATCH", ], detail=False)
    def forgot_password(self, request):
        req_data = request.data.copy()
        if not self.check_email_ans_pass(req_data[keys.PHONE]):
            return response_key.INVALID_PHONE
        user = self.queryset.get(phone=req_data[keys.PHONE])
        serializer = self.serializer_class(user, req_data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
        else:
            return response_key.ERROR_RESPONSE(msg=serializer.errors)
        return response_key.SUCCESS_RESPONSE(response={keys.DATA:serializer.data})
        
    @swagger_auto_schema(manual_parameters=[open_api_param.HEADER_TOKEN])
    def partial_update(self, request, *args, **kwargs):
        req_data = request.data
        instance = self.get_object()
        if self.check_email_ans_pass(req_data[keys.PHONE], user_id=instance.id):
            return response_key.PHONE_ALREADY_USED
        serializer = self.serializer_class(instance, data=req_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return response_key.SUCCESS_RESPONSE(response={keys.DATA:serializer.data})