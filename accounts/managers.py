from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, phone, password, **extra_fields):
        try:
            if not phone:
                raise ValueError('Phone must be required')
            user = self.model(
                phone=phone, **extra_fields
            )
            user.set_password(password)
            user.save(using=self._db)
        except Exception as e:
            return e
        return user

    def create_user(self, phone, password, **extra_fields):
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True
        user = self.model(
                phone=phone, **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)
        return user