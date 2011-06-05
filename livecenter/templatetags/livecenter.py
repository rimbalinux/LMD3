# http://docs.djangoproject.com/en/1.3/howto/custom-template-tags/#passing-template-variables-to-the-tag

import re
import urllib
from django import template
from django.utils.safestring import mark_safe
from django.template.base import Node, TemplateSyntaxError
from translate.lang import translate
from home.settings import DEFAULT_LOCATION
from globalrequest.middleware import get_request

register = template.Library()

############
# Metaform #
############
def _metaform(item, meta):
    t = meta.form_type
    try:
        val = getattr(item, meta.slug)
    except:
        val = ''
    if t == 'file':
        return '<input type="file" name="'+meta.slug+'" id="'+meta.slug+'" value=""/>'
    elif t == 'select':
        v = '<select name="'+meta.slug+'">'
        for opt in re.split("\n", meta.attribute):
            v += '<option value="'+opt+'">'+opt+'</option>'
        v += '</select>'
        return v
    elif t == 'textarea':
        return '<textarea name="'+meta.slug+'" style="width:100%;">'+val+'</textarea>'
    return '<input type="text" name="'+meta.slug+'" id="'+meta.slug+'" value="'+val+'" style="width:90%" />'

def metaform(item, meta, autoescape=None):
    return mark_safe(_metaform(item, meta))
metaform.needs_autoescape = True
register.filter(metaform)
 
############
# Metaview #
############
def metaview(item, meta):
    if meta.form_type == 'file':
        return ''
    try:
        return getattr(item, meta.slug)
    except:
        return ''
metaview.is_safe = True
register.filter(metaview)

##############
# Dictionary #
##############
def dictval(d, key):
    return d[key] 
register.filter('dict', dictval)

def dictquery(d):
    return urllib.urlencode(d)
register.filter(dictquery)

###############
# Tab default #
###############
def _tabdefault(d, checkval):
    return 'tab' in d and d['tab'] in [checkval, str(checkval)] \
            and 'tabbertabdefault' or ''

class TabdefaultNode(Node):
    def __init__(self, text):
        self.text = template.Variable(text)

    def render(self, context):
        request = context['request']
        text = self.text.resolve(context)
        return _tabdefault(request.GET, text)

@register.tag
def tabdefault(parser, token):
    try:
        tag, text = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError('Penggunaan: {% tabdefault "namatab" %}')
    return TabdefaultNode(text)

################
# Geo Position #
################
def positions(coordinat):
    return coordinat and 'positions.push(Array(%s));' % coordinat or ''
register.filter(positions)

def geo_pos(form):
    request = get_request()
    return hasattr(form.instance, 'geo_pos') and form.instance.geo_pos or \
        (hasattr(request, 'POST') and 'geo_pos' in request.POST and \
        request.POST['geo_pos']) or \
        ', '.join(map(lambda x: str(x), DEFAULT_LOCATION))
register.filter(geo_pos)


##############
# Form field #
##############
class FormFieldNode(template.Node):
    def __init__(self, text):
        self.text = template.Variable(text) 

    def render(self, context):
        bf = self.text.resolve(context)
        request = context.get('request', None)
        if request is None:
            label = bf.label
        else:
            language = request.session.get('lang','id')
            label = translate(bf.label, to=language)
        req = _required(bf.field.required)
        label = '<label>%s:%s</label>' % (label, req)
        errors = bf.errors and '\n' + str(bf.errors) or ''
        return "\n" + '<div class="field-wrapper">' + \
            "\n" + label + \
            "\n" + bf.as_widget() + \
            errors + \
            "\n</div>"

@register.tag
def formfield(parser, token):
    try:
        tag, text = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError('Contoh penggunaan tag formfield: {% formfield form.name %}')
    return FormFieldNode(text)

def required(bf, autoescape=None):
    return mark_safe(_required(bf.field.required))
required.needs_autoescape = True
register.filter(required)

def _required(yes):
    return yes and ' <span class="required">*</span>' or ''

def has_attr(obj, attrname):
    return hasattr(obj, attrname)
register.filter(has_attr)

