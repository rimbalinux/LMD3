# http://docs.djangoproject.com/en/1.3/howto/custom-template-tags/#passing-template-variables-to-the-tag

from django import template
from django.utils.safestring import mark_safe
from django.template.base import Node, TemplateSyntaxError
import re
import urllib
from translate.lang import tr

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

def singleposformat(p):
    hour = int(p)
    minute = (p - hour)*60
    return "%d&deg; %.3f'" % (hour, minute)

class GeoposNode(Node):
    def __init__(self, coordinat):
        self.coordinat = template.Variable(coordinat)

    def render(self, context):
        request = context['request']
        coordinat = self.coordinat.resolve(context)
        if not coordinat:
            return ''
        latitude, longitude = map(lambda x: singleposformat(float(x)),
                str(coordinat).split(','))
        return '%s %s, %s %s' % (
                tr('Utara', request), latitude,
                tr('Timur', request), longitude)

@register.tag
def posformat(parser, token):
    try:
        tag, coordinat = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError('Penggunaan: {% posformat <geopos> %}')
    return GeoposNode(coordinat)
