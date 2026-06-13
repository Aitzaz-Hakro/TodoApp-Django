import datetime
from time import timezone
from django.conf import settings
from django.db import models  # pyright: ignore[reportMissingImports]
from rest_framework import serializers  # pyright: ignore[reportMissingImports]


class Task(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    uncompleted_at = models.DateTimeField(blank=True, null=True)

    def complete(self):
        self.completed = True
        self.completed_at = (datetime.datetime.now())
        self.save()

    def uncomplete(self):
        self.completed = False
        self.uncompleted_at = (datetime.datetime.now())
        self.save()
    def __str__(self):
        return self.title + " - " + self.user.username


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
