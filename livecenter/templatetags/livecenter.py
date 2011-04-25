# http://docs.djangoproject.com/en/1.3/howto/custom-template-tags/#passing-template-variables-to-the-tag

from django import template

register = template.Library()

def metaview(item, meta):
    if meta.form_type == 'file':
        return ''
    try:
        return getattr(item, meta.slug)
    except:
        return ''

metaview.is_safe = True
register.filter('metaview', metaview)
