from django.forms import ModelForm
from .models import ContactForm
from django import forms


class ContactView(ModelForm):

    """Docstring for ContactView. """
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        fields = ['name', 'email', 'topic', 'message']
        model = ContactForm
