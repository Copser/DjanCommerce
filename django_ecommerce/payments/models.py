from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone


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

    @classmethod
    def get_by_id(cls, uid):
        """TODO: Docstring for get_by_id.
        :returns: TODO

        """
        return User.objects.get(pk=uid)

    @classmethod
    def create(cls, name, email, password, last_4_digits, stripe_id):
        """TODO: Docstring for create.
        :returns: TODO

        """
        new_user = cls(name=name, email=email,
                       last_4_digits=last_4_digits, stripe_id=stripe_id)
        new_user.set_password(password)

        new_user.save()
        return new_user

    def __str__(self):
        """TODO: Docstring for __str__.
        :returns: TODO

        """
        return self.email


class UnpaidUsers(models.Model):

    """Docstring for UnpaidUsers. """
    email = models.CharField(max_length=225, unique=True)
    last_notification = models.DateTimeField(default=timezone.now())
