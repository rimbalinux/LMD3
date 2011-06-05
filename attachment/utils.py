from .models import File 

def save_file_upload(request, form_name='photo_file'):
    f = request.FILES[form_name]
    file = File(name=f.name, size=f.size, mime=f.content_type, content=f.read(),
            user=request.user)
    file.save()
    return file
