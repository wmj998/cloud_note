from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from note.models import Note
from user.models import User


@login_required
def add(request):
    if request.method == 'GET':
        return render(request, 'add.html')
    elif request.method == 'POST':
        username = request.user
        title = request.POST['title']
        if not title:
            error = '请输入标题'
            return render(request, 'add.html', locals())
        content = request.POST['content']
        user = User.objects.get(username=username)
        Note.objects.create(title=title, content=content, user_id=user.id)
        return redirect('/user/index/')


@login_required
def update(request):
    note_id = request.GET.get('id')
    note = Note.objects.get(id=note_id)
    if request.method == 'GET':
        return render(request, 'update.html', locals())
    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        note.title = title
        note.content = content
        note.save()
        return redirect('/user/index/')


@login_required
def delete(request):
    note_id = request.GET.get('id')
    note = Note.objects.get(id=note_id)
    note.delete()
    return redirect('/user/index/')


@login_required
def search(request):
    username = request.user
    user = User.objects.get(username=username)
    notes = Note.objects.filter(user_id=user.id)

    page_num = request.GET.get('page', 1)
    paginator = Paginator(notes, 5)
    now_page = paginator.page(page_num)

    result = request.POST['search']
    search_notes = Note.objects.filter(title=result)
    if not search_notes:
        error = '暂无搜索结果'
    return render(request, 'user_index.html', locals())


@login_required
def result(request):
    id = request.GET.get('id')
    note = Note.objects.get(id=id)
    user = User.objects.get(id=note.user_id)
    return render(request, 'result.html', locals())
