from django.shortcuts import render, redirect
from ..models import *
import json
import traceback
import jwt
from typing import List
from . import auth as lib_auth
from django.http import HttpResponseForbidden
# Create your views here.

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse, HttpRequest

def get_available_departments(user:User):
    descendants: List[Department] = user.department.get_descendants(True)
    return descendants

def get_available_tasks(user:User) -> List[Task]:
    tasks = []
    descendants: List[Department] = get_available_departments(user)
    for depart in descendants:
        dep_tasks = Task.objects.filter(department=depart)
        tasks += dep_tasks
    return tasks

def get_tasks_map(user: User, tasks: List[Task]):
    tasks_map = {}
    for task in tasks:
        tasks_map[task.pk] = {
            "pk": task.pk,
            "completed": task.completed,
            "title": task.title,
            "description": task.description,
            "department_pk": task.department.pk,
            "can_edit": can_edit_task(user, task)
        }
    return tasks_map

def can_edit_task(user:User, task:Task):
    return task.author == user and user.position.level <= 1