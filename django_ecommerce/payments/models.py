from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):

    """Docstring for User. """
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    # password field define in base class
    last_4_digits = models.CharField(max_length=4, blank=True,
                                     null=True)
    stripe_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        """TODO: Docstring for __str__.
        :returns: TODO

        """
        return self.email
