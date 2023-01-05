from rest_framework import serializers
from rest_framework.authtoken.models import Token
from accounts.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from utilities import keys

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        token, flag = Token.objects.get_or_create(user=self.user)
        data = {keys.TOKEN : token.key}
        return data

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    phone = serializers.IntegerField()
    isd = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(max_length=50)
    fcm_token = serializers.CharField(required=False, allow_null=True, 
                                allow_blank=True,write_only=True)
    active = serializers.BooleanField(required=False)
    password = serializers.CharField(max_length=500, write_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.get('context', {}).get("fields", None)
        exclude = kwargs.get('context', {}).get("exclude", None)
        super(UserSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name)


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        context = self.context
        passw = None
        if keys.PASSWORD in validated_data:
            passw = validated_data.pop(keys.PASSWORD)
            instance.set_password(passw)
            instance.save()
        instance, _ = User.objects.update_or_create(id = instance.id,
                         defaults={**validated_data, **context})
        return instance
