from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class NonDefaultModelBackend(ModelBackend):
    """
    Authenticates against django.contrib.auth.models.User.
    Using SOMEOTHER db rather than the default
    """
    supports_inactive_user = True

    def authenticate(self, username=None, password=None, db='default'):
        try:
            user = User.objects.using(db).get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id, db='default'):
        try:
            return User.objects.using(db).get(pk=user_id)
        except User.DoesNotExist:
            return None