from django.urls import path  # pyright: ignore[reportMissingImports]
from TodoApp.api.views import TaskListCreate, TaskDetail


urlpatterns = [
    path('tasks/', TaskListCreate.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
]