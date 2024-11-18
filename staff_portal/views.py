from django.shortcuts import render
from .models import *
import json
# Create your views here.

from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, Django!")

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def test(request):
    deps = Department.objects.first().get_descendants(include_self=True)
    data = []
    for dep in deps:
        data.append(dep.name)
    return render(request, 'test.html', {'data': json.dumps(data, ensure_ascii=False, indent=2)})