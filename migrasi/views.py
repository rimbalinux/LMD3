from migrasi.models import Users
from django.contrib.auth.models import User
from django.views.generic.simple import direct_to_template


def user(request):
    users = Users.all().order('username')
    d = []
    for source in users:
        target = User.objects.filter(username=source.username).get()
        if target:
            if target.username == 'admin':
                target.set_password(source.passwd)
                target.save()
        else:
            target = User.objects.create_user(source.username, source.email, source.passwd)
        d.append([source, target])
    return direct_to_template(request, 'user.html', {
        'users': d 
        })
