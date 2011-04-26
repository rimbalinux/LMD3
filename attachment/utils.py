from .models import Attachment
from google.appengine.ext import db

def save_file_upload(request, field, container):
    if field not in request.FILES:
        return
    att = Attachment.all().filter('containers', container.key()).get()
    if not att:
        att = Attachment()
    att.containers.append(container.key())
    att.filename = '%s_%s' % (field, container.key().id())
    att.filesize = 1024
    att.file = db.Blob(request.FILES[field].read())
    att.put()
    return att
