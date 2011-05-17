# http://djangobook.com/en/2.0/chapter14/

from django.contrib import auth
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from translate.lang import tr
from .models import Users
from django.contrib.auth.models import User


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/sudah-login-%s' % request.user.username)
    if not request.POST:
        return direct_to_template(request, 'login.html')
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password) # just check
    if user is not None and user.is_active:
        auth.login(request, user) # session
        return HttpResponseRedirect('/')
    return direct_to_template(request, 'login.html', {
        'error': tr('Login gagal', request),
        })

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def migrate(request):
    users = Users.all().order('username')
    d = []
    for source in users:
        target = User.objects.filter(username=source.username)
        if target:
            target = target.get()
            if target.username == 'admin':
                target.set_password(source.passwd)
                target.save()
        else:
            target = User.objects.create_user(source.username, source.email, source.passwd)
        d.append([source, target])
    return direct_to_template(request, 'user.html', {
        'users': d 
        })
