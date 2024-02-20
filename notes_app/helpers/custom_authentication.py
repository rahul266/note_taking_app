from ..models import User
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            
            if check_password(password,user.password):
                return user
        except ObjectDoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
