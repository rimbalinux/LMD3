from django.views.generic.simple import direct_to_template
from google.appengine.ext import db
from livecenter.utils import redirect
from .models import Transaction
import urllib


def create(request, pid): # person id
    if request.POST:
        t = Transaction(person=pid)
        save(request, t)
        return goto(request, pid)
    person = db.get(pid)
    if not person:
        return goto(request, pid)
    return direct_to_template(request, 'transaction/edit.html', {
        'person': person,
        'form_action': form_action(request, 'create', pid),
        })

def edit(request, tid): # transaction id
    t = Transaction.objects.filter(id=tid)
    if not t:
        return goto(request)
    t = t[0]
    if request.POST:
        save(request, t)
        return goto(request, t.person)
    person = db.get(t.person)
    if not person:
        return goto(request, t.person)
    return direct_to_template(request, 'transaction/edit.html', {
        'person': person,
        'transaction': t,
        'form_action': form_action(request, 'edit', tid),
        })

def save(request, t):
    t.date = request.POST['date']
    t.description = request.POST['description']
    t.nominal = request.POST['nominal']
    t.author = request.user
    t.save()

def goto(request, pid):
    return redirect(request, '/people/show/%s' % pid)

def query_string(request):
    return request.GET and '?' + urllib.urlencode(request.GET) or ''

def form_action(request, action, id):
    return '/transaction/%s/%s%s' % (action, id, query_string(request))
