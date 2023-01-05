from django.db import models
from base.models import DateTimeRecord
from accounts.models import User

class UserMedia(DateTimeRecord):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_media')
    img = models.ImageField(upload_to='gallery')
    title = models.CharField(max_length=255)
    description = models.TextField()