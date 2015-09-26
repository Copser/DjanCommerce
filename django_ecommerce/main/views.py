from django.shortcuts import render_to_response
from django.template import RequestContext


# Create your views here.
def index(request):
    """TODO: Docstring for index.
    :returns: TODO

    """
    return render_to_response(
        'index.html', context_instance=RequestContext(request)
    )
