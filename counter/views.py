from .models import Counter, Counters 
from django.views.generic.simple import direct_to_template


def migrate(request):
    sources = Counters.all().order('name')
    for source in sources:
        target = Counter.objects.filter(name=source.name)
        if target:
            target = target.get()
            target.count = source.count
        else:
            target = Counter(name=source.name, count=source.count)
        target.save()
        if 'delete' in request.GET:
            source.delete()
    return direct_to_template(request, 'counter/migrate.html', {
        'items': Counter.objects.all().order_by('name'),
        'olds': Counters.all().order('name'),
        })

