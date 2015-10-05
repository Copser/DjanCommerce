"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
# import unittest
from django.test import TestCase, SimpleTestCase, RequestFactory
from django import forms
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from payments.models import User
from payments.forms import SigninForm, UserForm
from .views import sign_in, sign_out


class UserModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Setup
        """
        cls.test_user = User(email="j@j.com", name='test_user')
        cls.test_user.save()

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


class FormTextMixin():

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


class FormTests(SimpleTestCase, FormTextMixin):

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
        self.assertTrue(form.is_valid(), form.errors)

        # this will throw an error if the form doesn't clean
        # correctly
        self.assertIsNotNone(form.clean())

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

        self.assertRaisesMessage(forms.ValidationError,
                                 "Password do not match",
                                 form.clean)


class ViewTextMixin(object):

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

    def test_returns_appropriate_response_code(self):
        """TODO: Docstring for test_returns_appropriate_response_code.
        :returns: TODO

        """
        resp = self.view_func(self.request)
        self.assertEquals(resp.status_code, self.status_code)

    def test_returns_correct_html(self):
        """TODO: Docstring for test_returns_correct_html.
        :returns: TODO

        """
        resp = self.view_func(self.request)
        self.assertEquals(resp.content, self.expected_html)


class SignInPageTests(TestCase, ViewTextMixin):

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

        ViewTextMixin.setupViewTester(
            '/sign_in',
            sign_in,
            html.content
        )


class SignOutPageTests(TestCase, ViewTextMixin):

    """Docstring for SignOutPageTests. """
    @classmethod
    def setUpClass(cls):
        ViewTextMixin.setupViewTester(
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
