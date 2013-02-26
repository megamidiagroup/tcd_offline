import django
from django.contrib.auth.models import User, Permission
from django.core.validators import MaxLengthValidator
from django.utils.translation import ugettext as _
from django.db.models.signals import class_prepared

NEW_USERNAME_LENGTH = 255

def longer_username_signal(sender, *args, **kwargs):
    if (sender.__name__ == "User" and sender.__module__ == "django.contrib.auth.models"):
        patch_user_model(sender)
        
#class_prepared.connect(longer_username_signal)

def monkey_patch_username():
    username = User._meta.get_field("username")
    username.max_length = NEW_USERNAME_LENGTH
    username.help_text = _("Required, %s characters or fewer. Only letters, "
                                "numbers, and @, ., +, -, or _ "
                                    "characters." % NEW_USERNAME_LENGTH)
    for v in username.validators:
        if isinstance(v, MaxLengthValidator):
            v.limit_value = NEW_USERNAME_LENGTH
            
def monkey_patch_name_permission():
    name = Permission._meta.get_field("name")
    name.max_length = NEW_USERNAME_LENGTH

    for v in name.validators:
        if isinstance(v, MaxLengthValidator):
            v.limit_value = NEW_USERNAME_LENGTH

monkey_patch_name_permission()
monkey_patch_username()