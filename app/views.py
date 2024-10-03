from django.shortcuts import render
from requests import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *

#First student's tasks:
class UserCreateView():
    pass

class LoginView():
    pass

class LogoutView():
    pass

class TaskCreateView():
    pass

class TasksCreatedByUser():
    pass

class TaskWithExecutorAPIView():
    pass

#Second student's tasks:
class UserTasksAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    # Return tasks
    def get_queryset(self):
        return Task.objects.filter(executor=self.request.user)

class UserTasksStatsAPIView():
    pass

class UnassignedTasksAPIView():
    pass

class BecomeExecutorAPIView():
    pass

class MarkTaskDoneAPIView():
    pass

class ClearDatabaseView(APIView):
    def post(self, request):
        Task.objects.all().delete()
        User.objects.all().delete()
        return Response({'message': 'All data cleared successfully'}, status=200)