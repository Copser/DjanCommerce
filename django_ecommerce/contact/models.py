from django.db import models
import datetime

# Create your models here.


class ContactForm(models.Model):

    """Docstring for ContactForm. """
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    topic = models.CharField(max_length=200)
    message = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(
        auto_now_add=True, default=datetime.datetime.now
    )

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.email

    class Meta:
        ordering = ['-timestamp']
