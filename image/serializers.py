from rest_framework import serializers
from .models import UserMedia
from gallery import settings

class UserMediaSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = UserMedia
        fields = '__all__'

    def get_img_url(self, instance):
        return settings.SERVER_URL + instance.img.url