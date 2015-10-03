"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from django.test import RequestFactory
from payments.models import User
from .views import index


class MainPageTests(TestCase):
    # Setup
    @classmethod
    def setUpClass(cls):
        """TODO: Docstring for setUpClass.
        :returns: TODO

        """
        request_factory = RequestFactory()
        cls.request = request_factory.get('/')
        cls.request.session = {}

    # Testing routes
    def test_root_resolves_to_main_view(self):
        """
        Testing to see that are urls are well
        connected, and to si if they exists
        """
        main_page = resolve('/')
        self.assertEqual(main_page.func, index)

    def test_returns_appropriate_html_response_code(self):
        """TODO: Docstring for test_returns_appropriate_html_response_code.
        :returns: TODO

        """
        resp = index(self.request)
        self.assertEquals(resp.status_code, 200)

    # Start testing HTML and HTML property
    def test_returns_exact_html(self):
        """TODO: Docstring for test_returns_exact_htmk.
        Testing to see did we returning real HTML page,
        and to see if html property too.

        """
        index = self.client.get("/")
        self.assertEquals(
            index.content,
            render_to_response("index.html").content
        )

    def test_index_handles_logged_in_user(self):
        """TODO: Docstring for test_index_handles_logged_in_user.
        :returns: TODO
        Testing user.html page when Users are logged in.
        Addin RequestFactory to this part of the test, so
        we can Mock are way to see if the user is propery
        creating into the database, we are also setting the
        initial state so we can test that the index view responds
        correctly when we have a logged-in user.
        At the end passing the view function we see will it return
        appoproiate HTML tempalte.

        """
        # test logic will go here
        user = User(
            name='John',
            email='john@example.com',
        )
        user.save()

        # create a Mock request objec, so we can manipulate the session
        request_factory = RequestFactory()
        request = request_factory.get('/')

        # create a session that appears to heve a logged in user
        request.session = {'user': '1'}

        # request the index page
        resp = index(request)

        # verify the response returns the page for the logged in user
        self.assertTemplateUsed(
            resp.content,
            render_to_response('user.html', {'user': user}).content
        )
