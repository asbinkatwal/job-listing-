from rest_framework import generics, permissions
from .models import Job
from django.contrib.auth.models import User

from .serializers import JobSerializer
from .permissions import IsOwnerOrReadOnly

from rest_framework import generics, permissions
from .models import Job
from .serializers import JobSerializer
from .permissions import IsOwnerOrReadOnly

class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
       
        if self.request.method == 'POST':
            return []  
        return []

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            
            serializer.save(creator=self.request.user)
        else:
            
             guest_user = User.objects.get(id=1)  # Ensure this guest user exists in the database
             serializer.save(creator=guest_user)

# class JobListCreateView(generics.ListCreateAPIView):
#     queryset = Job.objects.all()
#     serializer_class = JobSerializer

#     def get_permissions(self):
#         if self.request.method == 'POST':
#             return [permissions.IsAuthenticated()]
#         return []

#     def perform_create(self, serializer):
#         serializer.save(creator=self.request.user)

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = []
