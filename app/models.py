from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    creator = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)
    executor = models.ForeignKey(User, related_name='executed_tasks', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    is_done = models.BooleanField(default=False)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.name
