from .models import Attachment 
from google.appengine.ext import db
from django.http import HttpResponse, HttpResponseRedirect


def image(request, file_id):
    response = HttpResponse(mimetype='image/png')
    image = Attachment.all().filter('containers = ', db.Key(file_id)).get()
    if image:
        response.write(image.file)
        return response
    return HttpResponseRedirect('/images/default.gif')
