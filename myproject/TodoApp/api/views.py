from rest_framework import generics
from TodoApp.models import Task
from TodoApp.api.serializers import TaskSerializer

class TaskListCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
    serializer_class = TaskSerializer

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
    serializer_class = TaskSerializer
