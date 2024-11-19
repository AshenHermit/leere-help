from django.shortcuts import render
from .models import *
import json
import traceback
import jwt
from .lib import auth as lib_auth
# Create your views here.

from django.http import HttpResponse, JsonResponse, HttpRequest


def data_view(func):
    def wrapper(request:HttpRequest):
        data = None
        error = None
        response = HttpResponse({})

        request_data = None
        if request.method == "POST":
            request_data = request.POST.dict()
        if request.method == "GET":
            request_data = request.GET.dict()

        try:
            data = func(request, response, request_data)
        except Exception as e:
            error = repr(e)

        new_response = HttpResponse(
            json.dumps({"data": data, "error": error}, ensure_ascii=False), 
            content_type="application/json")

        new_response.cookies = response.cookies
        return new_response
    return wrapper

def home(request):
    user = None
    try:
        user = lib_auth.get_authorized_user(request)
    except:
        pass
    
    if user:
        return render(request, 'task_list.html', {"user_name": user.name, "user_login": user.login})
    else:
        return render(request, 'auth.html', {})

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

@data_view
def test(request: HttpRequest, response: HttpResponse, data: dict):
    
    return request.COOKIES.get("test_cookie")


@data_view
def get_user_data(request: HttpRequest, response: HttpResponse, data: dict):
    user = lib_auth.get_authorized_user(request)
    return {"name": user.name, "pass": user.password}

@data_view
def auth(request: HttpRequest, response: HttpResponse, data: dict):
    if not "login" in data: raise Exception("no login")
    if not "password" in data: raise Exception("no password")
    login = data["login"]
    password = data["password"]

    user = lib_auth.get_authorized_user_by_credentials(login, password)
    token = lib_auth.generate_token_for_user(user)
    response.set_cookie("auth", token)

    return True