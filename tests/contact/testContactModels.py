from django.test import TestCase, SimpleTestCase
from contact.views import ContactView
from contact.models import ContactForm
from datetime import datetime, timedelta


class UserModelTest(TestCase):

    """Docstring for UserModelTest. """
    @classmethod
    def setUpTestData(cls):
        """TODO: Docstring for setUpTestData.
        :returns: TODO

        """
        ContactForm(email='test@dummy.com', name='test').save()
        ContactForm(email='j@j.com', nema='jj').save()
        cls.firstUser = ContactForm(
            email='first@first.com',
            name='first',
            timestamp=datetime.today() + timedelta(days=2)
        )
        cls.firstUser()

    def test_contactform_str_returns_email(self):
        """TODO: Docstring for test_contactform_str_returns_email.
        :returns: TODO

        """
        self.assertEqual('first@first.com', str(self.firstUser))

    def test_ordering(self):
        """TODO: Docstring for test_ordering.
        :returns: TODO

        """
        contacts = ContactForm.objects.all()
        self.assertEqual(self.firstUser, contacts[0])


class ContactViewTests(SimpleTestCase):

    """Docstring for ContactViewTests. """
    def test_displayed_fields(self):
        """TODO: Docstring for test_displayed_fields.
        :returns: TODO

        """
        expected_fields = ['name', 'email', 'topic', 'message']
        self.assertEqual(ContactView.Meta.fields, expected_fields)
