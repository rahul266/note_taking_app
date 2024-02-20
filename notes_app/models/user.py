from django.db import models
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        print(password)
        user.set_password(password)
        return user


class User(AbstractUser,PermissionsMixin):
    username=None
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    # def save(self, *args, **kwargs):
    #     print(self.password)
    #     print(check_password(self.password,make_password(self.password)))
    #     self.password = make_password(self.password)
    #     super().save(*args, **kwargs)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
