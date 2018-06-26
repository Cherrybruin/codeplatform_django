from django.shortcuts import render, get_object_or_404
from Code_Platform.models import User, Project, ProjectPermission, ProjectLog
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
# Create your views here.


def index(req):
    try:
        return render(req, 'base.html', context={
            'login_username': req.user.username
        })
    except Exception:
        return render(req, 'base.html')




def user_register(req):
    print(req.content_params)
    if req.method == 'POST':
        print(req.POST)
        print(req.POST['username'])
        try:
            new_username = req.POST['username']
            new_password = req.POST['password']
            new_email = req.POST['email']
            User.objects.create_user(
                username=req.POST['username'], password=req.POST['password'], email=req.POST['email'])
        except Exception:
            print('create user failed, please check where is wrong')
    p = get_object_or_404(User, username=req.POST['username'])
    try:
        selected_choice = p.username
        print(selected_choice)
    except Exception:
        pass
    else:
        pass
    return HttpResponseRedirect('/')


def user_login(req):
    if req.method == 'POST':
        print(req.POST)
        user = authenticate(username=req.POST['username'], password=req.POST['password'])
        if user is not None:
            login(req, user)
            print(user, 'alkreay login')
        # A backend authenticated the credentials
        else:
            print(user, 'failed')
            pass
    # No backend authenticated the credentials
        try:
            key_word_list = ['admin', 'login', 'user', 'register', 'admin', 'index']
            if req.POST['username'] in key_word_list:
                raise Exception
            if User.objects.get(username=req.POST['username']).username == req.POST['username']:
                return HttpResponseRedirect(req.POST['username'])
        except Exception:
            return HttpResponseRedirect('./')
    else:
        return HttpResponseRedirect('../')


@login_required(redirect_field_name='../')
def user_logout(req):
    logout(req)
    return HttpResponseRedirect('../')


@login_required(redirect_field_name='../')
def user_index(req, username):
    print('the cookies user is : ', req.user)
    print(username, 'heading to his page')
    try:
        # User.objects.get(username=username)
        print(Project.objects.all())
        return render(req, 'user.html', context={
            'login_username': req.user.username,
            'username': username,
            'projects': User.objects.get(username=username).groups.all()
        })
    except Exception:
        print('login required is not alow')
        return HttpResponseRedirect('../')


@login_required(redirect_field_name='../')
def project_start(req, username):
    print(username, 'starting a project')
    if req.method == 'POST':
        print(req.POST)
        Project.objects.create(name=req.POST['projectname'], description=req.POST['description'],
                               owner=User.objects.get(username=username), statue='O')
        User.objects.get(username=username).groups.add(Project.objects.get(name=req.POST['projectname']))
    return HttpResponseRedirect('./', username)


def user_project(req, username, projectname, fpath=''):
    storge = FileSystemStorage(location='\\'.join(['static', username, projectname]), )
    if req.method == 'GET':
        try:
            if '.' in storge.path(name=fpath):
                pass
            else:
                os.makedirs(storge.path(name=fpath))
        except Exception:
            pass
        print('login user:', req.user.username)
        if fpath == '':
            # print(os.listdir(storge.path(name=fpath)))
            # print('modified time:', storge.get_modified_time())
            # print('fds:', storge.listdir(path=fpath))

            return render(req, 'project.html', context={
                'login_username': req.user.username,
                'username': username,
                'projectname': projectname,
                'fds': storge.listdir(path=fpath)[0],
                'fps': storge.listdir(path=fpath)[1]
            })
        else:
            return render(req, 'project.html', context={
                'login_username': req.user.username,
                'username': username,
                'projectname': projectname,
                'fds': storge.listdir(path=fpath)[0],
                'fps': storge.listdir(path=fpath)[1]
            })
    elif req.method == "POST":
        obj = req.FILES.get('file')
        print(type(obj))

        try:
            storge.save(name=None, content=obj)
        except Exception:
            print('some error raised when  saving post file')
            pass
        return HttpResponseRedirect('./' + projectname)


def user_project_download(req, username, projectname, fpath):
    storge = FileSystemStorage(location='\\'.join(['static', username, projectname]), )
    if storge.exists(name=fpath):
        def file_iterator(file_name, chunk_size=512):
            with open(file_name, mode='rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        the_file_name = storge.path(name=fpath)
        response = StreamingHttpResponse(file_iterator(the_file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
        return response
    else:
        pass