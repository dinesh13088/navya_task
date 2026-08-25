from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    AbstractUser gives username/password/email/auth-related fields .
    """
    pass
