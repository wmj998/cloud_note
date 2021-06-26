from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from note.models import Note
from user.models import User


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
        if not username:
            error = '请输入用户名'
            return render(request, 'register.html', locals())
        if not password_1:
            error = '请输入密码'
            return render(request, 'register.html', locals())
        if not password_2:
            error = '请再次输入密码'
            return render(request, 'register.html', locals())
        user = User.objects.filter(username=username)
        if user:
            error = '该用户已存在'
            return render(request, 'register.html', locals())
        if password_1 != password_2:
            error = '您两次输入的密码不一致'
            return render(request, 'register.html', locals())
        try:
            user = User.objects.create_user(username=username, password=password_1)
            login(request, user)
            return redirect('/user/index/')
        except Exception as e:
            print('--- register user error %s' % (e))
            error = '该用户已存在'
            return render(request, 'register.html', locals())


def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not username:
            error = '请输入用户名'
            return render(request, 'login.html', locals())
        if not password:
            error = '请输入密码'
            return render(request, 'login.html', locals())
        user = authenticate(username=username, password=password)
        if not user:
            error = '用户名或密码错误'
            return render(request, 'login.html', locals())
        login(request, user)
        return redirect('/user/index/')


@login_required
def index(request):
    username = request.user
    user = User.objects.get(username=username)
    notes = Note.objects.filter(user_id=user.id)

    page_num = request.GET.get('page', 1)
    paginator = Paginator(notes, 5)
    now_page = paginator.page(page_num)
    return render(request, 'user_index.html', locals())


def logout_user(request):
    logout(request)
    return redirect('/user/login/')


@login_required
def delete(request):
    username = request.user
    if request.method == 'GET':
        return render(request, 'delete.html', locals())
    elif request.method == 'POST':
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if not user:
            error = '您输入的密码有误'
            return render(request, 'delete.html', locals())
        user = User.objects.get(username=username)
        user.delete()
        return redirect('/index/')
