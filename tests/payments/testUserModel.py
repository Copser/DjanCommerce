from django.test import TestCase
from payments.models import User
from django.db import IntegrityError


class UserModelTest(TestCase):

    """Docstring for UserModelTest. Making user for database model
    testing. Conductin a series of test's to see if are User will
    properly be loaded into database, returning are user
    email to us to see if email was loaded, checking to see if we can
    fatch User by id. then we are checking to see will
    error return on duplicate users."""
    @classmethod
    def setUpTestData(cls):
        """TODO: Docstring for setUpTestData.
        :returns: Setup User to load to are database.
        Using django setUpTestData
        """
        cls.test_user = User(email="j@j.com", name="test user")
        cls.test_user.save()

    def test_user_to_string_prin_email(self):
        """TODO: Docstring for test_user_to_string_prin_email.
        :returns: TODO

        """
        self.assertEqual(str(self.test_user), "j@j.com")

    def test_get_by_id(self):
        """TODO: Docstring for test_get_by_id.
        :returns: TODO

        """
        self.assertEqual(User.get_by_id(1), self.test_user)

    def test_create_user_function_stores_in_database(self):
        """TODO: Docstring for test_create_user_function_stores_in_database.
        :returns: TODO

        """
        user = User.create('test', 'test@t.com', 'tt', '1234', '22')
        self.assertEqual(User.objects.get(email='test@t.com'), user)

    def test_create_user_allready_exists_throws_IntegrityError(self):
        """TODO: Docstring for test_create_user_allready_exists_throws_IntegrityError.
        :returns: TODO

        """
        self.assertRaises(
            IntegrityError,
            User.create,
            'test user',
            'j@j.com',
            'jj',
            '1234',
            89
        )
