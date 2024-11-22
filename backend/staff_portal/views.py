from django.shortcuts import render, redirect
from .models import *
import json
import traceback
import jwt
from typing import List
from . import lib
from django.http import HttpResponseForbidden
# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django.http import HttpResponse, JsonResponse, HttpRequest


def home(request):
    user = None
    try:
        user = lib.auth.get_authorized_user(request)
    except:
        pass
    
    if user:
        return redirect("/tasks")
    else:
        return render(request, 'auth.html', {})

def task_list(request):
    try:
        user = lib.auth.get_authorized_user(request)
        deps = lib.tasks.get_available_departments(user)
        tasks = lib.tasks.get_available_tasks(user)
        tasks_map = lib.tasks.get_tasks_map(user, tasks)

        can_create_task = user.position.level == 1
        
        return render(request, 'task_list.html', 
                      { 'tasks': tasks,
                        'tasks_map': mark_safe(json.dumps(tasks_map, ensure_ascii=False)), 
                        'user': user, 
                        'departments': deps, 
                        "can_create_task": can_create_task})
    except:
        traceback.print_exc()
        return render(request, 'forbidden.html')

def debug_page(request):
    users = User.objects.all()
    return render(request, 'debug.html', {'users': users})
