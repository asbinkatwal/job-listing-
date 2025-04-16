from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:pk>/',views.job_detail, name='job_detail'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    path('upload/', views.upload_file, name='upload-file'),
    path('files/', views.list_files, name='list-files'),
    path('files/<int:pk>/', views.retrieve_file, name='retrieve-file'),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

