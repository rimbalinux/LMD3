from livecenter.models import LiveCluster, LiveCategory
from attachment.utils import save_file_upload
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from google.appengine.ext import db

def edit(request, pid):
    if request.POST:
        save(request, pid)
        return HttpResponseRedirect(request.POST['destination'])
    return direct_to_template(request, 'cluster/edit.html', {
        'cluster': db.get(db.Key(pid)),
        'categories': LiveCategory.all(),
        'destination': 'destination' in request.GET and request.GET['destination'] or '/',
        })
    
def save(request, pid):    
    item = db.get(db.Key(pid))
    item.name = request.POST['name']
    item.info = request.POST['info']
    item.category = db.Key(request.POST['category'])
    item.put()
    save_file_upload(request, 'photo', item)
