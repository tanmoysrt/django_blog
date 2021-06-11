from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from functools import wraps

#
# def normalUserRequired(view_func):
#     @wraps(view_func)
#     def wrap(request, *args, **kwargs):
#         if request.user.is_authenticated:
#
#         else:
#             return view_func(request, *args, **kwargs)
#
#     return wrap