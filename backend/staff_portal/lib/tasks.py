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
    """получает список доступных для чтения отделов"""

    # получаем все дочерние отделы того отдела к которому привязан пользователь
    descendants: List[Department] = user.department.get_descendants(True)
    return descendants

def get_available_tasks(user:User) -> List[Task]:
    """используя `get_available_departments`, собирает из всех доступных отделов все задачи"""

    tasks = []
    # получаем доступные отделы
    descendants: List[Department] = get_available_departments(user)
    # перечисляем отделы
    for depart in descendants:
        # получаем задачи отдела
        dep_tasks = Task.objects.filter(department=depart)
        # добавляем их к общему списку
        tasks += dep_tasks
    return tasks

def get_tasks_map(user: User, tasks: List[Task]):
    """для преобразования списка задач в формат который читается фронт-эндом и используется на странице на стороне js"""
    tasks_map = {}
    # перечисляем задачи
    for task in tasks:
        # собираем отчеты задачи
        reports = {}
        for report in Report.objects.filter(task=task):
            # добавляем их в dict, в которой "ключ" -> "значение" это "pk отчета" -> "текст отчета"
            reports[report.pk] = report.content
        
        # 
        task_data = {
            "pk": task.pk,
            "completed": task.completed,
            "title": task.title,
            "description": task.description,
            "department_pk": task.department.pk,
            "can_edit": can_edit_task(user, task), # чтобы решить отрисовывать ли элементы редактирования или нет
            "can_add_report": can_add_report(user, task), # чтобы решить отрисовывать ли элементы добавления отчета
            "reports": reports,
        }
        # добавляем в общий dict задач
        tasks_map[task.pk] = task_data
            
    return tasks_map

def can_edit_task(user:User, task:Task):
    """проверка на то может ли пользователь редактировать/удалять задачу"""
    # только автор задачи может ее редактировать
    return task.author == user

def can_add_report(user:User, task:Task):
    """проверка на то может ли пользователь создать отчет"""
    # все из отдела которому принадлежит задача, могут создавать отчеты
    return user.department == task.department