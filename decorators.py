# decorators.py
from functools import wraps
from django.http import JsonResponse, HttpResponseNotFound

def my_decorator(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        var_app_name = request.POST.get('app_name')
        if(var_app_name == 'qq'):
            return HttpResponseNotFound("Not Found") 
            # print("Decorator logic here", var_app_name)
        else:
            return func(request, *args, **kwargs)
    return wrapper
