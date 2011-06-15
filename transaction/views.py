from django.views.generic.simple import direct_to_template
from livecenter.utils import redirect
from people.models import People
from .forms import TransactionForm
from .models import Transaction


def create(request, pid): # person id
    person = People.objects.get(pk=pid)
    trx = Transaction(person=person)
    return show(request, trx)

def edit(request, tid):
    trx = Transaction.objects.get(pk=tid)
    return show(request, trx)

def show(request, trx):
    form = TransactionForm(instance=trx)
    if request.POST:
        person_id = trx.person.id
        if 'delete' in request.POST:
            trx.delete()
            return redirect(request, '/people/show/%d?tab=transaction' % person_id)
        if form.is_valid():
            form.save()
            return redirect(request, '/people/show/%d?tab=transaction' % person_id)
    return direct_to_template(request, 'transaction/edit.html', {
        'form': form,
        })

