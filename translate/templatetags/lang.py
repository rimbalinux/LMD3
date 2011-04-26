# http://docs.djangoproject.com/en/1.3/howto/custom-template-tags/#passing-template-variables-to-the-tag

from django import template
from django.template.base import Node, TemplateSyntaxError
from django.utils.encoding import force_unicode
from translate.lang import translate
from django.template.defaultfilters import stringfilter
from html2text import html2text
import re

register = template.Library()

class TranslateNode(Node):
    def __init__(self, text):
        self.text = template.Variable(text)

    def render(self, context):
        request = context['request']
        text = self.text.resolve(context)
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

# Gubahan dari django/contrib/templatetags/humanize.py dengan menambahkan
# pemisah ribuan.
"""
Converts an integer to a string containing commas every three digits.
For example, 3000 becomes '3,000' and 45000 becomes '45,000'.
"""
def _money(value, separator="."):
    orig = force_unicode(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>%s\g<2>' % separator, orig)
    if orig == new:
        return new
    return _money(new, separator)

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
