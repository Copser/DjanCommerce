"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import unittest
import mock
from django import forms
from django.test import TestCase, RequestFactory
from django.db import IntegrityError
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from payments.models import User
from payments.forms import SigninForm, UserForm, CardForm
import django_ecommerce.settings as settings
from .views import sign_in, sign_out
from payments.views import soon, register


class UserModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Setup
        """
        cls.test_user = User(email="j@j.com", name='test_user')
        cls.test_user.save()

    def test_create_user_function_stores_in_database(self):
        """TODO: Docstring for test_create_user_function_stores_in_database.
        :returns: TODO

        """
        user = User.create('test', 'test@t.com', 'tt', '1234', '22')
        self.assertEquals(User.objects.get(email='test@t.com'), user)

    def test_create_user_allready_exists_throws_IntegrityError(self):
        """TODO: Docstring for test_create_user_allready_exists_throws_IntegrityError.
        :returns: TODO

        """
        self.assertRaises(
            IntegrityError,
            User.create,
            'test_user',
            'j@j.com',
            'jj',
            '1234',
            89
        )

    def test_user_to_string_print_email(self):
        """TODO: Docstring for test_user_to_string_print_email.
        :returns: TODO

        """
        self.assertEquals(str(self.test_user), "j@j.com")

    def test_get_by_id(self):
        """TODO: Docstring for test_get_by_id.
        :returns: TODO

        """
        self.assertEquals(User.get_by_id(1), self.test_user)


class FormTesterMixin():

    """Docstring for FormTextMixin. """
    def assertFormError(self, from_cls, expected_error_name,
                        expected_error_msg, data):
        from pprint import pformat
        test_form = from_cls(data=data)
        # if we get an error then the form should not be valid
        self.assertFalse(test_form.is_valid())

        self.assertEquals(
            test_form.errors[expected_error_name],
            expected_error_msg,
            msg="Expected {}: Actual {}: using data {}".format(
                test_form.errors[expected_error_name],
                expected_error_msg, pformat(data)
            )
        )


class FormTests(unittest.TestCase, FormTesterMixin):

    """Docstring for FormTests. """
    def test_signin_form_validation_for_invalid_data(self):
        invalid_data_list = [
            {'data': {'email': 'j@j.com'},
             'error': ('password', [u'This field is required.'])},
            {'data': {'password': '1234'},
             'error': ('email', [u'This field is required.'])}
        ]

        for invalid_data in invalid_data_list:
            self.assertFormError(SigninForm,
                                 invalid_data['error'][0],
                                 invalid_data['error'][1],
                                 invalid_data['data'])

    def test_user_form_password_match(self):
        """TODO: Docstring for test_user_form_password_match.
        :returns: TODO

        """
        form = UserForm(
            {
                'name': 'jj',
                'email': 'j@j.com',
                'password': '1234',
                'var_password': '1234',
                'last_4_digits': '3333',
                'stripe_token': '1'}
        )
        # Is the data valid? -- if not print out the error
        if form.is_valid():
            # this will throw an error if the form doesn't clean
            # correctly
            self.assertTrue(form.cleaned_data)

    def test_user_form_passwords_dont_match_throws_error(self):
        """TODO: Docstring for test_user_form_passwords_dont_match_throws_error.
        :returns: TODO

        """
        form = UserForm(
            {
                'name': 'jj',
                'email': 'j@j.com',
                'password': '234',
                'ver_password': '1234',  # bad password
                'last_4_digits': '3333',
                'stripe_token': '1'
            }
        )
        # Is the form valid?
        self.assertFalse(form.is_valid())

#    def test_card_form_data_validation_for_invalid_data(self):
        """TODO: Docstring for test_card_form_data_validation_for_invalid_data.
        :returns: TODO

        """
#        invalid_data_list = [
#            {
#                'data': {'last_4_digits': '123'},
#                'error': (
#                    'last_4_digits',
#                    [u'Ensure this value has at least 4 characters(it has 3).']
#                )
#            },
#            {
#                'data': {'last_4_digits': '12345'},
#                'error': (
#                    'last_4_digits',
#                    [u'Ensure this value has at most 4 characters (it has 5),']
#                )
#            }
#        ]

#        for invalid_data in invalid_data_list:
#            self.assertFormError(
#                CardForm,
#                invalid_data['error'][0],
#                invalid_data['error'][1],
#                invalid_data["data"]
#            )


# Testin routes
class ViewTesterMixin(object):

    """Docstring for ViewTextMixin. """
    @classmethod
    def setupViewTester(cls, url, view_func, expected_html,
                        status_code=200, session={}):
        """TODO: Docstring for setupViewTester.
        :returns: TODO

        """
        request_factory = RequestFactory()
        cls.request = request_factory.get(url)
        cls.request.session = session
        cls.status_code = status_code
        cls.url = url
        cls.view_func = staticmethod(view_func)
        cls.expected_html = expected_html

    def test_resolves_to_correct_view(self):
        """TODO: Docstring for test_resolves_to_correct_view.
        :returns: TODO

        """
        test_view = resolve(self.url)
        self.assertEquals(test_view.func, self.view_func)

#    def test_returns_appropriate_response_code(self):
        """TODO: Docstring for test_returns_appropriate_response_code.
        :returns: TODO

        """
#        resp = self.view_func(self.request)
#        self.assertEquals(resp.status_code, self.status_code)

#    def test_returns_correct_html(self):
        """TODO: Docstring for test_returns_correct_html.
        :returns: TODO

        """
#        resp = self.view_func(self.request)
#        self.assertEquals(resp.content, self.expected_html)


class SignInPageTests(TestCase, ViewTesterMixin):

    """Docstring for SignInPageTests. """
    @classmethod
    def setUpClass(cls):
        """TODO: Docstring for setUpClass.
        :returns: TODO

        """
        html = render_to_response(
            'sign_in.html',
            {
                'form': SigninForm(),
                'user': None
            }
        )

        ViewTesterMixin.setupViewTester(
            '/sign_in',
            sign_in,
            html.content
        )


class SignOutPageTests(TestCase, ViewTesterMixin):

    """Docstring for SignOutPageTests. """
    @classmethod
    def setUpClass(cls):
        ViewTesterMixin.setupViewTester(
            '/sign_out',
            sign_out,
            "",  # a redirect will return no hmtl
            status_code=302,
            session={'user': 'dummy'},
        )

    def setUp(self):
        """TODO: Docstring for setUp.
        :returns: TODO

        """
        # sign_out clears the session, so let's reset it overtime
        self.request.session = {'user': 'dummy'}


class RegisterPageTest(TestCase, ViewTesterMixin):

    """Docstring for RegisterPageTest. """
    @classmethod
    def setUpClass(cls):
        html = render_to_response(
            'register.html',
            {   
                'form': UserForm(),
                'months': range(1, 12),
                'publishable': settings.STRIPE_PUBLISHABLE,
                'soon': soon(),
                'user': None,
                'years': range(2011, 2036),
            }
        )
        ViewTesterMixin.setupViewTester(
            '/register',
            register,
            html.content,
        )

    def setUp(self):
        """TODO: Docstring for setUp.
        :returns: TODO

        """
        request_factory = RequestFactory()
        self.request = request_factory.get(self.url)

    def test_invalid_form_returns_registration_page(self):
        """TODO: Docstring for test_invalid_form_returns_registration_page.
        :returns: TODO

        """
        with mock.patch('payments.forms.UserForm.is_valid') as user_mock:
            user_mock.return_value = False

            self.request.method = "POST"
            self.request.POST = None
            resp = register(self.request)
            self.assertEquals(resp.content, self.expected_html)
            # make shure that we did indeed call our is_valid function
            self.assertEquals(user_mock.call_count, 1)

        @mock.patch('stripe.Customer.create')
        @mock.patch.object(User, 'create')
        def test_registration_new_user_returns_succesfilly(
            self, create_mock, stripe_mock
        ):
            """TODO: Docstring for test_regostration_new_user_returns_successfilly.
            :returns: TODO

            """
            self.request.session = {}
            self.request.method = 'POST'
            self.request.POST = {
                'email': 'python@rocks.com',
                'name': 'pyRock',
                'stripe_token': '...',
                'last_4_digits': '4242',
                'password': 'bad_password',
                'ver_password': 'bad_password',
            }

            # get the return values of the mocks, for our checks later
            new_user = create_mock.return_value
            new_cust = stripe_mock.return_value

            resp = register(self.reguest)

            self.assertEquals(resp.content, "")
            self.assertEquals(resp.status_code, 302)
            self.assertEquals(self.request.session['user'], new_user.pk)
            # verify the user was actually strored in the database.
            create_mock.assert_called_with(
                'pyRock', 'python@rocks.com', 'bad_password', '4242',
                new_cust.id
            )

        def get_MockUserForm(self):
            """TODO: Docstring for get_MockUserForm.
            :returns: TODO

            """
            class MockUserForm(forms.Form):
            
                """Docstring for MockUserForm. """
                def is_valid(self):
                    """TODO: Docstring for is_valid.
                    :returns: TODO

                    """
                    return True 

                @property
                def cleaned_data(self):
                    """TODO: Docstring for cleaned_data.
                    :returns: TODO

                    """
                    return {
                        'email': 'python@rocks.com',
                        'name': 'pyRock',
                        'stripe_token': '...',
                        'last_4_digits': 'bad_password',
                        'password': 'bad_password',
                        'ver_password': 'bad_password',
                    }

                def addError(self, error):
                    """TODO: Docstring for addError.
                    :returns: TODO

                    """
                    pass
            return MockUserForm()

        @mock.patch('payments.views.UserForm', get_MockUserForm)
        @mock.patch('payments.models.User.save.', side_effect=IntegrityError)
        def test_registering_user_twice_cause_error_msg(self, save_mock):
            """TODO: Docstring for test_registering_user_twice_cause_error_msg.
            :returns: TODO

            """
            # create the request used to test the view
            self.request.session = {}
            self.request.method = 'POST'
            self.request.POST = {}

            # create the expected_html
            html = render_to_response(
                'register.html',
                {
                    'form': self.get_MockUserForm(),
                    'months': list(range(1, 12)),
                    'publishable': settings.STRIPE_PUBLISHABLE,
                    'soon': soon(),
                    'user': None,
                    'years': list(range(2011, 2036)),
                }
            )

            # mock out stripe so we don't hit their server
            with mock.patch('payments.views.Customer') as stripe_mock:
                config = {'create.return_value': mock.Mock()}
                stripe_mock.configure_mock(**config)

                # run the test
                resp = register(self.request)

                # verify that we did things correctly
                self.assertEqual(resp.content, html.content)
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(self.request.session, {})

                # assert there is no records in the database
                user = User.objects.filter(email='python@rocks.com')
                self.assertEqual(len(user), 0)
