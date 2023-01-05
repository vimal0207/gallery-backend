from django.contrib import admin

from .models import UserMedia

@admin.register(UserMedia)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'img']
