from django.urls import path
from .views import JobListView, JobCreateView, JobDetailView, JobUpdateView, JobDeleteView

urlpatterns = [
    path('api/jobs/', JobListView.as_view(), name='job-list'),
    path('api/jobs/create/', JobCreateView.as_view(), name='job-create'),
    path('api/jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('api/jobs/<int:pk>/update/', JobUpdateView.as_view(), name='job-update'),
    path('api/jobs/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
]
