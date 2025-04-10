from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Job 
from django.contrib.auth import authenticate
from .serializers import JobSerializer,RegisterSerializer,UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
 


@api_view(['POST'])
@permission_classes([AllowAny]) 

def register(request):
    print("Received data:", request.data)  
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])  
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    errors = {}
    if not username:
        errors["username"] = ["This field is required."]
    if not password:
        errors["password"] = ["This field is required."]

    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# List all jobs or create new
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def job_list(request):
    if request.method == 'GET':
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)#changing creator to user 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update, delete single job
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def job_detail(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

    # Read-only access
    if request.method == 'GET':
        serializer = JobSerializer(job)
        return Response(serializer.data)

    # Allow authenticated users to modify the job, not just the owner
    if request.user.is_authenticated:
        if request.method == 'PUT':
            serializer = JobSerializer(job, data=request.data)
            if serializer.is_valid():
                serializer.save(creator=request.user)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            job.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
###