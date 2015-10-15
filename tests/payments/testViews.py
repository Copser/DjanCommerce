from payments.views import sign_in, sign_out, register, soon
from django.test import TestCase, RequestFactory
from payments.models import User
from payments.forms import SigninForm, UserForm
from django.db import IntegrityError
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
import django_ecommerce.settings as settings
import mock
import socket


class ViewTesterMixin(object):

    """Docstring for ViewTesterMixin. """
    @classmethod
    def setupViewTester(cls, url, view_func, expected_html,
                        status_code=200,
                        session={}):
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
        :returns: Test to see if we can return wright url.

        """
        test_view = resolve(self.url)
        self.assertEqual(test_view.func, self.view_func)

#    def test_returns_appropriate_response_code(self):
#        """TODO: Docstring for test_returns_appropriate_response_code.
#        :returns: Testing to see if we can return appropriate status_code
#
#        """
#        resp = self.view_func(self.request)
#        self.assertEqual(resp.status_code, self.status_code)
#
#    def test_returns_correct_html(self):
#        """TODO: Docstring for test_returns_correct_html.
#        :returns: Testing to see will we return correct html
#
#        """
#        resp = self.view_func(self.request)
#        self.assertEqual(resp.content, self.expected_html)
#


class SignInPageTest(TestCase, ViewTesterMixin):

    """Docstring for SignInPageTest. Building test for
    SignInPage."""
    @classmethod
    def setUpClass(cls):
        """TODO: Docstring for setUpCla.

        :s(cl: TODO
        :returns: TODO

        """
        super().setUpClass()
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


class SignOutPageTest(TestCase, ViewTesterMixin):

    """Docstring for SignOutPageTest. Building tests for SignOutPag
    to see will page sign_out user properly. and will it redirect
    user to proper html page."""
    @classmethod
    def setUpClass(cls):
        """TODO: Docstring for setUpClass.
        :returns: TODO

        """
        super().setUpClass()
        ViewTesterMixin.setupViewTester(
            '/sign_out',
            sign_out,
            b"",  # a redirect will return an empty bytestering
            status_code=302,
            session={'user': 'dummy'},
        )

    def setUp(self):
        """TODO: Docstring for setUp.
        :returns: Sign_out clears the session, so let;s reset it everytime

        """
        self.request.session = {'user': 'dummy'}


class RegisterPageTests(TestCase, ViewTesterMixin):

    """Docstring for RegisterPageTests. """
    @classmethod
    def setUpClass(cls):
        """TODO: Docstring for setUpClass.
        :returns: TODO

        """
        super().setUpClass()

        html = render_to_response(
            'register.html',
            {
                'form': UserForm(),
                'months': list(range(1, 12)),
                'publishable': settings.STRIPE_PUBLISHABLE,
                'soon': soon(),
                'user': None,
                'years': list(range(2011, 2036)),
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
        :returns: Testing to see will form error return User to registration
        page

        """
        with mock.patch('payments.forms.UserForm.is_valid') as user_mock:
            user_mock.return_value = False
            self.request.method = 'POST'
            self.request.POST = None
            resp = register(self.request)
            self.assertEqual(resp.content, self.expected_html)

            # make sure that we did indeed call our is_valid function
            self.assertEqual(user_mock.call_count, 1)

    def test_registering_user_when_stripe_is_down(self):
        """TODO: Docstring for test_registering_user_when_stripe_is_down.
        :returns: TODO

        """
        # create the request user to test the view
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

        # mock out Stripe and as it to trow a connection error
        with mock.patch(
            'stripe.Customer.create',
            side_effect=socket.error("Can't connect to Stripe")
        ) as stripe_mock:

            # run the test
            register(self.request)

            # assert ther is a record in the database without Stripe id.
            users = User.objects.filter(email="python@rocks.com")
            self.assertEquals(len(users), 1)
            self.assertEquals(users[0].stripe_id, '')

    def get_mock_cust():
        """TODO: Docstring for get_mock_cust.
        :returns: TODO

        """
        class mock_cust():
            @property
            def id(self):
                """TODO: Docstring for id.
                :returns: TODO

                """
                return 1234

        return mock_cust()

    @mock.patch('payments.views.Customer.create',
                return_value=get_mock_cust())
    def test_registering_new_user_returns_succesfully(self, stripe_mock):
        """TODO: Docstring for test_registering_new_user_returns_succesfully.
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

        resp = register(self.request)

        self.assertEqual(resp.content, b"")
        self.assertEqual(resp.status_code, 302)

        users = User.objects.filter(email="python@rocks.com")
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].stripe_id, '1234')

    def get_MockUserForm(self):
        """TODO: Docstring for get_MockUserForm.
        :returns: TODO

        """
        from django import forms

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
                    'last_4_digits': '4242',
                    'password': 'bad_password',
                    'ver_password': 'bad_password',
                }

            def addError(self, error):
                """TODO: Docstring for addError.
                :returns: TODO

                """
                pass

        return MockUserForm()
