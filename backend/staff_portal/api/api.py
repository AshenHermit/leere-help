from django.shortcuts import render, redirect
from ..models import *
import json
import traceback
import jwt
from ..lib import auth as lib_auth, tasks as lib_tasks
# Create your views here.

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse, HttpRequest

def data_view(func):
    @csrf_exempt
    def wrapper(request:HttpRequest):
        data = None
        error = None
        response = HttpResponse({})

        request_data = None
        if request.method == "POST":
            request_data = json.loads(request.body)
        if request.method == "GET":
            request_data = request.GET.dict()

        try:
            data = func(request, response, request_data)
        except Exception as e:
            error = repr(e)
            traceback.print_exc()

        new_response = HttpResponse(
            json.dumps({"data": data, "error": error}, ensure_ascii=False), 
            content_type="application/json")

        new_response.cookies = response.cookies
        return new_response
    return wrapper

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

@data_view
def debug_auth_user(request: HttpRequest, response: HttpResponse, data: dict):
    if not "login" in data: raise Exception("no login")
    login = data["login"]

    user = User.objects.get(login=login)
    token = lib_auth.generate_token_for_user(user)
    response.set_cookie("auth", token)

    return True

@data_view
def task_save(request: HttpRequest, response: HttpResponse, data: dict):
    if not "pk" in data: raise Exception("no pk")

    user = lib_auth.get_authorized_user(request)
    task = None
    if user:
        if data["pk"] == None:
            task = Task()
        else:
            task = Task.objects.get(pk=data["pk"])
            if not lib_tasks.can_edit_task(user, task):
                return False
        
        if task:
            task.title = data["title"]
            task.description = data["description"]
            task.department = Department.objects.get(pk=data["department_pk"])
            deps = lib_tasks.get_available_departments(user)
            if not task.department in deps: return False
            task.author = user
            task.completed = data["completed"]
            task.save()
            return True

    return False

@data_view
def task_delete(request: HttpRequest, response: HttpResponse, data: dict):
    if not "pk" in data: raise Exception("no pk")

    user = lib_auth.get_authorized_user(request)
    task = Task.objects.get(pk=data["pk"])
    if not lib_tasks.can_edit_task(user, task):
        return False
    task.delete()
    return True