from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from requests import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import status
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

class UserTasksStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Number of completed tasks
        completed_tasks = Task.objects.filter(executor=user, is_done=True).count()

        # Number of pending tasks
        pending_tasks = Task.objects.filter(executor=user, is_done=False, deadline__gte=now()).count()

        # Number of overdue tasks
        overdue_tasks = Task.objects.filter(executor=user, is_done=False, deadline__lt=now()).count()

        # Number of tasks
        assigned_tasks = Task.objects.filter(creator=user).count()

        # Total amount earned: Sum of costs for completed tasks
        total_earned = Task.objects.filter(executor=user, is_done=True).aggregate(total_earned=models.Sum('cost'))['total_earned'] or 0

        # Total amount spent: Sum of costs for assigned tasks
        total_spent = Task.objects.filter(creator=user).aggregate(total_spent=models.Sum('cost'))['total_spent'] or 0

        # Response data
        stats = {
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'overdue_tasks': overdue_tasks,
            'assigned_tasks': assigned_tasks,
            'total_earned': total_earned,
            'total_spent': total_spent
        }

        return Response(stats, status=200)

class UnassignedTasksAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        # Return tasks where executor is None and sorted by cost in ascending order
        return Task.objects.filter(executor__isnull=True).order_by('cost')

class BecomeExecutorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, task_id):
        user = request.user

        # Get the task by id or return 404 if not found
        task = get_object_or_404(Task, id=task_id)

        # Check if the current user is the creator of the task
        if task.creator == user:
            return Response({'error': 'You cannot assign yourself as executor of your own task'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the task already has an executor
        if task.executor is not None:
            return Response({'error': 'This task already has an executor'}, status=status.HTTP_400_BAD_REQUEST)

        # Assign the current user as the executor
        task.executor = user

        # Save the task
        task.save()

        return Response({'message': 'You have been assigned as the executor of the task'}, status=status.HTTP_200_OK)

class MarkTaskDoneAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, task_id, *args, **kwargs):
        user = request.user

        # Get the task by id or return 404 if not found
        task = get_object_or_404(Task, id=task_id)

        # Check if the current user is the executor of the task
        if task.executor != user:
            return Response({'error': 'You are not authorized to mark this task as done'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the task as done
        task.is_done = True
        task.save()

        # Serialize the task and return the response
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClearDatabaseView(APIView):
    def post(self, request):
        Task.objects.all().delete()
        User.objects.all().delete()
        return Response({'message': 'All data cleared successfully'}, status=200)