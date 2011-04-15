# http://docs.djangoproject.com/en/1.3/howto/custom-template-tags/#passing-template-variables-to-the-tag

from django import template
from django.template.base import Node, TemplateSyntaxError
from translate.lang import translate

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
    return TranslateNode(text) # hapus kutip
