from django.test import TestCase
from payments.forms import SigninForm, CardForm, UserForm


class FormTesterMixin():

    """Docstring for FormTesterMixin. We are testing if are form's are
    configurated good and will they be valid, and building errors for
    forms test."""
    def should_have_form_error(
        self, form_cls, expected_error_name,
        expected_error_msg, data
    ):

        """Testing to see will form return eny error."""
        from pprint import pformat
        test_form = form_cls(data=data)
        # if we got an error then form should not be valid
        self.assertFalse(test_form.is_valid())

        self.assertEqual(
            test_form.errors[expected_error_name],
            expected_error_msg,
            msg="Expected {} : Actual {} : using data {}".format(
                test_form.errors[expected_error_name],
                expected_error_msg, pformat(data)
            )
        )


class FormTests(FormTesterMixin, TestCase):

    """Docstring for FormTests. """
    def test_signin_form_data_validation_for_invalid_data(self):
        """TODO: Docstring for test_signin_form_data_validation_for.

        :returns: Testing to see will are user signin succesfilly,
        if not it will raise error.

        """
        invalid_data_list = [
            {'data': {'email': 'j@j.com'},
             'error': ('password', ['This field is required.'])},
            {'data': {'password': '1234'},
             'error': ('email', ['This field is required.'])}
        ]

        for invalid_data in invalid_data_list:
            self.should_have_form_error(
                SigninForm,
                invalid_data['error'][0],
                invalid_data['error'][1],
                invalid_data['data']
            )

    def test_user_form_passwords_match(self):
        """TODO: Test to see will users password be succesfilly
        validated, if not raise and error.

        """
        form = UserForm(
            {
                'name': 'jj',
                'email': 'j@j.com',
                'password': '1234',
                'ver_password': '1234',
                'last_4_digits': '3333',
                'stripe_token': '1'}
        )
        # Is the data valid?
        if form.is_valid():
            # Is the data cleand?
            self.assertTrue(form.cleaned_data)

    def test_user_form_password_dont_match_throws_error(self):
        """TODO: Testing password not match, to see will it return
        error if password not match each other.

        """
        form = UserForm(
            {
                'name': 'jj',
                'email': 'j@j.com',
                'password': '234',
                'ver_password': '1234',  # bad password
                'last_4_digits': '3333',
                'stripe_token': '1'}
        )

        # Is the data valid?
        self.assertFalse(form.is_valid())

#    def test_card_form_data_validation_for_invalid_data(self):
#        """TODO: Testing CardForm to see if boundary checking are
#        working correctly, other name for this is performing QA team
#        tests.
#
#        """
#        invalid_data_list = [
#            {
#                'data': {'last_4_digits': '123'},
#                'error': (
#                    'last_4_digits',
#                    ['Ensure this value has at least \
#                        4 characters (it has 3).']
#                )
#            },
#            {
#                'data': {'last_4_digits': '12345'},
#                'error': (
#                    'last_4_digits',
#                    ['Ensure this value has at most \
#                            4 characters (it has 5).']
#                )
#            },
#        ]
#        for invalid_data in invalid_data_list:
#            self.should_have_form_error(
#                CardForm,
#                invalid_data['error'][0],
#                invalid_data['error'][1],
#                invalid_data["data"]
#            )
