from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.task_list, name='task_list'),
    path('test/', views.test, name='test'),
    path('api/user/', views.get_user_data, name='get_user_data'),
    path('api/auth/', views.auth, name='auth'),
    path('api/logout/', views.logout, name='logout'),
]