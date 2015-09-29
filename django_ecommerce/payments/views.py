from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from payments.forms import SigninForm, CardForm, UserForm
from payments.models import User
import django_ecommerce.settings as settings
import stripe
import datetime
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET


def soon():
    """TODO: Docstring for soon.
    This function returns current datetime,
    and the current duration between time
    """
    soon = datetime.date.today() + datetime.timedelta(days=30)
    return {'month': soon.month, 'year': soon.year}


def sign_in(request):
    """TODO: Docstring for sign_in.
    :returns: TODO
    Sign in form function, checks if user make
    a valid email and password to are db, if not
    trows an error
    """
    user = None
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            results = User.objects.filter(email=form.cleaned_data['email'])
            if len(results) == 1:
                if results[0].check_password(form.cleaned_data['password']):
                    request.session['user'] = results[0].pk
                    return HttpResponseRedirect('/')
                else:
                    form.addError('Incorrect email address or password')
            else:
                form.addError('Incorrect email address or password')
    else:
        form = SigninForm()
    print form.non_field_errors()

    return render_to_response('sign_in.html', {'form': form, 'user': user},
                              context_instance=RequestContext(request))


def sign_out(request):
    """TODO: Docstring for sign_out.
    :returns: TODO
    Handle sign_out from the import application,
    when user sign out retern him on home page.
    """
    del request.session['user']
    return HttpResponseRedirect('/')


def register(request):
    """TODO: Docstring for register.
    :returns: TODO
    Handle User registration, and user registration for
    Stripe chargeing.
    """
    user = None
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # update based on your billing method (subscription vs
            # one time)
            customer = stripe.Customer.create(
                email=form.cleaned_data['email'],
                description=form.cleaned_data['name'],
                card=form.cleaned_data['stripe_token'],
                plan='gold',
            )

            customer = stripe.Charge.create(
                description=form.cleaned_data['email'],
                card=form.cleaned_data['stripe_token'],
                amount="5000",
                currency="usd"
            )

            user = User(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                last_4_digits=form.cleaned_data['last_4_digits'],
                stripe_id=customer.id,
            )
            # ensure encrypted password
            user.set_password(form.cleaned_data['password'])

            try:
                user.save()
            except IntegrityError:
                form.addError(user.email + ' is already a member')
            else:
                request.session['user'] = user.pk
                return HttpResponseRedirect('/')
    else:
        form = UserForm()

    return render_to_response(
        'register.html',
        {
            'form': form,
            'months': range(1, 12),
            'publishable': settings.STRIPE_PUBLISHABLE,
            'soon': soon(),
            'user': user,
            'years': range(2011, 2036),
        },
        context_instance=RequestContext(request)
    )


def edit(request):
    """TODO: Docstring for edit.
    :returns: TODO
    Handles the user credit card, numbers and
    last_4_digits, when user whant to pay for
    a service.
    """
    uid = request.session.get('user')

    if uid is None:
        return HttpResponseRedirect('/')

    user = User.objects.get(pk=uid)

    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid:
            customer = stripe.Customer.retrieve(user.stripe_id)
            customer.card = form.cleaned_data['stripe_token']
            customer.save()

            user.last_4_digits = form.cleaned_data['last_4_digits']
            user.stripe_id = customer.id
            user.save()

            return HttpResponseRedirect('/')
    else:
        form = CardForm()

    return render_to_response(
        'edit.html',
        {
            'form': form,
            'publishable': settings.STRIPE_PUBLISHABLE,
            'soon': soon(),
            'months': range(1, 12),
            'years': range(2011, 2036)
        },
        context_instance=RequestContext(request)
    )
