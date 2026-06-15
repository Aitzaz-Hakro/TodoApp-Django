from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render  # pyright: ignore[reportMissingImports]
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .models import Task


@login_required
def index(request):
    error = None
    form_data = {'title': '', 'description': '', 'due_date': ''}

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        due_date_str = request.POST.get('due_date', '').strip()
        form_data = {
            'title': title,
            'description': description,
            'due_date': due_date_str,
        }

        if not title:
            error = 'Title is required.'
        else:
            parsed_due_date = parse_datetime(due_date_str)
            if not parsed_due_date:
                error = 'Invalid due date.'
            else:
                if timezone.is_naive(parsed_due_date):
                    parsed_due_date = timezone.make_aware(
                        parsed_due_date,
                        timezone.get_current_timezone(),
                    )
                if parsed_due_date < timezone.now():
                    error = 'Due date must be in the future.'
                else:
                    Task.objects.create(  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
                        user=request.user,
                        title=title,
                        description=description,
                        due_date=parsed_due_date,
                    )
                    return redirect('index')

    tasks = Task.objects.filter(user=request.user).order_by('completed', '-created_at')  # pyright: ignore[reportAttributeAccessIssue]
    completed_count = tasks.filter(completed=True).count()
    pending_count = tasks.filter(completed=False).count()
    return render(request, 'index.html', {
        'tasks': tasks,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'error': error,
        'form_data': form_data,
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
    task = Task.objects.get(id=task_id)  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
    task.delete()
    return redirect('index')

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
    task.complete()
    task.save()
    return redirect('index')

def uncomplete_task(request, task_id):
    task = Task.objects.get(id=task_id)  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
    task.uncomplete()
    task.save()
    return redirect('index')