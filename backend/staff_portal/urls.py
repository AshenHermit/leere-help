from django.urls import path
from . import views
from .api import api

urlpatterns = [
    path('', views.home, name='home'),
    path('debug/', views.debug_page, name='debug'),
    path('tasks/', views.task_list, name='task_list'),
    path('reports/<int:pk>', views.report_page, name='report_page'),
    
    path('api/user/', api.get_user_data, name='get_user_data'),
    path('api/auth/', api.auth, name='auth'),
    path('api/tasks/save', api.task_save, name='task_save'),
    path('api/tasks/delete', api.task_delete, name='task_delete'),
    
    path('api/debug_auth/', api.debug_auth_user, name='debug_auth'),
]