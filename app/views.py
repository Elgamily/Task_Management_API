from django.shortcuts import render
from requests import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

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
class UserTasksAPIView():
    pass

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