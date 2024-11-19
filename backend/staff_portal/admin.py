from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'department')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'login', 'position', 'department')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'department', 'created_at', 'completed')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('task', 'created_at')