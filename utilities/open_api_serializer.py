from rest_framework import serializers


class LoginPOSTSerializer(serializers.Serializer):
    phone = serializers.IntegerField(required=True)
    # password = serializers.CharField(required=True)


class OtpSerializer(serializers.Serializer):
    phone = serializers.IntegerField(required=True)
    otp = serializers.IntegerField(required=True)


class ChangePasswordPOSTSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)