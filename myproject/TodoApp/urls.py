from django.urls import path  # pyright: ignore[reportMissingImports]
from . import views  # pyright: ignore[reportMissingImports]

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('uncomplete_task/<int:task_id>/', views.uncomplete_task, name='uncomplete_task'),
]