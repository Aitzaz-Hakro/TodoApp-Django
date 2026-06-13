from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render  # pyright: ignore[reportMissingImports]

from .models import Task


@login_required
def index(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        due_date = request.POST.get('due_date', '').strip()
        
        if title:
            task = Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                due_date=due_date
            )
        return redirect('index')

    tasks = Task.objects.filter(user=request.user).order_by('completed', '-created_at')
    completed_count = tasks.filter(completed=True).count()
    pending_count = tasks.filter(completed=False).count()
    return render(request, 'index.html', {
        'tasks': tasks,
        'completed_count': completed_count,
        'pending_count': pending_count,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already taken'})
        user = User.objects.create_user(username=username, password=password)
        auth_login(request, user)
        return redirect('index')

    return render(request, 'signup.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('index')

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.complete()
    task.save()
    return redirect('index')

def uncomplete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.uncomplete()
    task.save()
    return redirect('index')