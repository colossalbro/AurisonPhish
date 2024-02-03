from django.shortcuts import redirect
from django.http import HttpRequest
from django.views import View

from .utils import sessions as cookies
from decouple import config
from functools import wraps



def lazyAuthorization(view: View) -> callable:
    @wraps(view)
    def wrapper(request: HttpRequest, *args, **kwargs):
        cookie = request.COOKIES.get('manage_cookie')

        if not cookie or cookie not in cookies:
            url = config('DOMAIN_URL')
            return redirect(url, permanent=True)
        
        return view(request, *args, **kwargs)

    return wrapper