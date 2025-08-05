from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q

class EmailOrPhoneBackend(ModelBackend):
    """
    Authenticate with username OR email OR phone (from Profile).
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('email') or kwargs.get('phone')
        try:
            user = User.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username) |
                Q(profile__phone__iexact=username)
            )
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
