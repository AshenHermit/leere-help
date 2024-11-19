from django.db import models

# Create your models here.

# Модель "Отдел"
from mptt.models import MPTTModel, TreeForeignKey
class Department(MPTTModel):
    name = models.CharField(max_length=255, verbose_name="Название отдела")
    parent = TreeForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subdepartments',
        verbose_name="Родительский отдел"
    )

    def __str__(self):
        return self.name


# Модель "Должность"
class Position(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название должности")
    level = models.PositiveIntegerField(verbose_name="Уровень должности")
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='positions',
        verbose_name="Привязка к отделу"
    )

    def __str__(self):
        return f"{self.name} (Уровень {self.level})"


# Модель "Пользователь"
class User(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    login = models.CharField(max_length=255, unique=True, verbose_name="Логин")
    password = models.CharField(max_length=255, verbose_name="Пароль")
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name="Привязка к должности"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name="Привязка к отделу"
    )

    def __str__(self):
        return self.name


# Модель "Задача"
class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание задачи", blank=True, null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks_created',
        verbose_name="Автор"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name="Отдел-адресат"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    completed = models.BooleanField(default=False, verbose_name="Завершена")

    def __str__(self):
        return self.title


# Модель "Отчет"
class Report(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name="Задача"
    )
    content = models.TextField(verbose_name="Содержимое отчета")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Отчет для задачи: {self.task.title}"