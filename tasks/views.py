from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm
from .models import Task


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('task_list')
    else:
        form = UserCreationForm()

    return render(request, 'tasks/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.info(request, f'Welcome back, {user.username}!')
            return redirect('task_list')
    else:
        form = AuthenticationForm()

    return render(request, 'tasks/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.warning(request, 'You have been logged out.')
    return redirect('login')


@login_required
def task_list(request):
    search_query = request.GET.get('q', '')

    tasks = Task.objects.filter(
        user=request.user,
        title__icontains=search_query
    ).order_by('-created_at')

    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query
    }

    return render(request, 'tasks/task_list.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            messages.success(request, 'New task added!')
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(
        request,
        'tasks/task_form.html',
        {'form': form, 'title': 'Create Task'}
    )


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(
        request,
        'tasks/task_form.html',
        {'form': form, 'title': 'Edit Task'}
    )


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.delete()
        messages.error(request, 'Task deleted!')
        return redirect('task_list')

    return render(
        request,
        'tasks/task_confirm_delete.html',
        {'task': task}
    )