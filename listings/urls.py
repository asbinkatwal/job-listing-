from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:pk>/',views.job_detail, name='job_detail'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]
