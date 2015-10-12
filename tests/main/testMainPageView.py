from django.test import TestCase
from django.core.urlresolvers import resolve
from main.views import index
from django.shortcuts import render_to_response
from django.test import RequestFactory
import mock


class MainPageTests(TestCase):

    """Docstring for MainPageTests. """
    # Setup
    def setUpClass(cls):
        """TODO: Docstring for setUpClass.
        :returns: TODO

        """
        super(MainPageTests, cls).setUpClass()
        request_factory = RequestFactory()
        cls.request = request_factory.get('/')
        cls.request.session = {}

        # Testing Routes
        def test_root_resolves_to_main_view(self):
            """TODO: Docstring for test_root_resolves_to_main_view.
            :returns: TODO

            """
            main_page = resolve('/')
            self.assertEqual(main_page.func, index)

        def test_returns_appropriate_html_response_code(self):
            """TODO: Docstring for test_returns_appropriate_html_response_code.
            :returns: TODO

            """
            resp = index(self.request)
            self.assertEqual(resp.status_code, 200)

        # Testing templates and views
        def test_returns_exact_html(self):
            """TODO: Docstring for test_returns_exact_html.
            :returns: TODO

            """
            resp = index(self.request)
            self.assertEqual(
                resp.content,
                render_to_response('index.html').content
            )

        def test_index_handlers_logged_in_user(self):
            """TODO: Docstring for test_index_handlers_logged_in_user.
            :returns: TODO

            """
            self.request.session = {'user': '1'}

            with mock.patch('main.views.User') as user_mock:
                # Tell the mock what to do when called
                config = {'get_by_id.return_value': mock.Mock()}
                user_mock.configure_mock(**config)

                # Run the test
                resp = index(self.request)

                # Enshure we return the state of the session back to normal
                self.request.session = {}
                expected_html = render_to_response(
                    'user.html', {'user': user_mock.get_by_id(1)}
                )
                self.assertEqual(resp.contetn, expected_html.content)
