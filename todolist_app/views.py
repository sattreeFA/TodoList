from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):

    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).manage = request.user
            form.save()
        messages.success(request, ("New Task Added!"))
        return redirect('todolist')

    else:
        all_tasks = TaskList.objects.filter(manage = request.user)
        paginator = Paginator(all_tasks, 5)
        page_number = request.GET.get('page')
        all_tasks = paginator.get_page(page_number)

        return render(request, 'todolist.html', {'all_tasks': all_tasks})

@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.error(request, ("Not allowed to perform this function"))
    return redirect('todolist')

@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        updated_task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=updated_task)
        if form.is_valid():
            form.save()
        messages.success(request, ("Task Edited!"))
        return redirect('todolist')

    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {'task_obj': task_obj})

@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request, ("Not allowed to perform this function"))
    return redirect('todolist')

@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = False
        task.save()
    else:
        messages.error(request, ("Not allowed to perform this function"))
    return redirect('todolist')

def contact(request):
    data = {
        'welcome_text':'Welcome to the ContactUs page!'
    }
    return render(request, 'contact.html', data)

def about(request):
    data = {
        'welcome_text':'Welcome to the AboutUs page!'
    }
    return render(request, 'about.html', data)

def index(request):
    data = {
        'index_text':'Welcome to the Home page!'
    }
    return render(request, 'index.html', data)