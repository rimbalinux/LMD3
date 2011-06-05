# http://docs.djangoproject.com/en/1.3/howto/custom-template-tags/#passing-template-variables-to-the-tag

from django import template
from django.template.base import Node, TemplateSyntaxError
from translate.lang import translate, tr, money as _money
from django.template.defaultfilters import stringfilter
from html2text import html2text

register = template.Library()

##############
# Translator #
##############
class TranslateNode(Node):
    def __init__(self, text):
        self.text = template.Variable(text)

    def render(self, context):
        text = self.text.resolve(context)
        if 'request' not in context:
            return text
        request = context['request']
        try:
            return translate(text, to=request.session.get('lang','id'))
        except template.VariableDoesNotExist:
            return 'Variabel tidak ada'

@register.tag
def t(parser, token):
    try:
        tag, text = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError('Penggunaan tag t: {% t "pesan" %}')
    return TranslateNode(text)

def t_(text, request):
    return html2text(translate(text, to=request.session.get('lang','id')))
t_.is_safe = True
t_ = stringfilter(t_)
register.filter('t', t_)

MONEY_LANGUAGE = { 
    'id': ['.',','],
    'en': [',','.'],
    }

class MoneyNode(Node):
    def __init__(self, text):
        self.text = template.Variable(text)

    def render(self, context):
        request = context['request']
        text = self.text.resolve(context)
        if text is None:
            return ''
        language = request.session.get('lang','id')
        sep = language in MONEY_LANGUAGE and MONEY_LANGUAGE[language][0] or '.'
        return _money(text, sep)

@register.tag
def money(parser, token):
    try:
        tag, text = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError('Penggunaan tag money: {% money 10000 %}')
    return MoneyNode(text)


#######################
# Geo position format #
#######################
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

##########
# String #
##########
def _str(s):
    if s is None:
        return ''
    return s
register.filter('s', _str)


